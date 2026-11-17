"""Synthetic-only validation helpers for the Lexora dataset procedure."""
from __future__ import annotations
import hashlib
import json
import re
import unicodedata
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schemas" / "dataset-records-v1.schema.json"

def load_schema(path: Path = SCHEMA_PATH) -> dict[str, Any]:
    schema = json.loads(path.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema

def validate_record_schema(record: dict[str, Any], schema: dict[str, Any] | None = None) -> list[str]:
    validator = Draft202012Validator(schema or load_schema(), format_checker=FormatChecker())
    return [e.message for e in validator.iter_errors(record)]

def validate_sentence_offsets(record: dict[str, Any]) -> list[str]:
    """Check zero-based, end-exclusive Unicode code-point offsets into raw_text."""
    errors, raw = [], record.get("raw_text")
    sentences = record.get("sentences")
    if not isinstance(raw, str): return ["raw_text must be a string"]
    if not isinstance(sentences, list): return ["sentences must be an array"]
    previous_end, seen = 0, set()
    for i, sentence in enumerate(sentences):
        sid, start, end = sentence.get("sentence_id"), sentence.get("start_char"), sentence.get("end_char")
        if not isinstance(sid, str) or not sid: errors.append(f"sentence[{i}] has an empty sentence_id")
        elif sid in seen: errors.append(f"duplicate sentence_id: {sid}")
        else: seen.add(sid)
        if sentence.get("sentence_index") != i: errors.append(f"sentence[{i}] has a non-sequential sentence_index")
        if (not isinstance(start, int) or isinstance(start, bool) or
            not isinstance(end, int) or isinstance(end, bool)):
            errors.append(f"sentence[{i}] offsets must be integers"); continue
        if start < 0 or end <= start or end > len(raw):
            errors.append(f"sentence[{i}] offset range is invalid"); continue
        if start < previous_end: errors.append(f"sentence[{i}] overlaps or is out of order")
        if raw[start:end] != sentence.get("text"):
            errors.append(f"sentence[{i}] text does not match raw_text slice")
        previous_end = end
    return errors

def validate_editing_history(history: list[dict[str, Any]]) -> list[str]:
    """Validate unique IDs, a single root, ordered parent links, acyclic lineage and time."""
    errors = []
    if not isinstance(history, list): return ["editing_history must be an array"]
    if not history: return errors
    ids = {}
    for i, v in enumerate(history):
        vid = v.get("version_id")
        if not isinstance(vid, str) or not vid: errors.append(f"version[{i}] has an empty version_id")
        elif vid in ids: errors.append(f"duplicate version_id: {vid}")
        else: ids[vid] = i
        if not re.fullmatch(r"[a-fA-F0-9]{64}", v.get("text_sha256", "")):
            errors.append(f"version[{i}] has an invalid text_sha256")
    roots = [v for v in history if v.get("parent_version_id") is None]
    if len(roots) != 1: errors.append(f"history must have exactly one root version; found {len(roots)}")
    for i, v in enumerate(history):
        parent = v.get("parent_version_id")
        if parent is None: continue
        if parent not in ids: errors.append(f"version[{i}] references missing parent: {parent}")
        elif ids[parent] >= i: errors.append(f"version[{i}] parent must appear before child: {parent}")
    parent_map = {v.get("version_id"): v.get("parent_version_id") for v in history}
    for vid in parent_map:
        seen, cursor = set(), vid
        while cursor is not None and cursor in parent_map:
            if cursor in seen:
                errors.append(f"cycle detected at version_id: {cursor}"); break
            seen.add(cursor); cursor = parent_map[cursor]
    for i, v in enumerate(history):
        parent = v.get("parent_version_id")
        if parent not in ids: continue
        pt, ct = history[ids[parent]].get("created_at_utc"), v.get("created_at_utc")
        if pt and ct:
            try:
                pdt = datetime.fromisoformat(pt.replace("Z", "+00:00"))
                cdt = datetime.fromisoformat(ct.replace("Z", "+00:00"))
                if pdt.tzinfo is None or cdt.tzinfo is None:
                    errors.append(f"version[{i}] timestamps must include a timezone")
                elif pdt.astimezone(timezone.utc) > cdt.astimezone(timezone.utc):
                    errors.append(f"version[{i}] timestamp precedes its parent")
            except (AttributeError, TypeError, ValueError):
                errors.append(f"version[{i}] has an invalid timestamp")
    return errors

def normalize_for_exact_match(text: str) -> str:
    """Comparison-only normalization; never overwrites immutable raw_text."""
    return re.sub(r"\s+", " ", unicodedata.normalize("NFC", text).casefold()).strip()

def find_duplicate_candidates(records: list[dict[str, Any]], near_threshold: float = 0.88):
    """Return review candidates only. Never auto-merge or delete source records."""
    exact, near = [], []
    values = [(r["document_id"], normalize_for_exact_match(r["raw_text"])) for r in records]
    for i, (left_id, left) in enumerate(values):
        if not left: continue
        for right_id, right in values[i + 1:]:
            if not right: continue
            if left == right: exact.append((left_id, right_id, 1.0)); continue
            score = SequenceMatcher(None, left, right, autojunk=False).ratio()
            if score >= near_threshold: near.append((left_id, right_id, round(score, 4)))
    return {"exact": exact, "near": near}

def assign_group_splits(records: list[dict[str, Any]], seed: str = "lexora-synthetic-v1",
                        challenge_groups: set[str] | None = None) -> dict[str, str]:
    """Deterministic group assignment; approximate ratios are by group count, not rows."""
    raw_groups = [r.get("group_id") for r in records]
    if any(not isinstance(g, str) or not g for g in raw_groups):
        raise ValueError("every record must have a non-empty group_id")
    groups, challenge_groups = sorted(set(raw_groups)), challenge_groups or set()
    unknown = challenge_groups.difference(groups)
    if unknown: raise ValueError(f"challenge_groups not present in records: {sorted(unknown)}")
    result = {}
    for group in groups:
        if group in challenge_groups: result[group] = "test_challenge"; continue
        bucket = int(hashlib.sha256(f"{seed}:{group}".encode()).hexdigest()[:8], 16) % 100
        result[group] = "train" if bucket < 70 else "validation" if bucket < 85 else "test_in_distribution"
    return result

def apply_group_splits(records: list[dict[str, Any]], seed: str = "lexora-synthetic-v1",
                       challenge_groups: set[str] | None = None):
    assignments = assign_group_splits(records, seed, challenge_groups)
    return [{**r, "split": assignments[r["group_id"]]} for r in records]

def validate_group_split(records: list[dict[str, Any]]) -> list[str]:
    errors, group_splits, pair_groups, pair_splits = [], {}, {}, {}
    allowed = {"train", "validation", "test_in_distribution", "test_challenge", "unassigned"}
    for r in records:
        gid, split, pair = r.get("group_id"), r.get("split"), r.get("pair_id")
        if not gid: errors.append(f"{r.get('document_id', '<unknown>')} has no group_id"); continue
        if split not in allowed: errors.append(f"{r.get('document_id', '<unknown>')} has invalid split")
        group_splits.setdefault(gid, set()).add(split)
        if pair:
            pair_groups.setdefault(pair, set()).add(gid); pair_splits.setdefault(pair, set()).add(split)
    for gid, splits in group_splits.items():
        if len(splits) > 1: errors.append(f"group_id {gid} crosses splits: {sorted(splits)}")
    for pair, groups in pair_groups.items():
        if len(groups) > 1: errors.append(f"pair_id {pair} spans multiple group_id values: {sorted(groups)}")
        if len(pair_splits[pair]) > 1: errors.append(f"pair_id {pair} crosses splits: {sorted(pair_splits[pair])}")
    return errors

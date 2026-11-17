from __future__ import annotations
import copy, hashlib, json, sys, unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts"))
from synthetic_dataset_checks import (SCHEMA_PATH, apply_group_splits, find_duplicate_candidates,
    load_schema, validate_editing_history, validate_group_split, validate_record_schema,
    validate_sentence_offsets)
FIXTURES = Path(__file__).parent / "fixtures"
def record(): return json.loads((FIXTURES / "valid_document.json").read_text(encoding="utf-8"))
def sha(text): return hashlib.sha256(text.encode("utf-8")).hexdigest()

class SchemaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): cls.schema = load_schema(SCHEMA_PATH)
    def test_schema_draft_2020_12(self):
        self.assertEqual(self.schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
    def test_valid_fixture(self): self.assertEqual(validate_record_schema(record(), self.schema), [])
    def test_invalid_mutations(self):
        cases = json.loads((FIXTURES / "invalid_documents.json").read_text())
        for case in cases:
            with self.subTest(case=case["case_id"]):
                r, m = record(), case["mutation"]
                if m == "remove_required_group_id": r.pop("group_id")
                elif m == "add_unrecognized_top_level_property": r["unexpected"] = True
                elif m == "set_document_label_to_STYLE_GUESS": r["document_label"] = "STYLE_GUESS"
                elif m == "set_raw_text_to_empty_string": r["raw_text"] = ""
                elif m == "set_raw_text_sha256_to_not-a-hash": r["raw_text_sha256"] = "not-a-hash"
                self.assertTrue(validate_record_schema(r, self.schema))
    def test_nested_unknown_property(self):
        r = record(); r["source"]["unapproved_field"] = "nope"
        self.assertTrue(validate_record_schema(r, self.schema))

class OffsetTests(unittest.TestCase):
    def test_unicode_combining_emoji_crlf_tabs(self):
        r, raw = record(), "AI 🤖 memproses e\u0301jaan.\r\nBaris kedua!\tSelesai."
        parts, cursor = ["AI 🤖 memproses e\u0301jaan.", "Baris kedua!", "Selesai."], 0
        r["raw_text"], r["sentences"] = raw, []
        for i, part in enumerate(parts):
            start = raw.index(part, cursor); end = start + len(part)
            r["sentences"].append({"sentence_id":f"s{i}","sentence_index":i,
                "start_char":start,"end_char":end,"text":part}); cursor = end
        self.assertEqual(validate_sentence_offsets(r), [])
        self.assertEqual(len("e\u0301"), 2); self.assertEqual(len("🤖"), 1)
    def test_mismatch(self):
        r=record(); r["sentences"][0]["text"]="Saya belajar CSS."
        self.assertIn("sentence[0] text does not match raw_text slice", validate_sentence_offsets(r))
    def test_out_of_range(self):
        r=record(); r["sentences"][0]["end_char"]=len(r["raw_text"])+1
        self.assertIn("sentence[0] offset range is invalid", validate_sentence_offsets(r))
    def test_overlap(self):
        r=record(); r["raw_text"]="Satu. Dua."
        r["sentences"]=[{"sentence_id":"s1","sentence_index":0,"start_char":0,"end_char":5,"text":"Satu."},
          {"sentence_id":"s2","sentence_index":1,"start_char":4,"end_char":10,"text":". Dua."}]
        self.assertTrue(any("overlaps" in e for e in validate_sentence_offsets(r)))
    def test_empty_text_schema_rejection(self):
        r=record(); r["raw_text"]=""; r["sentences"]=[]
        self.assertTrue(validate_record_schema(r))

class LineageTests(unittest.TestCase):
    def setUp(self):
        self.history=[
          {"version_id":"v1","parent_version_id":None,"actor_type":"AI","action":"GENERATE","text_sha256":sha("draft"),"created_at_utc":"2026-01-01T00:00:00Z"},
          {"version_id":"v2","parent_version_id":"v1","actor_type":"HUMAN","action":"EDIT","text_sha256":sha("revised"),"created_at_utc":"2026-01-01T00:01:00Z"}]
    def test_valid_lineage(self): self.assertEqual(validate_editing_history(self.history),[])
    def test_missing_parent(self):
        h=copy.deepcopy(self.history); h[1]["parent_version_id"]="missing"
        self.assertTrue(any("missing parent" in e for e in validate_editing_history(h)))
    def test_duplicate_id(self):
        h=copy.deepcopy(self.history); h[1]["version_id"]="v1"
        self.assertTrue(any("duplicate version_id" in e for e in validate_editing_history(h)))
    def test_cycle(self):
        h=[{"version_id":"v1","parent_version_id":"v2","text_sha256":sha("a")},
           {"version_id":"v2","parent_version_id":"v1","text_sha256":sha("b")}]
        self.assertTrue(any("cycle detected" in e for e in validate_editing_history(h)))
    def test_parent_order(self):
        h=copy.deepcopy(self.history); h.reverse()
        self.assertTrue(any("parent must appear before child" in e for e in validate_editing_history(h)))
    def test_timestamp_order_and_offsets(self):
        h=copy.deepcopy(self.history); h[0]["created_at_utc"]="2026-01-01T02:00:00+02:00"
        h[1]["created_at_utc"]="2025-12-31T23:59:00Z"
        self.assertTrue(any("timestamp precedes" in e for e in validate_editing_history(h)))
    def test_timestamp_cannot_precede_parent(self):
        h=copy.deepcopy(self.history); h[1]["created_at_utc"]="2025-12-31T23:59:00Z"
        self.assertTrue(any("timestamp precedes" in e for e in validate_editing_history(h)))
    def test_empty_history(self): self.assertEqual(validate_editing_history([]),[])

class DedupTests(unittest.TestCase):
    def test_exact_and_normalized_exact(self):
        r=[{"document_id":"a","raw_text":"Belajar AI\nitu menarik."},
           {"document_id":"b","raw_text":"  BELAJAR ai itu menarik.  "}]
        self.assertEqual([(x[0],x[1]) for x in find_duplicate_candidates(r)["exact"]],[("a","b")])
    def test_near_is_candidate_not_merge(self):
        r=[{"document_id":"a","raw_text":"Saya belajar bahasa Indonesia dengan tekun."},
           {"document_id":"b","raw_text":"Saya belajar bahasa Indonesia dengan sungguh tekun."}]
        result=find_duplicate_candidates(r,0.88)
        self.assertFalse(result["exact"]); self.assertTrue(result["near"]); self.assertEqual(len(r),2)
    def test_shared_boilerplate_not_enough(self):
        r=[{"document_id":"a","raw_text":"Kesimpulan: teknologi membantu pendidikan. Siswa perlu memahami konsep."},
           {"document_id":"b","raw_text":"Kesimpulan: teknologi membantu pendidikan. Guru perlu merancang evaluasi."}]
        result=find_duplicate_candidates(r,0.95)
        self.assertFalse(result["exact"]); self.assertFalse(result["near"])
    def test_unicode_canonical_equivalence(self):
        r=[{"document_id":"a","raw_text":"Kafe\u0301 itu nyaman."},{"document_id":"b","raw_text":"Kafé itu nyaman."}]
        self.assertEqual(len(find_duplicate_candidates(r)["exact"]),1)

class SplitTests(unittest.TestCase):
    def test_group_and_pair_stay_together(self):
        r=[{"document_id":"a","group_id":"g1","pair_id":"p1","split":"unassigned"},
           {"document_id":"b","group_id":"g1","pair_id":"p1","split":"unassigned"},
           {"document_id":"c","group_id":"g2","pair_id":None,"split":"unassigned"}]
        out=apply_group_splits(r); self.assertEqual(out[0]["split"],out[1]["split"])
        self.assertEqual(validate_group_split(out),[])
    def test_group_leakage_rejected(self):
        r=[{"document_id":"a","group_id":"g1","split":"train"},{"document_id":"b","group_id":"g1","split":"test_in_distribution"}]
        self.assertTrue(any("crosses splits" in e for e in validate_group_split(r)))
    def test_pair_across_groups_rejected(self):
        r=[{"document_id":"a","group_id":"g1","pair_id":"p1","split":"train"},
           {"document_id":"b","group_id":"g2","pair_id":"p1","split":"train"}]
        self.assertTrue(any("spans multiple group_id" in e for e in validate_group_split(r)))
    def test_missing_group_rejected(self):
        for r in [[{"document_id":"a","group_id":"","split":"unassigned"}],[{"document_id":"a","split":"unassigned"}]]:
            with self.assertRaises(ValueError): apply_group_splits(r)
    def test_challenge_holdout(self):
        r=[{"document_id":"a","group_id":"gc","pair_id":"p1"},{"document_id":"b","group_id":"gc","pair_id":"p1"}]
        out=apply_group_splits(r,challenge_groups={"gc"})
        self.assertEqual({x["split"] for x in out},{"test_challenge"})
        self.assertEqual(validate_group_split(out),[])
    def test_deterministic(self):
        r=[{"document_id":f"d{i}","group_id":f"g{i}"} for i in range(20)]
        self.assertEqual(apply_group_splits(r),apply_group_splits(r))

if __name__ == "__main__": unittest.main(verbosity=2)

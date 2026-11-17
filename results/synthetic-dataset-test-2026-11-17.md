# Synthetic Dataset Procedure Test Run

- **Tanggal:** 2026-11-17
- **Scope:** synthetic fixtures only
- **Environment:** Python 3.13.5; jsonschema 4.26.0
- **Command:** python -m unittest discover -s tests/synthetic_dataset -p 'test_*.py' -v
- **Local result:** 27 tests passed, 0 failed, 0 skipped

## Results by area

| Area | Test cases | Result |
|---|---:|---|
| JSON Schema Draft 2020-12 | 4 | PASS |
| Sentence offsets | 5 | PASS |
| Editing history and lineage | 8 | PASS |
| Exact/near deduplication | 4 | PASS |
| Group-based split | 6 | PASS |
| **Total** | **27** | **PASS** |

## Coverage notes

- Valid record accepted; missing required field, unknown property, invalid enum, empty raw text, and malformed hash rejected.
- Sentence offsets checked against exact source substrings, including combining marks, emoji, CRLF, tabs, invalid bounds, overlap, and empty text.
- Version lineage checked for missing parent, duplicate ID, cycles, parent ordering, timestamp ordering, and empty history.
- Exact and normalized-exact duplicates detected. Near-duplicates are returned for human review only; no records are merged or deleted.
- Group and pair integrity checked across train, validation, in-distribution test, and explicit challenge holdout.

## Interpretation and limitations

This is a local synthetic-procedure test record. It does not validate real-world provenance, consent, license rights, annotation truth, model performance, or dataset representativeness.

The near-duplicate threshold 0.88 is a test parameter, not a production threshold. The deterministic hash-bucket split approximates 70/15/15 by group count; it does not guarantee document/class stratification or exact ratios. Challenge groups require explicit holdout designation.

The GitHub Actions workflow was added at .github/workflows/synthetic-dataset-tests.yml. No GitHub Actions run/status was available when this report was written, so CI verification remains pending. The committed test files were read back from GitHub after publication; local execution and remote CI execution are reported separately.

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

GitHub Actions workflow: .github/workflows/synthetic-dataset-tests.yml. Remote CI run #2 completed successfully on commit 500b11be6c34588fd72d1e9f6fff27e95533b468 (run ID 44026691695). The job installed jsonschema 4.26.0, ran the committed unittest suite on Python 3.12.16, and reported: Ran 27 tests; OK. Run URL: https://github.com/Fajriansyah21/Website-AI-Ditector/actions/runs/44026691695. A prior run #1 also passed on commit 0cb5a3d4d1ed9af2f72fc9053184f50e8e2954c0.

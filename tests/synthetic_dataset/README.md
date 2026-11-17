# Synthetic Dataset Procedure Tests

Status: executable harness for synthetic fixtures only.

## Coverage
1. JSON Schema Draft 2020-12 validation and invalid-record rejection.
2. Sentence offsets with zero-based, end-exclusive Unicode code-point indices.
3. Immutable editing-version lineage, parent links, cycles, and timestamp order.
4. Exact, normalized-exact, and near-duplicate candidate detection.
5. Group-based split integrity for group IDs and paired records, including explicit challenge holdouts.

## Run from repository root

    python -m pip install -r requirements-test.txt
    python -m unittest discover -s tests/synthetic_dataset -p 'test_*.py' -v

Fixtures are artificial. No participant text, public corpora, or real model outputs are used.

## Limitations
- JSON Schema checks structure; semantic checks validate offsets, lineage, and split integrity.
- Near-duplicate detection only creates review candidates. It never auto-merges records.
- Similarity threshold 0.88 is a test parameter, not an approved production threshold. Calibrate it on a reviewed validation sample before real-data use.
- Hash-bucket split assignment approximates 70/15/15 by group count, not by document count or class. It does not replace stratified research design. Challenge groups must be explicitly held out.
- The harness does not validate consent, license rights, provenance truth, annotation correctness, or model quality.
- Passing synthetic tests does not independently authorize pilot collection or model training.

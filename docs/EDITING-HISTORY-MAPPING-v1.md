# Editing History Template to Dataset Export Mapping v1

**Purpose:** define the explicit conversion from the collection template to the dataset record JSON export. The template is an intake worksheet, not a complete dataset record.

## Field mapping

| Intake template | Dataset export | Rule |
|---|---|---|
| template_version | Not exported | Identifies the worksheet version only |
| document_id | document_id | Copy unchanged |
| group_id | group_id | Copy unchanged |
| pair_id | pair_id | Copy unchanged, including null |
| versions[] | editing_history[] | Copy each version object; preserve order and parent links |
| consent_or_license_review_id | source.usage_review_id | Link to the source/consent review record |
| history_completeness | provenance.history_completeness | Copy unchanged |
| history_notes | provenance.history_notes | Copy unchanged |

## Per-version fields

All version fields are retained in editing_history[], including provenance_evidence[] and reviewer_note. The Dataset Record JSON Schema explicitly allows these fields. Evidence references must point to controlled audit artifacts; do not embed private participant identity or unrestricted raw evidence in the export.

Before export:
- Replace all instructional placeholders with actual values.
- created_at_utc must be a valid ISO 8601 date-time with timezone.
- prompt_sha256 and text_sha256 must be 64-character hexadecimal SHA-256 digests when present/required.
- Each parent_version_id must reference an earlier version in the same document history, or be null for the single root.
- Preserve the exact text hash for each immutable version.
- Do not invent missing provenance. Use UNKNOWN/PARTIAL and evidence notes where appropriate.

## Verification

The mapping is exercised by tests/synthetic_dataset/test_synthetic_pipeline.py in test_editing_template_maps_to_export_record. The test fills template placeholders with synthetic values, maps the fields above, validates the exported record against schemas/dataset-records-v1.schema.json, and checks editing lineage.

This mapping test verifies structure and conversion only. It does not validate the truth of evidence, consent, license rights, or authorship labels.

# Privacy and Legal Readiness — Lexora

- **Tanggal:** 2026-11-17
- **Status:** Requirements recorded; legal applicability and provider contracts must be reviewed before production.
- **Scope:** Indonesian launch baseline for user text, uploaded documents, account data, AI processing, payments, notifications, and potential access by children.

## 1. Legal and regulatory references

1. **UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP).** Relevant areas include lawful bases and transparency, data-subject rights, DPIA for high-risk processing, breach notification, and cross-border transfers.
2. **PP No. 17 Tahun 2025 (PP TUNAS).** Requires electronic system providers to assess product/service/feature risks to children and apply protections appropriate to the risk and age classification.
3. **Permenkomdigi No. 9 Tahun 2026.** Implements PP TUNAS and describes risk classification, self-assessment, mitigation, verification, reporting, and child-friendly features.

This document is a product-design checklist, not a legal opinion. A qualified Indonesian privacy/legal reviewer must confirm applicability, controller/processor roles, registration obligations, age classification, lawful bases, and final notices before launch.

## 2. Data inventory and purpose limitation

| Data | Purpose | Baseline handling |
|---|---|---|
| Account identity and authentication | Login, account security, billing | Store minimum identity fields; protect credentials |
| User-submitted text and uploaded documents | Requested Detector/Humanizer processing | Process only for requested service; no default training use |
| Humanizer style samples and profiles | Create user-requested personal style profile | Separate profile storage, consent notice, retention/deletion controls |
| Detector/Humanizer results | Show, download, and optionally save results | No automatic training/research reuse |
| Credit ledger and payment records | Balance, billing, fraud prevention, reconciliation | Immutable financial/audit records; retention exceptions documented |
| Support tickets | Resolve support requests | Do not request raw text attachments on MVP |
| Logs and telemetry | Reliability and security | Metadata only by default; no raw text or document content |

## 3. Privacy notice and consent

Before text processing, the notice should explain:
- Who controls the data and how to contact the controller.
- Processing purposes and lawful basis for each purpose.
- Data categories collected and whether text/documents may contain personal data.
- AI, payment, email, storage, analytics, and other processors/subprocessors.
- Known processing locations and cross-border transfers.
- Retention periods or the criteria used to determine them.
- User rights and how to submit a request.
- Whether automated analysis is performed and its limitations.

Consent must be separated by purpose. Service processing consent/notice must not be bundled with marketing, research, or model-training opt-in. Record the notice version, selection, timestamp, and context.

## 4. User content and model training

- Do not use submitted text, documents, samples, profiles, or results for model training/fine-tuning by default.
- Optional research/training use requires a separate, specific, revocable opt-in.
- Do not make optional consent a condition of using the service.
- Withdrawal must stop future use and trigger handling of derived datasets according to the disclosed policy.
- Maintain provenance, pseudonymization, license/consent evidence, and a withdrawal propagation procedure.
- Production data must not enter a training pipeline merely because it is present in storage or logs.

## 5. Third-party processors and cross-border transfer

Maintain a processor/subprocessor register with:
- Provider, service, purpose, data categories, and processing region.
- Retention and deletion behavior.
- Whether prompts/responses may be used for provider training or abuse monitoring.
- DPA/contract and security controls.
- Transfer basis and safeguards for any processing outside Indonesia.
- A documented decision to allow or block production data.

A provider must remain blocked from production until legal/privacy review confirms that the transfer and processing arrangement is acceptable. Do not assume that a provider's global API region means data stays in Indonesia.

## 6. Data-subject requests

Provide a request workflow for applicable rights, including:
- Access/copy.
- Correction.
- Deletion.
- Withdrawal of optional consent.
- Objection to processing/automated decisions where applicable.

Every request needs an ID, identity verification proportional to risk, status, owner, deadline, outcome, and audit trail. Explain exceptions for legal retention, financial records, backups, and third-party processors. Do not promise instantaneous deletion from every backup/provider unless it has been verified.

## 7. Incident response

Maintain an incident response plan covering detection, containment, investigation, evidence preservation, recovery, and communications. Where a personal-data protection failure meets the statutory notification criteria, prepare the required written notification within the applicable statutory deadline, including the 3 x 24 hour period under UU PDP Article 46. Do not put raw text into general incident logs.

## 8. Children and age-appropriate design

Before launch in Indonesia:
1. Perform the required self-assessment for whether the product, service, or feature may be used/accessed by children.
2. Determine risk classification and minimum age/age-assurance requirements from the applicable rules.
3. Assess text upload, profiling, AI-generated analysis, advertising, and payment/reward features for child-specific risks.
4. Implement appropriate age, consent, reporting, privacy, and safety controls.
5. Record assessment evidence and re-run it when product functionality changes.

Do not assume an adult-focused marketing position or an 18+ checkbox alone removes all PP TUNAS obligations. The final age classification and controls require legal review.

## 9. DPIA and high-risk processing

Before production, assess whether Lexora's processing meets high-risk criteria under UU PDP, including use of new technology, systematic evaluation/profiling, large-scale processing, or sensitive data. Complete a DPIA where required, document mitigations and residual risks, assign accountable owners, and repeat the assessment after material model/provider/data-flow changes.

## 10. Launch blockers

- [ ] Legal review of controller/processor roles and lawful bases.
- [ ] Privacy Notice and separate consent wording approved.
- [ ] Processor/subprocessor register and DPA completed.
- [ ] Cross-border transfer review completed for every provider.
- [ ] Retention/deletion matrix covers database, object storage, cache, temp files, backups, logs, and provider systems.
- [ ] Data-subject request workflow tested.
- [ ] Child protection self-assessment and age classification completed.
- [ ] DPIA completed if required.
- [ ] Incident response plan and notification contacts tested.
- [ ] Provider data-use settings verified; no default training use of submitted content.

## 11. Official references

- [UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi — JDIH Komdigi](https://jdih.komdigi.go.id/produk_hukum/view/id/832).
- [PP No. 17 Tahun 2025 tentang Tata Kelola PSE dalam Pelindungan Anak — JDIH Komdigi](https://jdih.komdigi.go.id/produk_hukum/view/id/965).
- [Permenkomdigi No. 9 Tahun 2026 — JDIH Komdigi](https://jdih.komdigi.go.id/produk_hukum/abstrak/547).
- [Komdigi: Implementasi PP TUNAS dan Permenkomdigi No. 9 Tahun 2026](https://portal.komdigi.go.id/kanal-publik/berita-kini/10066).
- [UU PDP Pasal 46: pemberitahuan kegagalan pelindungan data pribadi](https://jdih.komdigi.go.id/produk_hukum/view/id/832).
- [UU PDP Pasal 56: transfer data pribadi ke luar Indonesia](https://jdih.komdigi.go.id/produk_hukum/view/id/832).

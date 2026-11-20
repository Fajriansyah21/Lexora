# Task Plan: AI Text Detector (M3)

- **Tanggal:** 2026-11-20
- **Status:** Planning Approved; implementation blocked by M2 mandatory review gate
- **Milestone:** Stage 7, M3
- **Parent mandate:** [Stage 7 Implementation Mandate](../../docs/STAGE-7-IMPLEMENTATION-MANDATE-2026-11-18.md)
- **Architecture:** Option A — separate Web/BFF, Node.js Worker, and Python FastAPI Detector
- **Planning decisions:** Private object storage; mock credit reservation port; mock-first inference; backend pipeline only, no final UI

## 1. Objective

Membangun dan membuktikan pipeline AI Text Detector secara end-to-end melalui Next.js Web/BFF, PostgreSQL, private S3-compatible object storage, Redis/BullMQ, Node.js Worker, dan Python FastAPI inference service.

M3 berfokus pada integrasi backend dan perilaku pipeline. Mock inference membuktikan kontrak serta alur sistem, bukan akurasi atau kualitas model AI.

## 2. Approval and implementation lock

Task plan ini telah disetujui sebagai dokumen perencanaan. Persetujuan ini **bukan** izin memulai implementasi.

M3 implementation hanya boleh dimulai setelah:
1. Seluruh acceptance criteria M2 yang berlaku memiliki bukti verifikasi.
2. Migration, autentikasi, session, protected API, authorization baseline, API foundation, dan security baseline M2 telah diverifikasi sesuai task plan induk.
3. M2 mandatory review gate diselesaikan.
4. Project owner secara eksplisit menyetujui perpindahan M2 ke M3.

Sebelum seluruh syarat tersebut terpenuhi, pekerjaan M3 dibatasi pada perencanaan dan klarifikasi dokumentasi. Dilarang membuat kode M3, memasang dependency M3, membuat service, menjalankan migration M3, atau mengubah konfigurasi runtime M3.

## 3. Confirmed decisions

| Area | Decision | Boundary |
|---|---|---|
| Architecture | Option A, full separation | Web/BFF, Worker, dan Detector API adalah proses terpisah |
| Database | PostgreSQL 18 + Drizzle | PostgreSQL adalah source of truth untuk job dan hasil |
| Queue | Redis 8 + BullMQ | Transport antrean saja, bukan source of truth |
| Storage | Private S3-compatible object storage | Provider dan region produksi belum dipilih |
| Credits | Mock reservation port | Tidak membuat credit ledger atau saldo produksi |
| Inference | Mock-first | Model nyata dan training tidak termasuk implementasi M3 |
| UI | Pipeline only | Tidak ada UI Detector final pada M3 |
| Runtime | Node.js 26 dan Python 3.13 | Mengikuti baseline Stage 7 |

## 4. Architecture boundaries

- `apps/web`: Next.js UI/BFF, authentication integration, request validation, job creation, status/result/report API.
- `apps/worker`: Node.js BullMQ consumer, job lifecycle, storage access, inference client, persistence, retry, cancellation.
- `apps/detector-api`: Python FastAPI inference service, internal-only.
- PostgreSQL: authoritative job state, ownership, analysis metadata, segment results, and artifact references.
- Redis/BullMQ: queue transport containing job ID, trace ID, and non-sensitive routing metadata only.
- Private object storage: source input and generated report/result artifacts, accessed using scoped service credentials and short-lived signed URLs where appropriate.

Worker and Detector API must not be publicly exposed. Raw text must not appear in queue payloads, URLs, general logs, analytics, or telemetry. Service-to-service calls must authenticate and validate payloads.

## 5. Scope and workstreams

### M3.1 — Documentation and implementation readiness

Deliverables:
- This approved M3 task plan.
- M2 dependency checklist and explicit implementation lock.
- Resolved M2 task numbering references.
- API/export boundary reflected in the plan.
- M3 risk and unresolved-decision register.

Acceptance:
- [ ] M3 scope matches Stage 7 Mandate and System Design.
- [ ] M2 dependencies are explicit.
- [ ] No task implies M3 implementation can begin before M2 approval.
- [ ] M3 decisions do not silently select production storage provider/region or a real model.

### M3.2 — Detector contracts and API design

Deliverables:
- Versioned request/response contracts for Web/BFF, Worker, and FastAPI.
- Zod schemas for TypeScript boundaries and matching Python validation models.
- BullMQ event/payload contract.
- Job state machine and transition rules.
- Error catalogue and idempotency behavior.
- Canonical result/report data contract.

API surface aligned to `plan/API-CONTRACTS.md`:
- `POST /api/v1/detector/estimate`
- `POST /api/v1/detector/jobs`
- `GET /api/v1/detector/jobs/{jobId}`
- `GET /api/v1/detector/jobs/{jobId}/result`
- `GET /api/v1/detector/jobs/{jobId}/report?format=txt|docx|pdf`
- `POST /api/v1/jobs/{jobId}/cancel`

Acceptance:
- [ ] Every endpoint has request, response, authorization, and error contracts.
- [ ] Queue messages contain only opaque job ID and non-sensitive metadata.
- [ ] Idempotency and duplicate-request behavior are specified.
- [ ] Result and report schemas preserve sentence order and source references.
- [ ] TypeScript and Python contract fixtures agree.

Gate: contracts and job state transitions must be reviewed before implementation workstreams depend on them.

### M3.3 — Detector database foundation

Deliverables:
- Drizzle schema and reviewed migrations for Detector job and result data.
- Repository/query layer separated from route handlers.
- Ownership constraints and access patterns.
- Atomic job state transitions and idempotency constraints.
- Indexes for job lookup, user ownership, status, and processing/reconciliation needs.

Candidate logical entities (physical schema to be finalized during implementation design):
- jobs, job_attempts, job_events
- detector_analyses, detector_segments
- detector_model_versions
- stored_artifacts and required file/object metadata

Acceptance:
- [ ] Schema and migration match approved contracts.
- [ ] Job ownership is enforced server-side.
- [ ] State transitions are atomic and invalid transitions are rejected.
- [ ] Duplicate idempotency keys cannot create duplicate jobs.
- [ ] Raw text is not placed in general-purpose metadata columns.
- [ ] Migration is tested against a development database after the M2 gate.

### M3.4 — Private object storage adapter

Deliverables:
- S3-compatible storage interface for put/get/delete/head operations.
- Private bucket/container configuration.
- Opaque object-key convention.
- Scoped service credentials and short-lived signed access where needed.
- Encryption and lifecycle configuration supported by the selected test environment.
- Isolated integration test storage.

Acceptance:
- [ ] Public access is disabled.
- [ ] Object keys contain no user text or direct personal identifiers.
- [ ] Access is authorized and scoped.
- [ ] Signed URLs, if used, expire within the configured short lifetime.
- [ ] Upload, read, and deletion behavior is tested.
- [ ] Storage failures do not incorrectly mark jobs completed.
- [ ] Logs contain object identifiers/metadata only, not content.

Provider/region boundary:
- DEC-186 establishes private S3-compatible storage, but production provider and region remain conditional on cost, availability, encryption, deletion, and cross-border/privacy review.
- M3 may use an isolated S3-compatible development/test service or approved test account.
- Do not provision or commit to a production provider/region without separate approval.

### M3.5 — Python FastAPI Detector service

Deliverables:
- `apps/detector-api` Python service.
- Internal inference endpoint and health/readiness endpoints.
- Request/response validation.
- Mock inference adapter with deterministic fixtures.
- Internal service authentication.
- Model/config version metadata fields, explicitly identifying mock output.

Mock scenarios:
- HUMAN, AI, MIXED, and UNCERTAIN.
- Indonesian, English, code-switch, and unsupported dominant language.
- Short/context-poor sentence.
- Insufficient or conflicting evidence.
- Timeout, malformed output, and inference failure.

Acceptance:
- [ ] Service is reachable only from the private application network.
- [ ] Invalid requests are rejected.
- [ ] Responses conform to the shared contract.
- [ ] Every result records mock model and config version identifiers.
- [ ] Mock results are never represented as real-model findings.
- [ ] Timeout and failure semantics are testable by Worker.

### M3.6 — Node.js Worker and BullMQ pipeline

Deliverables:
- `apps/worker` workspace application.
- Redis/BullMQ queue and consumer.
- Database-backed job state transitions.
- Input retrieval from private object storage.
- Authenticated FastAPI client.
- Result persistence and artifact handling.
- Retry, cancellation, idempotency, and graceful shutdown.

Processing rules:
- Retry only transient failures, maximum two retries with exponential backoff and jitter.
- Preserve the same job idempotency identity across retries.
- Waiting cancellation transitions to Cancelled and triggers reservation release.
- Processing cancellation is best-effort; terminal state follows confirmed worker/service outcome.
- Duplicate delivery or callback must not create duplicate result or duplicate settlement.
- PostgreSQL remains authoritative even if Redis loses/replays a message.

Acceptance:
- [ ] Worker consumes a valid job and retrieves its input from storage.
- [ ] Worker invokes the internal FastAPI service.
- [ ] Worker persists structured results and updates job state.
- [ ] Retry and duplicate delivery are idempotent.
- [ ] Cancellation races preserve a valid terminal state.
- [ ] Queue payload contains no raw text or signed storage URL.
- [ ] Graceful shutdown does not leave jobs in an unresolvable state.

### M3.7 — Credit reservation mock port

Deliverables:
- Credit reservation interface/port.
- Deterministic mock implementation for tests.
- Mock estimate, reserve, settle, and release operations.
- Idempotency and failure-path tests.

Acceptance:
- [ ] Reservation is invoked before queue publication.
- [ ] Queue publication failure causes the reservation to be released.
- [ ] Processing success settles through the mock port.
- [ ] Terminal failure/cancellation releases the reservation according to the agreed job lifecycle.
- [ ] Repeated calls do not duplicate effects.
- [ ] Worker and Detector depend on the port, not a future M5 ledger implementation.

Out of scope:
- No production balance, credit lots, ledger entries, payment, top-up, expiry, or rewarded-ad logic.
- Mock state is test infrastructure and must never be presented as a real account balance.

### M3.8 — Detector result and report generation

Deliverables:
- Canonical analysis result with overall label, summary, warnings, and sentence-level segments.
- Traceable evidence metadata limited to signals actually computed by the inference implementation.
- Model/config version, detected language, analysis timestamp, and processing status.
- Server-side report renderer for TXT, DOCX, and PDF.
- Report endpoint contract and authorized download flow.
- Private storage of generated report artifacts where persistence is needed, with short-lived signed download access.

Report scope decision:
- **M3 includes backend report generation and delivery capability for TXT, DOCX, and PDF.** This is required to cover FR-DET-16 / AC-034 without relying on the later UI milestone.
- **M3 excludes all final user-facing Detector UI**, including download buttons, report preview layout, editor integration, and visual download states. Those belong to M6.
- Report contents must include overall label, summary, available sentence analysis, warnings/limitations, and the required non-proof disclaimer.
- The report must not show an authorship percentage or uncalibrated numeric probability.
- Report generation must consume the canonical stored result; it must not rerun inference or fabricate explanations.
- Export files are private artifacts. Do not expose public bucket URLs. Retention follows the approved product retention policy; M3 must not invent a user-facing retention promise.

Acceptance:
- [ ] TXT, DOCX, and PDF are generated from the same canonical result.
- [ ] All formats preserve required report content and sentence ordering.
- [ ] Invalid/unauthorized job access cannot retrieve a report.
- [ ] Report URLs are short-lived and scoped, if signed URLs are used.
- [ ] Report generation failure does not corrupt the analysis result or job state.
- [ ] Exported reports contain no unsupported claims or uncalibrated authorship percentage.

### M3.9 — Input validation, privacy, and security verification

Deliverables:
- Backend extended-grapheme-cluster validation consistent with Unicode 18.0.0 UAX #29.
- Maximum 20,000 clusters enforced before storage side effects, queueing, inference, or credit reservation.
- Language and unsupported-input behavior.
- Cross-user authorization tests.
- Log/telemetry redaction tests.
- Internal service authentication tests.

Acceptance:
- [ ] Exactly 20,000 clusters is accepted for subsequent validation.
- [ ] 20,001 clusters is rejected before queue, inference, or credit reservation.
- [ ] No product minimum rejects short text; insufficient evidence returns UNCERTAIN.
- [ ] Indonesian and English are supported; code-switch produces the specified warning.
- [ ] Unsupported dominant language returns UNCERTAIN/unsupported language.
- [ ] Unauthorized and cross-user access are rejected.
- [ ] No raw text, secrets, signed URLs, or document contents appear in queue/log/telemetry.
- [ ] Worker and Detector API are not publicly exposed.

### M3.10 — End-to-end integration and acceptance review

Required end-to-end flow:
1. Web authenticates and authorizes the user.
2. Web validates input and any required processing notice/basis.
3. Credit mock reserves the estimate.
4. Input is stored in private object storage.
5. Job and metadata are persisted in PostgreSQL.
6. BullMQ receives only job ID and non-sensitive metadata.
7. Worker atomically claims the job and retrieves input.
8. Worker calls FastAPI mock inference.
9. Worker validates and persists analysis output.
10. Worker settles or releases the mock reservation.
11. Report renderer produces TXT, DOCX, and PDF from the canonical result.
12. Authorized Web API returns job status, result, and report access.

Required failure and edge tests:
- Invalid input; 20,000/20,001 grapheme-cluster boundary.
- Short text and unsupported language.
- Storage unavailable or permission denied.
- Redis unavailable and duplicate queue delivery.
- FastAPI timeout, invalid response, and service unavailable.
- Worker crash/restart.
- Duplicate job request and idempotency collision.
- Cancellation before and during processing.
- Unauthorized and cross-user job/result/report access.
- Duplicate completion and reservation calls.
- Report renderer failure for each format.
- Redaction checks for logs and telemetry.

Acceptance:
- [ ] API → PostgreSQL → BullMQ → Worker → FastAPI → PostgreSQL pipeline passes using mock inference.
- [ ] Private object storage is exercised in integration tests.
- [ ] TXT, DOCX, and PDF report generation is verified.
- [ ] Job state, retry, cancellation, and idempotency are consistent.
- [ ] Security/privacy acceptance tests pass.
- [ ] M1 and M2 regression checks pass.
- [ ] Test evidence, known limitations, and blocked criteria are documented.
- [ ] Project owner approves M3 completion before M4 can begin.

## 6. Dependency map

M3 has a hard dependency on M2 approval. After the M2 gate and M3.1/M3.2 approval, M3.3, M3.4, and M3.5 can proceed in parallel. M3.6 depends on the database, storage, and inference contracts. M3.7 is integrated into job creation/processing. M3.8 depends on the canonical result contract. M3.9 applies across all components. M3.10 integrates and verifies the complete pipeline.

## 7. M2 dependency checklist

The following M2 workstreams must be completed and accepted before M3 implementation:
- [ ] M2.1 Documentation and roadmap.
- [ ] M2.2 Next.js Web Foundation.
- [ ] M2.3 PostgreSQL/Drizzle Database Foundation.
- [ ] M2.4 Versioned SQL migrations and successful development migration execution.
- [ ] M2.5 Better Auth, session management, and ownership authorization baseline.
- [ ] M2.6 API foundation and domain-service baseline.
- [ ] M2.7 Security baseline, including authentication guard, headers, CORS, and rate limiting.
- [ ] M2.8 Integration tests, regression checks, and acceptance evidence.
- [ ] M2 mandatory review gate approved by project owner.

A workstream being partially implemented or having generated files does not count as accepted without the required execution evidence.

## 8. Explicit non-scope

- Real AI model selection, model integration, training, and quality benchmark.
- Dataset pilot or collection of real user text for training.
- Production credit ledger and payment.
- Humanizer logic and provider integration.
- Final Detector UI, report preview UI, download buttons, dashboard, and editor.
- Production storage provider/region commitment before its separate review.
- Production deployment and operational go-live.
- DOCX Metadata Cleaner.

## 9. Risks and unresolved decisions

| Risk / open item | Handling |
|---|---|
| Production object storage provider/region undecided | Use isolated S3-compatible test storage; require separate approval before production provisioning |
| Real model not selected | Keep inference mock-first; model decision and benchmark are separate gates |
| Credit ledger belongs to M5 | Use mock port only; do not create production ledger schema |
| Report retention values remain TBD | Keep artifacts private; follow later approved retention policy; do not promise retention duration |
| Aggregation method not validated | Keep aggregation behind a replaceable strategy; mock fixtures must not imply a validated production method |
| Exact physical schema not yet designed | Finalize constraints/indexes during M3.3 implementation design and review migration before execution |
| File upload/extraction/OCR scope may expand M3 | Reuse only approved shared file-processing requirements; do not silently add OCR or broad file pipeline work without a scoped decision |

## 10. Mandatory review gates

1. **M2 → M3:** no M3 implementation before M2 acceptance evidence and explicit project-owner approval.
2. **M3.1 → M3.2:** approve scope, dependency, and open-decision register.
3. **M3.2 → implementation:** approve API/event contracts, job state machine, and canonical result/report schema.
4. **Migration gate:** review generated SQL and schema diff before applying any M3 migration to a shared or development database.
5. **Storage gate:** approve production provider/region and privacy/security terms separately before production use.
6. **Model gate:** real model integration requires explicit model decision and benchmark plan approval.
7. **M3 → M4:** all applicable M3 acceptance criteria verified and project owner approves the milestone transition.

## 11. Verification principles

- Distinguish **Passed**, **Failed**, and **Blocked**. A blocked test is not a pass.
- Mock integration proves orchestration and contract behavior only, not model accuracy.
- Every acceptance claim must have reproducible command/output or inspectable evidence.
- Do not change unrelated dataset research files or the seven existing design wireframes.
- Do not commit secrets, credentials, or private user text.

## 12. Related source documents

- [Active Roadmap](../ACTIVE-ROADMAP.md)
- [System Design](../SYSTEM-DESIGN.md)
- [Data Flow and Data Lifecycle](../DATA-FLOW-AND-DATA-LIFECYCLE.md)
- [Security Architecture and Threat Model](../SECURITY-ARCHITECTURE-AND-THREAT-MODEL.md)
- [API Contracts](../API-CONTRACTS.md)
- [Acceptance Criteria](../ACCEPTANCE-CRITERIA.md)
- [Acceptance Test Scenarios](../ACCEPTANCE-TEST-SCENARIOS.md)
- [AI Text Detector Plan](../AI-TEXT-DETECTOR-PLAN.md)
- [Dataset and Model Research Plan](../DATASET-AND-MODEL-RESEARCH-PLAN.md)
- [M2 Database and Backend Foundation](./2026-11-19-database-backend-foundation.md)
- [M2.5 Authentication Foundation](./2026-11-19-authentication-foundation.md)

# Lexora Security Architecture and Threat Model

- **Tanggal:** 2026-11-17
- **Status:** Threat model baseline for System Design; controls require implementation and security testing.
- **Scope:** MVP web app, background worker, Detector API, file processing, payments, credits, rewarded ads, Admin, and privacy workflows.

## 1. Security objectives

1. Protect user text, uploaded documents, profiles, and generated results from unauthorized access.
2. Prevent double-spend, duplicate payment/reward grants, and inconsistent job state.
3. Restrict privileged Admin access and preserve audit evidence.
4. Prevent malicious files, prompt injection, and model output from compromising the application.
5. Minimize data exposure to logs, analytics, queues, and external providers.
6. Preserve availability and recoverability without making unsupported privacy promises.

## 2. Trust boundaries

- Browser ↔ public web/BFF.
- Public web ↔ private database/Redis/object storage.
- Worker ↔ Detector inference service.
- Worker ↔ external Humanizer provider.
- Webhook endpoints ↔ payment provider.
- Reward verification endpoint ↔ ad provider.
- Admin Panel ↔ privileged domain operations.
- Production environment ↔ development/test environments.

All cross-boundary communication must authenticate the caller, validate the payload, and apply least privilege.

## 3. STRIDE threat register

| Asset/boundary | Threat | Impact | Required controls |
|---|---|---|---|
| User session | Credential theft, session fixation, session replay | Account takeover | Secure cookies, rotation, re-auth for sensitive actions, session revocation, CSRF controls |
| Account linking | Attacker links own OAuth identity to another account | Account takeover | Re-authenticate existing account, verify both identities, explicit confirmation, audit |
| User text/files | IDOR or cross-tenant query leak | Exposure of private text | Ownership checks in domain layer, opaque IDs, row-level access tests, private object storage |
| File upload | Malware, parser exploit, zip bomb, decompression bomb | Code execution or resource exhaustion | Quarantine, magic-byte validation, allowlist, size/time/memory limits, sandboxed parser, malware scanning |
| File extraction | SSRF through external references or URL upload | Internal network access | No remote URL ingestion in MVP; block private IP/metadata endpoints if introduced |
| Humanizer prompt | Prompt injection embedded in user text/sample | System prompt override or data exfiltration | Treat user text as untrusted content, delimit content, no tool access, fixed system policy, output validation |
| Model output | HTML/script injection or unsafe markup | XSS | Render as text, sanitize allowed markup, CSP, no unsafe HTML injection |
| Detector result | Overconfident or misleading classification | User harm/reputational harm | UNCERTAIN state, no uncalibrated percentage, limitations, benchmark gates |
| Credit ledger | Race/double-spend/duplicate settlement | Financial loss | DB transaction, row locking, unique idempotency keys, append-only ledger, reconciliation |
| Payment webhook | Forged/replayed/out-of-order callback | Fraudulent credit grant | Signature verification, amount/currency/order validation, replay protection, monotonic state transitions |
| Rewarded ad | Forged/replayed reward callback | Fraudulent credit grant | Provider SSV, server nonce/session binding, login-only reward, idempotent grant |
| Job queue | Duplicate job/retry race | Duplicate processing or charge | Job idempotency key, atomic state transition, retry classification, outbox |
| Admin Panel | Privilege escalation or insider misuse | Data exposure/financial abuse | RBAC, Admin 2FA, reasoned actions, least privilege, audit, sensitive access grant |
| Logs/telemetry | Raw text or secret leakage | Privacy breach | Structured metadata-only logs, redaction, secret scanning, access controls |
| Provider API | Data retention/training/cross-border transfer | Privacy/legal risk | Provider inventory, DPA, retention review, no-training settings, cross-border gate |
| Backup/storage | Deletion not propagated | False deletion promise | Retention matrix, deletion tasks, backup expiry disclosure, restore/deletion tests |
| Dependencies/build | Supply-chain compromise | Code execution/data breach | Lockfiles, dependency scanning, signed builds, secret scanning, CI permissions minimization |
| Child access | Inappropriate processing/design for children | Legal and safety risk | PP TUNAS self-assessment, age classification, age-appropriate controls |

## 4. File-processing security

- Accept only explicitly supported formats and validate extension, MIME type, and magic bytes.
- Reject encrypted/password-protected or malformed files when safe extraction cannot be guaranteed.
- Quarantine files before extraction.
- Run parsers in a restricted worker/container with CPU, memory, disk, and execution-time limits.
- Do not allow parsers to access the public network or cloud metadata endpoints.
- Store original files in private object storage; use short-lived signed URLs.
- Never serve uploaded content as active HTML.
- Preserve the existing editor content if replacement extraction fails.
- Delete temporary extraction artifacts according to the retention policy.

## 5. AI-specific security

### Prompt injection
- User text and uploaded documents are data, not instructions to the system.
- The Humanizer must not execute embedded instructions, reveal system prompts, call tools, or access unrelated user data.
- Do not place secrets or privileged operational instructions in model-visible context.
- Use explicit delimiters and structured input/output schemas.
- Validate provider output before rendering or storing.

### Provider data handling
- Send only the minimum text and context required for the requested task.
- Do not include account email, payment details, unrelated history, or other users' data.
- Use provider settings/contracts that prevent provider training on submitted content.
- Keep provider request IDs and usage metadata, not raw prompt/response content, in operational logs.
- Block providers until privacy, retention, region, and transfer reviews pass.

### Detector integrity
- Pin model/config versions per job.
- Keep benchmark and test sets separate from production training.
- Prevent test-set leakage through source/group lineage.
- Monitor HUMAN false-positive rate, calibration, drift, and unsupported-language behavior.
- Never present the result as proof of authorship.

## 6. Payment and credit controls

- Resolve package price and currency on the server from an effective configuration version.
- Never accept client-supplied amount as authoritative.
- Verify provider signature and transaction details before marking Paid.
- Enforce unique provider transaction/event IDs.
- Grant credit in the same database transaction as the verified payment state transition, using an idempotent ledger command.
- Do not let Admin edit balance directly.
- Credit adjustments are append-only entries with reason, actor, case reference, and before/after balance.
- Reconcile provider state against internal payment records.
- Use database locks/constraints to prevent concurrent reservations from overspending.

## 7. Admin access controls

- Super Admin, Admin, and Moderator have separate permission sets.
- Admin login requires 2FA.
- Admins cannot self-escalate.
- Sensitive text access requires explicit consent, relevant ticket/report, minimum object scope, maximum one-hour grant, and audit.
- Moderator has no default raw-text access.
- Audit logs are append-only or tamper-evident and access controlled.
- Sensitive configuration changes require reason, effective time, and before/after values.

## 8. Application security baseline

- HTTPS/TLS everywhere; service-to-service traffic stays private.
- Secure, HttpOnly, SameSite cookies; CSRF protection for cookie-authenticated mutations.
- Strict CORS allowlist and Content Security Policy.
- Rate limits on auth, upload, job creation, payment intent, reward callback, support, and Admin endpoints.
- Backend validation and authorization on every request.
- Parameterized database queries and least-privilege database roles.
- Secret manager/environment injection; no secrets in source control or browser bundles.
- Security headers and safe error responses.
- Dependency, secret, SAST, and container image scanning in CI.
- Separate development, staging, and production credentials/data.
- No real user text in test fixtures.

## 9. Security testing plan

| Test | Expected result |
|---|---|
| Cross-user job/result ID substitution | 403/404; no data leakage |
| Missing/expired consent for sensitive Admin access | Denied; audit event |
| Moderator attempts raw-text endpoint | Denied |
| Duplicate payment webhook | One payment transition and one credit grant |
| Invalid webhook signature | No credit grant |
| Duplicate reward SSV | One reward grant |
| Forged client reward event | No credit grant |
| Concurrent credit reservations | Balance cannot be overspent |
| Cancel vs complete race | One terminal state and one settlement |
| Malformed/oversized/zip-bomb file | Rejected or safely quarantined |
| Prompt injection in source text | Treated as content; no system/tool disclosure |
| XSS payload in generated output | Rendered inert |
| Raw text in application logs | Test fails |
| Session revocation | Revoked session cannot refresh or access protected APIs |
| Backup restore | Restored state is consistent and verified |

## 10. Incident response

- Define severity levels and incident owner.
- Preserve security evidence without copying raw text into general logs.
- Contain compromised sessions, keys, providers, and service accounts.
- Identify affected data subjects and processors.
- Follow applicable notification obligations, including UU PDP timelines when criteria are met.
- Document root cause, remediation, and follow-up test.
- Reassess DPIA and provider risk after material changes.

## 11. Release gates

Production release is blocked until:
- Threat model reviewed against final architecture.
- Security testing passes for authentication, authorization, payments, credits, file handling, and Admin.
- Privacy/processor/cross-border reviews are complete.
- Child-safety self-assessment and DPIA applicability are resolved.
- Backup/restore and incident response are tested.
- No critical/high unresolved vulnerabilities remain without an approved mitigation.

# Lexora API and Event Contracts

- **Tanggal:** 2026-11-17
- **Status:** Conceptual API contract for System Design; payload schemas and exact error codes must be frozen before implementation.
- **Base path:** `/api/v1`
- **Transport:** HTTPS + JSON; file transfer uses private signed URLs.
- **Source of truth:** SRS and Decision Log.

## 1. Contract rules

1. All business endpoints authenticate and authorize on the server.
2. All request bodies are validated against shared Zod schemas on the server.
3. The frontend is never trusted for character count, price, credit balance, role, payment status, or job state.
4. Use `Idempotency-Key` for job creation, payment intent creation, credit adjustments, and other non-repeatable actions.
5. Never put raw text, uploaded file contents, passwords, API keys, or payment secrets in URLs, query strings, queue payloads, or logs.
6. Long-running processing returns a job ID and status; it does not hold an HTTP request open.
7. Use opaque IDs; do not expose database primary keys.
8. Provider webhooks are separate endpoints with provider signature verification and replay protection.

## 2. Response envelope

Success:
```json
{
  "data": {},
  "meta": {
    "request_id": "req_opaque",
    "timestamp": "2026-11-17T00:00:00Z"
  }
}
```

Error:
```json
{
  "error": {
    "code": "INSUFFICIENT_CREDITS",
    "message": "Saldo kredit tidak mencukupi.",
    "field_errors": {},
    "request_id": "req_opaque"
  }
}
```

Do not return stack traces, provider secrets, internal prompts, or raw exception messages.

## 3. Identity and account

Authentication endpoints are provided by Better Auth under the configured auth base path. Product APIs:
- `GET /api/v1/account`
- `PATCH /api/v1/account/profile`
- `POST /api/v1/account/email-change`
- `GET /api/v1/account/sessions`
- `DELETE /api/v1/account/sessions/{sessionId}`
- `POST /api/v1/account/sessions/revoke-others`
- `GET /api/v1/account/consents`
- `PATCH /api/v1/account/consents`
- `POST /api/v1/privacy/requests`
- `GET /api/v1/privacy/requests`

Account linking must require proof of control over the existing identity and explicit confirmation.

## 4. Detector

- `POST /api/v1/detector/estimate`
- `POST /api/v1/detector/jobs`
- `GET /api/v1/detector/jobs/{jobId}`
- `GET /api/v1/detector/jobs/{jobId}/result`
- `GET /api/v1/detector/jobs/{jobId}/report?format=txt|docx|pdf`
- `POST /api/v1/jobs/{jobId}/cancel`

Request example:
```json
{
  "input": {
    "type": "text",
    "text": "User text is sent in the request body only."
  },
  "language_hint": "id"
}
```

Rules:
- Backend counts extended grapheme clusters using the pinned Unicode version.
- Maximum 20,000; no hard product minimum.
- Input language and support status are checked before processing.
- Estimate is returned before job confirmation.
- Job creation reserves credits transactionally.
- Result includes overall label, warnings, per-sentence analysis, and model/config version metadata.
- Numeric authorship percentages are not part of the MVP response.

## 5. Humanizer

- `POST /api/v1/humanizer/estimate`
- `POST /api/v1/humanizer/jobs`
- `GET /api/v1/humanizer/jobs/{jobId}`
- `GET /api/v1/humanizer/jobs/{jobId}/result`
- `POST /api/v1/humanizer/jobs/{jobId}/save-history`
- `GET /api/v1/humanizer/history`
- `GET /api/v1/humanizer/history/{historyId}`
- `DELETE /api/v1/humanizer/history/{historyId}`

Rules:
- Authenticated account required.
- Text length 100–50,000 extended grapheme clusters.
- Style/profile ID must belong to the authenticated user and be Active.
- Job stores an immutable profile version snapshot.
- History is saved only through explicit user action where required by SRS.
- Result exports support TXT, DOCX, and PDF.

## 6. Style profiles

- `GET /api/v1/humanizer/profiles`
- `POST /api/v1/humanizer/profiles`
- `GET /api/v1/humanizer/profiles/{profileId}`
- `PATCH /api/v1/humanizer/profiles/{profileId}`
- `POST /api/v1/humanizer/profiles/{profileId}/samples`
- `DELETE /api/v1/humanizer/profiles/{profileId}/samples/{sampleId}`
- `POST /api/v1/humanizer/profiles/{profileId}/evaluate`
- `POST /api/v1/humanizer/profiles/{profileId}/samples/{sampleId}/restore`
- `DELETE /api/v1/humanizer/profiles/{profileId}`

Rules:
- Sample and profile limits are enforced on the backend.
- Sample versions are immutable.
- Evaluation is asynchronous and returns a job/evaluation ID.
- Deletion and restore are state transitions with atomic behavior.
- Profile deletion does not rewrite an already-running document job snapshot.

## 7. Credits

- `GET /api/v1/credits/balance`
- `GET /api/v1/credits/lots`
- `GET /api/v1/credits/ledger`
- `POST /api/v1/credits/estimate`
- `GET /api/v1/credits/reservations/{reservationId}`

Client cannot directly create a credit lot, edit balance, settle a reservation, or refund credits. These are internal domain commands.

## 8. Payments

- `POST /api/v1/payments/intents`
- `GET /api/v1/payments/transactions`
- `GET /api/v1/payments/transactions/{transactionId}`
- `POST /api/v1/webhooks/midtrans`

Payment intent creation requires package ID and idempotency key. Price and currency are resolved server-side from the effective configuration version; never accept a client-supplied amount as authoritative.

Webhook processing:
1. Verify provider signature/authenticity.
2. Validate merchant, order ID, amount, currency, and status.
3. Persist raw provider event metadata with secrets redacted.
4. Deduplicate by provider event/transaction identity.
5. Transition payment state monotonically.
6. Grant a credit lot only after verified Paid.
7. Reconcile unknown or mismatched states for Admin review.

## 9. Support and notifications

- `POST /api/v1/support/tickets`
- `GET /api/v1/support/tickets`
- `GET /api/v1/support/tickets/{ticketId}`
- `POST /api/v1/support/tickets/{ticketId}/messages`
- `GET /api/v1/notifications`
- `PATCH /api/v1/notifications/{notificationId}`
- `GET /api/v1/notifications/preferences`
- `PATCH /api/v1/notifications/preferences`

MVP ticket creation does not accept file attachments. Promotional notification preference is separate from essential/security notifications.

## 10. Admin

Admin routes are protected by role + permission checks and Admin 2FA:
- `GET /api/v1/admin/overview`
- `GET /api/v1/admin/users`
- `POST /api/v1/admin/users/{userId}/suspend`
- `POST /api/v1/admin/users/{userId}/restore`
- `GET /api/v1/admin/payments`
- `GET /api/v1/admin/credit-ledger`
- `POST /api/v1/admin/credit-adjustments`
- `GET /api/v1/admin/support/tickets`
- `GET /api/v1/admin/audit-logs`
- `POST /api/v1/admin/sensitive-access-grants`
- `POST /api/v1/admin/config-versions`
- `GET /api/v1/admin/operations/failed-jobs`

Every privileged mutation requires a reason and writes an audit event. Raw text access is denied unless all consent/ticket/scope/expiry checks pass.

## 11. Internal event contracts

| Event | Producer | Consumer | Idempotency key |
|---|---|---|---|
| `job.created` | Web/domain | Worker | job ID |
| `job.started` | Worker | Operations/notification | job ID + attempt |
| `job.completed` | Worker | Credit, notification, result UI | job ID |
| `job.failed` | Worker | Credit, notification, operations | job ID |
| `payment.paid` | Webhook handler | Credit ledger, notification | provider transaction ID |
| `payment.refund.updated` | Provider webhook/Admin | Payment, ledger, notification | refund ID |
| `credit.reserved` | Credit domain | Job domain/audit | reservation ID |
| `credit.settled` | Credit domain | Job domain/audit | reservation ID |
| `reward.verified` | Reward verifier | Credit ledger | reward-session ID |
| `notification.requested` | Domain modules | Notification worker | event ID |
| `privacy.request.created` | Privacy domain | Privacy operations | request ID |

## 12. Error catalogue baseline

| Code | Meaning | Expected behavior |
|---|---|---|
| `INPUT_TOO_LONG` | Input exceeds feature maximum | Reject before queue/reservation |
| `INPUT_TOO_SHORT_FOR_EVIDENCE` | Input is too short for reliable Detector evidence | Return UNCERTAIN, not hard rejection |
| `UNSUPPORTED_FILE_TYPE` | File type unsupported | Reject upload |
| `FILE_EXTRACTION_FAILED` | File could not be safely extracted | Preserve previous editor state |
| `UNSUPPORTED_LANGUAGE` | Dominant language outside Detector scope | Return UNCERTAIN/unsupported language |
| `INSUFFICIENT_CREDITS` | Balance below estimate | Do not queue job |
| `PROFILE_NOT_READY` | Profile is not Active | Prevent selection and explain next action |
| `PAYMENT_NOT_VERIFIED` | Provider payment not verified | Do not grant credits |
| `JOB_NOT_CANCELLABLE` | Terminal or execution state prevents cancellation | Return current state and explanation |
| `CONSENT_REQUIRED` | Required consent is missing/expired | Deny sensitive processing/access |
| `FORBIDDEN` | Actor lacks permission | Deny and audit privileged attempts |
| `RATE_LIMITED` | Request exceeds configured limit | Return retry guidance and Retry-After |

Exact schemas, pagination, HTTP status mapping, rate-limit numbers, and token/session details are frozen during implementation planning.

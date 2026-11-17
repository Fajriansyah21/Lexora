# Lexora User Flows

- **Tanggal:** 2026-11-17
- **Status:** User flow baseline for MVP; detailed visual wireframes are in [UI/UX Specification](UI-UX-SPECIFICATION.md).
- **Source of truth:** SRS and Decision Log. If this document conflicts with SRS, SRS wins.

## 1. Public entry and product discovery

```mermaid
flowchart TD
  A[Visitor opens Lexora] --> B[Landing page]
  B --> C{Choose a tool}
  C --> D[AI Text Detector]
  C --> E[AI Humanizer]
  B --> F[Pricing and credits]
  B --> G[Help and privacy]
  D --> H{Guest or signed-in?}
  H --> I[Guest session]
  H --> J[Authenticated app]
  E --> K[Sign in / register]
  K --> J
```

## 2. Guest AI Text Detector

```mermaid
flowchart TD
  A[Open Detector] --> B[Paste text or upload TXT/DOCX/PDF]
  B --> C[Validate file, extraction, language, and 20k grapheme limit]
  C -->|Invalid or too long| D[Show specific validation error]
  C -->|Valid| E[Show input count and estimated credit]
  E --> F{Guest session has usable credit?}
  F -->|No| G[Show sign-in or configured non-ad trial credit]
  F -->|Yes| H[Confirm analysis]
  G --> I{User chooses sign-in or trial?}
  I -->|Sign in| J[Authenticate and preserve draft]
  I -->|Trial credit| K[Grant configured session-bound trial once]
  J --> H
  K --> H
  H --> L[Reserve credit and create job]
  L --> M[Queue and worker]
  M --> N[Detector inference]
  N --> O[Aggregate segment evidence]
  O --> P[Settle credit and save result state]
  P --> Q[Show label, explanation, warnings, and sentence analysis]
  Q --> R[Copy or download report]
  Q --> S[Explicit handoff to Humanizer]
  S --> T[Require login if needed and preserve selected text]
```

Rules:
- The backend validates the 20,000 extended grapheme limit before reservation or queueing. Guest rewarded ads are disabled on MVP; Guest may receive a configured non-ad trial grant.
- No minimum input is enforced as a hard rejection. If evidence is insufficient, the result is UNCERTAIN.
- Unsupported dominant language returns UNCERTAIN/unsupported language.
- No numeric authorship percentage is shown in MVP.
- A result is not proof of authorship or misconduct.

## 3. Registered AI Humanizer

```mermaid
flowchart TD
  A[Open Humanizer] --> B{Authenticated?}
  B -->|No| C[Sign in / register]
  B -->|Yes| D[Choose built-in style or personal profile]
  C --> D
  D --> E[Paste text or upload document]
  E --> F[Extract into temporary editor state]
  F --> G[Edit text and review count]
  G --> H{100 to 50k grapheme clusters?}
  H -->|No| I[Show remaining/over-limit count]
  I --> G
  H -->|Yes| J[Estimate credit]
  J --> K{Sufficient balance?}
  K -->|No| L[Top up or return]
  L --> J
  K -->|Yes| M[Confirm and reserve]
  M --> N[Queue Humanizer job]
  N --> O[Worker loads profile snapshot and calls provider]
  O --> P{Success?}
  P -->|No| Q[Release reservation and show safe error]
  P -->|Yes| R[Settle actual verified usage]
  R --> S[Show result and source/result comparison]
  S --> T[Copy or download]
  S --> U{Save to history?}
  U -->|Yes| V[Persist history entry]
  U -->|No| W[Keep temporary result for active session]
```

## 4. Create a personal style profile

```mermaid
flowchart TD
  A[Open Style Profiles] --> B[Create profile and name it]
  B --> C[Add sample text or upload supported file]
  C --> D[Validate each sample >=500 grapheme clusters]
  D -->|Below minimum| E[Keep sample as incomplete and show remaining count]
  E --> C
  D -->|Eligible| F[Store immutable sample version]
  F --> G{At least 3 eligible samples?}
  G -->|No| C
  G -->|Yes| H[Run adaptive quality evaluation]
  H --> I{Consistent and diverse enough?}
  I -->|No| J[Explain gap and request more samples]
  J --> C
  I -->|Yes| K[Activate profile]
  K --> L[Set as main or additional profile]
```

A count of three eligible samples is necessary but not sufficient. Adaptive evaluation can request more samples. Maximum 20 samples per profile; maximum six profiles per account.

## 5. Purchase credits

```mermaid
flowchart TD
  A[Open credit page] --> B[Choose package]
  B --> C[Create payment intent]
  C --> D{Authenticated?}
  D -->|No| E[Register / sign in]
  E --> F[Link pending purchase intent]
  D -->|Yes| G[Open Midtrans Snap checkout]
  F --> G
  G --> H[User completes or abandons payment]
  H --> I[Provider sends webhook]
  I --> J[Verify signature, transaction, amount, currency]
  J -->|Invalid| K[Keep unpaid and log event]
  J -->|Valid Paid| L[Idempotently mark Paid]
  L --> M[Create credit lot and ledger entry]
  M --> N[Notify user and show receipt]
```

The browser redirect is never sufficient proof of payment. The server-side webhook and reconciliation process determine payment state.

## 6. Credit reservation and job cancellation

```mermaid
stateDiagram-v2
  [*] --> Estimated
  Estimated --> Rejected: Insufficient balance
  Estimated --> Reserved: User confirms
  Reserved --> Waiting: Job queued
  Waiting --> Cancelled: User cancels
  Waiting --> Processing: Worker starts
  Processing --> Completed: Provider result verified
  Processing --> CancelRequested: User requests cancel
  CancelRequested --> Cancelled: Worker/provider confirms stop
  CancelRequested --> Completed: Completion wins race
  Processing --> Failed: Permanent failure
  Processing --> RetryWaiting: Transient failure and retries remain
  RetryWaiting --> Processing: Retry
  RetryWaiting --> Failed: Retry budget exhausted
  Completed --> Settled: Settle verified usage and release remainder
  Cancelled --> Released: Release reservation or settle verified usage
  Failed --> Released: Release full reservation if no result
  Settled --> [*]
  Released --> [*]
```

## 7. Support ticket

```mermaid
flowchart TD
  A[Open Support] --> B[Choose category and describe issue]
  B --> C[Submit ticket]
  C --> D[Open]
  D --> E[In Progress]
  E --> F{Need user response?}
  F -->|Yes| G[Waiting for User]
  G --> H[User replies]
  H --> E
  F -->|No| I[Resolved]
  I --> J{User replies within 7 days?}
  J -->|Yes| E
  J -->|No| K[Closed]
  K --> L[New issue requires new ticket]
```

No file attachments are available in MVP. Users should provide ticket IDs, transaction references, and redacted descriptions rather than uploading raw documents.

## 8. Admin sensitive text access

```mermaid
flowchart TD
  A[Support ticket or report exists] --> B[User provides explicit consent]
  B --> C[Authorized Admin requests scoped access]
  C --> D{Permission + ticket + consent valid?}
  D -->|No| E[Access denied and logged]
  D -->|Yes| F[Grant access to specific object]
  F --> G[One-hour expiry timer enforced server-side]
  G --> H[Admin reviews minimum necessary content]
  H --> I[Access expires or is revoked]
  I --> J[Audit record retained]
```

Super Admin does not receive default raw-text access. Moderator has no default access to user text.

## 9. Privacy request

```mermaid
flowchart TD
  A[User opens Privacy Center] --> B[Choose access, correction, deletion, withdrawal, or objection]
  B --> C[Verify identity proportionally]
  C --> D[Create request ID and status]
  D --> E[Route to privacy owner]
  E --> F[Check legal retention and processor dependencies]
  F --> G[Execute permitted action across data layers]
  G --> H[Record exceptions and evidence]
  H --> I[Notify user and close request]
```

## 10. Notification preferences

- Security and essential transaction notifications remain enabled.
- Promotional notifications require separate opt-in.
- Delivery retries do not alter the underlying transaction/job state.
- Duplicate event IDs create at most one logical notification.

## 12. Flow invariants

1. Backend is authoritative for length, balance, permissions, payment, and job state.
2. No raw text is placed in queue payloads or general logs.
3. A job has one idempotency key across retries.
4. Payment and reward grants are idempotent.
5. Credit balance is derived from ledger entries.
6. Guest credit is not transferred during account conversion.
7. User text is not used for model training by default.
8. A Detector result is never presented as proof of authorship.

## 11. Login-only rewarded ad

```mermaid
flowchart TD
  A[Logged-in user opens Credits] --> B[Rewarded ad available flag + eligibility check]
  B -->|Not eligible| C[Do not show ad option]
  B -->|Eligible| D[Show reward amount, expiry, non-transferability, and conditions]
  D --> E{User opts in?}
  E -->|No| F[Continue normal platform use]
  E -->|Yes| G[Create server-side reward session]
  G --> H[Request Google Ad Manager Rewarded Web]
  H --> I[User completes ad]
  I --> J[Google SSV callback]
  J --> K[Verify signature/key ID/transaction ID]
  K --> L{Can callback be securely linked to account?}
  L -->|No| M[Do not grant; keep ads disabled pending provider clarification]
  L -->|Yes| N[Idempotently grant one credit lot]
  N --> O[Notify user]
```

Guest rewarded ads are disabled on MVP. Guest can only use a configured non-ad trial grant tied to the Guest session. The web SSV callback fields must be tested before production; do not assume user_id/custom_data are available on the web format.

## 12. Flow invariants

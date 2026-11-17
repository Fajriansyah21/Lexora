# Critical Acceptance Test Scenarios

- **Tanggal:** 2026-11-17
- **Status:** Test scenarios designed; execution waits for implementation.
- **Related matrix:** [Acceptance Criteria Baseline](ACCEPTANCE-CRITERIA.md).
- **Important:** These are executable test designs, not claims that the features already exist.

## A. AI Text Detector

### DET-AC-01 — Maximum input boundary
```gherkin
Given a valid Detector request
When the input contains exactly 20,000 extended grapheme clusters
Then backend validation accepts the length and continues to the next validation stage
When the input contains 20,001 extended grapheme clusters
Then the backend rejects it before queueing, model invocation, or credit reservation
```

### DET-AC-02 — Short text abstention
```gherkin
Given a valid input shorter than the model's reliable evidence threshold
When the user requests analysis
Then the system does not reject it solely because of a product minimum
And returns UNCERTAIN/insufficient context when evidence is inadequate
And does not force HUMAN or AI
```

### DET-AC-03 — Unsupported language
```gherkin
Given text whose dominant language is outside Indonesian and English
When the user requests analysis
Then the system returns unsupported language/UNCERTAIN
And does not present a HUMAN, AI, or MIXED authorship conclusion
```

### DET-AC-04 — MIXED versus UNCERTAIN
```gherkin
Given a document with sufficient evidence for HUMAN-like and AI-like patterns in distinct segments
When document aggregation runs
Then the document may be classified MIXED
Given a document with only conflicting or weak evidence
When document aggregation runs
Then the document is UNCERTAIN, not MIXED
```

### DET-AC-05 — No uncalibrated numeric score
```gherkin
Given the MVP Detector result screen and downloadable report
When any result category is displayed
Then no authorship percentage or numeric probability is shown
And the category, explanation, and limitation notice remain visible
```

### DET-AC-06 — Sentence-level abstention and aggregation
```gherkin
Given a document containing both long and very short sentences
When sentence analysis completes
Then short/context-poor sentences are marked UNCERTAIN/insufficient context
And document aggregation uses the validated method
And does not use unvalidated simple majority vote
```

### DET-AC-07 — Report export
```gherkin
Given a completed Detector result
When the user downloads TXT, DOCX, or PDF
Then each supported format contains the overall label, summary, warnings, and available sentence analysis
And the report does not claim to prove authorship or misconduct
```

## B. AI Humanizer

### HUM-AC-01 — Minimum profile samples
```gherkin
Given a profile with two eligible samples
When the user attempts to activate it
Then the profile remains unavailable and requests another sample
Given a profile with three eligible samples of at least 500 extended grapheme clusters each
When the adaptive quality assessment passes
Then the profile becomes available
And a three-sample count alone does not bypass the quality assessment
```

### HUM-AC-02 — Sample and profile limits
```gherkin
Given a profile already containing 20 active samples
When the user tries to add another sample
Then the system rejects the addition without deleting existing samples
Given an account already containing six profiles
When the user tries to create a seventh
Then the system requires an eligible profile to be removed first
```

### HUM-AC-03 — Main profile deletion
```gherkin
Given an account with multiple profiles and one main profile
When the user deletes the main profile
Then the system requires a replacement profile before final confirmation
Given the main profile is the only profile
When the user confirms deletion
Then deletion may proceed without a replacement and the built-in style is used afterward
```

### HUM-AC-04 — Bulk sample deletion and recovery
```gherkin
Given a profile with active samples
When the user confirms Delete All Samples
Then all active samples move to Recently Deleted
And remain recoverable for 30 days
When the user restores an eligible sample within the recovery window
Then the sample returns to the active list without duplicate creation
```

### HUM-AC-05 — Failed document replacement preserves editor
```gherkin
Given an editor containing extracted text and manual edits
When the user confirms replacement with a corrupt or unreadable file
Then extraction fails safely
And the prior document content and manual edits remain unchanged
And a clear error is displayed
```

### HUM-AC-06 — Profile deletion and in-flight jobs
```gherkin
Given a profile has a profile-evaluation job and a document Humanizer job already Processing
When the user confirms profile deletion
Then profile-management jobs are cancelled and stale results cannot recreate the profile
And the document job continues using the immutable profile snapshot captured at start
And no new job can select the deleted profile
```

### HUM-AC-07 — Profile deletion cancellation race
```gherkin
Given a deletion request is pending but execution has not started
When the user cancels and the cancellation state transition wins
Then no profile data is deleted and the worker does not execute deletion
Given the worker atomically transitions the request to Executing first
When the user attempts cancellation
Then cancellation is rejected and the UI explains that execution has started
```

### HUM-AC-08 — Atomic profile deletion failure
```gherkin
Given a profile with versions, samples, and related records
When the deletion transaction fails at any stage
Then all profile data remains intact
And cancelled profile-management jobs are not resumed automatically
And a new retry must be submitted as a new request
```

### HUM-AC-09 — Export history cooldown
```gherkin
Given a full-history deletion transaction reaches terminal Failed at server time T
When the user submits another attempt before T plus 30 seconds
Then the server rejects the attempt and returns the authoritative retry time
When the user submits after the cooldown
Then a new authentication and confirmation are required
```

### HUM-AC-10 — Unicode character counting
```gherkin
Given text containing combining marks, emoji ZWJ sequences, flag emoji, spaces, LF, and CRLF
When the frontend displays a character count and backend validates the same text
Then both use the pinned extended grapheme cluster rules
And the stored source text is not normalized or mutated for counting
```

## C. Account and sessions

### ACC-AC-01 — Secure account linking
```gherkin
Given an email/password account and a Google identity with the same email
When the user signs in through the second method
Then the system does not silently merge the accounts
And requires proof of control over the existing account before linking
```

### ACC-AC-02 — Guest conversion
```gherkin
Given a Guest with a Detector draft and temporary reward balance
When the Guest registers successfully
Then the draft may be carried into the account session as specified
But Guest reward credit is not transferred
And a new analysis is required for the registered account
```

### ACC-AC-03 — Session revocation
```gherkin
Given a registered user with multiple active sessions
When the user revokes one session or all other sessions
Then the server invalidates the selected session credentials
And the revoked device cannot refresh or continue authenticated requests
```

## D. Credits and reward

### CRED-AC-01 — Credit reservation and settlement
```gherkin
Given a job estimate of E credits and an account balance of at least E
When the user confirms processing
Then E credits are reserved before queueing
When the job succeeds with verified cost A where A is less than or equal to E
Then A is settled and E minus A is released
And no additional charge above E is applied
```

### CRED-AC-02 — Insufficient balance
```gherkin
Given the available balance is below the displayed estimate
When the user submits the job
Then no job is queued and no credit is reserved or deducted
```

### CRED-AC-03 — Failure refund
```gherkin
Given a job has a credit reservation
When the system/provider fails before a result is delivered
Then the full reservation is released
And duplicate failure callbacks do not create duplicate refunds
```

### CRED-AC-04 — Guest credit expiry
```gherkin
Given a Guest reward grant at timestamp T
When the time reaches T plus 24 hours
Then the reward is no longer usable
And it cannot be transferred to a newly registered account
```

### CRED-AC-05 — Daily bonus
```gherkin
Given an active registered account on a calendar date in Asia/Jakarta
When the daily bonus scheduler reaches 03:00
Then exactly 20 credits are granted once for that account/date
And rerunning the scheduler does not grant a duplicate
```

### CRED-AC-06 — Reward callback verification
```gherkin
Given a rewarded-ad completion callback
When the server verifies its authenticity and unique reward-session ID
Then one reward grant is written to the ledger
When the callback is forged or replayed
Then no additional credit is granted
```

## E. Payments

### PAY-AC-01 — Verified payment grants credit
```gherkin
Given a Pending payment with matching transaction ID, amount, currency, and valid provider signature
When the backend verifies the payment as Paid
Then the transaction becomes Paid and the associated credit lot is granted once
```

### PAY-AC-02 — Invalid or mismatched callback
```gherkin
Given a callback with an invalid signature or mismatched amount/currency
When the backend receives it
Then the transaction is not marked Paid
And no credit is granted
And the event is recorded for investigation
```

### PAY-AC-03 — Duplicate and out-of-order callbacks
```gherkin
Given a transaction already marked Paid
When the same Paid callback is replayed or an older Pending callback arrives later
Then no duplicate credit is granted
And the transaction remains Paid
```

### PAY-AC-04 — Guest purchase recovery
```gherkin
Given a Guest starts a purchase and is required to authenticate
When the Guest completes registration/login
Then the pending purchase intent can be linked to the authenticated account
And credit is granted only after verified payment
```

## F. Support and notifications

### SUP-AC-01 — Ticket lifecycle
```gherkin
Given an Open ticket
When support moves it to In Progress, Waiting for User, Resolved, or Closed
Then each allowed transition is recorded
And the user sees the current status and conversation history
```

### SUP-AC-02 — Reopen window
```gherkin
Given a ticket has status Resolved
When the user replies within seven calendar days
Then the ticket reopens
When the seven-day window has passed
Then the user must create a new ticket
```

### NOT-AC-01 — Duplicate notification
```gherkin
Given a notification event with a unique event ID
When the event is delivered or retried multiple times
Then only one logical notification is created
And delivery failures do not change the underlying payment/job/security state
```

### NOT-AC-02 — Promotional consent
```gherkin
Given a user has not opted in to promotional notifications
When a promotional campaign is triggered
Then no promotional email or in-app promotion is sent
When the user opts out
Then future promotional delivery stops
```

## G. Admin and operations

### ADM-AC-01 — Moderator cannot access raw text
```gherkin
Given a Moderator role
When the Moderator opens a user document or sample content endpoint
Then access is denied
And the attempt is recorded in the security/audit log
```

### ADM-AC-02 — Time-limited sensitive text access
```gherkin
Given a relevant ticket and explicit user consent
When an authorized Admin requests access to the specific text
Then access is limited to that object and expires within one hour
When consent is absent or expired
Then access is denied
```

### ADM-AC-03 — Ledger adjustment audit
```gherkin
Given an Admin with credit-adjustment permission
When the Admin submits an adjustment with reason and case reference
Then a new ledger entry is created
And the prior ledger entries remain immutable
And actor, timestamp, reason, and before/after balance are recorded
```

### OPS-AC-01 — Queued job cancellation
```gherkin
Given a job in Waiting
When the user cancels it
Then the job becomes Cancelled
And the full reservation is released
And the worker cannot later execute the cancelled job
```

### OPS-AC-02 — Processing cancellation race
```gherkin
Given a job in Processing
When cancellation and provider completion race
Then the terminal state reflects the event that is confirmed first by the worker/provider
And the ledger settles only verified usage
And no duplicate result or refund is created
```

### OPS-AC-03 — Retry classification
```gherkin
Given a transient provider/network failure
When retry policy executes
Then at most two automatic retries occur with exponential backoff and jitter
Given a permanent validation/authentication/billing error
When retry policy evaluates it
Then no automatic retry occurs
```

## H. Nonfunctional controls

### NFR-AC-01 — No raw text in logs
```gherkin
Given requests containing user text
When application, access, error, and telemetry logs are generated
Then raw text and uploaded document contents are absent by default
And logs contain only approved operational metadata
```

### NFR-AC-02 — Backend validation
```gherkin
Given a client bypasses or alters frontend validation
When the request reaches the API
Then the backend independently validates input, file, balance, transaction state, and authorization
And rejects invalid requests without side effects
```

### NFR-AC-03 — Idempotency
```gherkin
Given duplicate payment, reward, job, refund, or notification events
When they are replayed
Then each logical business operation produces at most one side effect
```

### NFR-AC-04 — Accessibility
```gherkin
Given each MVP flow and modal
When tested using keyboard-only navigation and supported screen readers
Then focus order, labels, contrast, status announcements, and modal focus management meet WCAG 2.2 AA
```

### NFR-AC-05 — Performance and availability release gate
```gherkin
Given the selected infrastructure and model provider
When load, latency, and availability benchmarks are run
Then numerical targets, measurement windows, and failure thresholds are documented before launch
And no SLO claim is published before the evidence passes
```

## H. Test execution status

All scenarios above are **Not executed**. They become executable when the corresponding implementation or test harness exists. Evidence must include test ID, commit SHA, environment, test data/fixture, actual result, and timestamp.

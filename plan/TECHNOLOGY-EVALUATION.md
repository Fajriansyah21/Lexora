# Technology Evaluation and Recommended Stack

- **Tanggal:** 2026-11-17
- **Status:** Recommended architecture for MVP; provider/region/price decisions remain conditional where legal, merchant, or benchmark evidence is required.
- **Product:** Lexora — AI Text Detector + AI Humanizer.
- **Architecture style:** Modular monolith with dedicated background worker and Python inference service.

## 1. Design constraints

1. Preserve the existing project preference for React + Next.js.
2. Keep the application code primarily TypeScript to reduce language/runtime sprawl.
3. Keep ML inference in Python because the detector research and model ecosystem are Python-first.
4. Separate long-running AI work from web request lifetimes.
5. Make PostgreSQL the source of truth for accounts, credits, jobs, payments, profiles, and audit records.
6. Never put raw user text in queue payloads, general logs, or analytics by default.
7. Keep payment, reward, and job side effects idempotent.
8. Prefer managed infrastructure where it materially reduces operational burden, but keep the app portable through Docker.
9. Do not lock in a model/provider until privacy review, benchmark, latency, and unit economics pass.

## 2. Recommended stack

| Layer | Recommendation | Reason | Status |
|---|---|---|---|
| Web framework | Next.js 16.x App Router + React 19.x + TypeScript | SSR/SEO for public pages, interactive editor/dashboard, shared TypeScript types, route handlers | Recommended |
| Runtime | Node.js 26 LTS | Current Active LTS line; supported by current Next.js requirements | Recommended |
| Styling | Tailwind CSS 4.x + shadcn/ui + Radix UI | Fast consistent UI, accessible primitives, design-token ownership | Recommended |
| Icons | Lucide | Consistent icon set with low visual noise | Recommended |
| Forms/validation | React Hook Form + Zod | Typed client validation; backend repeats authoritative validation | Recommended |
| Authentication | Better Auth | Email/password, OAuth, sessions, account linking, and extensible plugins without a mandatory SaaS identity vendor | Recommended; security review required |
| Database | PostgreSQL 18 | Strong transactions, constraints, JSONB, row locking, and robust financial-ledger modeling | Recommended |
| ORM/migrations | Drizzle ORM | Type-safe SQL-oriented access and explicit transaction control | Recommended |
| Queue/cache | Redis 8 + BullMQ | Dedicated workers, retries, backoff, delayed jobs, rate limits, concurrency, and job events | Recommended |
| Node worker | Separate Node.js worker process in same monorepo | Long-running jobs do not depend on browser/API request lifetime | Required |
| Detector inference | Python 3.13 + FastAPI | Python ML ecosystem; isolate inference from web app | Recommended |
| Detector baseline | TF-IDF + Linear SVM, compared with IndoBERT/XLM-R candidates | A strong classical baseline prevents premature Transformer selection | Experiment only |
| Humanizer provider | Provider adapter; OpenAI API as first candidate, Gemini API as comparison | Avoid vendor lock-in; compare quality, privacy, latency, and cost | Candidate, not final |
| File storage | Private S3-compatible object storage | Signed URLs, lifecycle policies, isolated uploads, portable interface | Required; provider/region conditional |
| Payment | Midtrans Snap | Hosted checkout, one integration for supported payment methods, no monthly Snap fee | Primary candidate; merchant fee confirmation required |
| Rewarded ads | Google Ad Manager Rewarded Web | Web-specific rewarded inventory; do not use AdMob as if this were a mobile app | Conditional; policy/account approval required |
| Email | Provider adapter; Resend or Amazon SES shortlist | Transactional email for verification, password reset, payment, and support | Provider not selected |
| Observability | OpenTelemetry + Sentry; metrics dashboard | Trace job lifecycle, failures, and performance without logging user text | Recommended |
| Deployment | Docker containers on a container host | Supports Next.js, worker, Python inference, and internal networking | Recommended |
| Monorepo | pnpm workspaces + Turborepo; Python service managed separately with uv | Shared TypeScript packages and reproducible builds | Recommended |

## 3. Framework and architecture alternatives

### 3.1 Next.js vs Laravel vs Vite SPA

| Option | Advantages | Trade-offs | Decision |
|---|---|---|---|
| Next.js + React | SSR/SEO, server components, route handlers, strong ecosystem, user preference | Requires separate worker for long jobs; more moving parts than Blade | **Selected** |
| Laravel + Inertia | Mature backend, queues, auth, ORM, user has PHP/Laravel familiarity | Adds PHP runtime beside Python ML; less aligned with current React/Next preference | Viable fallback |
| Vite React SPA | Simple frontend and fast local development | SEO/public landing and server-side integration require separate backend/BFF | Not selected for MVP |

### 3.2 PostgreSQL vs MySQL

PostgreSQL is preferred because credit lots, reservations, settlement, payment callbacks, audit records, and privacy requests require reliable transactions, uniqueness constraints, and explicit locking. MySQL remains technically viable, but the project should not maintain two database dialects.

### 3.3 Drizzle vs Prisma

Drizzle is recommended because its SQL-oriented model makes transaction boundaries, unique constraints, and specialized ledger queries explicit. Prisma remains a viable alternative if team familiarity or tooling becomes more important than SQL-level control. The choice should be validated with a small schema/migration spike before implementation.

### 3.4 BullMQ vs synchronous request processing

AI processing, document extraction, reward callbacks, payment reconciliation, notifications, and deletion workflows must not run as long synchronous HTTP requests. BullMQ provides worker lifecycle, retry/backoff, delayed jobs, rate limits, and job events. PostgreSQL remains the source of truth; Redis is the queue transport, not the financial ledger.

### 3.5 FastAPI vs Node-only inference

FastAPI is recommended for the Detector because scikit-learn, PyTorch, Transformers, and model evaluation are Python-first. Humanizer orchestration remains in the Node worker and calls an external LLM provider through an adapter. This avoids moving the entire web application to Python.

## 4. Payment gateway evaluation

### Midtrans Snap — primary candidate
- Hosted checkout can be shown as a popup or redirect.
- One integration supports the payment methods enabled for the merchant.
- Snap documentation states there is no monthly Snap fee.
- Payment status must still be verified server-side; browser redirect is not proof of payment.
- Standard public pricing is not necessarily the final merchant rate for digital products. Obtain a written quote and verify supported methods, settlement, refund, and webhook behavior before activation.

### Xendit — alternative
- Strong API/webhook model and broad Indonesian payment coverage.
- Public pricing lists QRIS and Virtual Account fees, but exact effective cost depends on merchant category and terms.
- Keep the payment adapter provider-neutral so switching does not change credit-ledger logic.

**Decision:** Implement the payment domain against an internal provider interface. Midtrans Snap is the first integration candidate, subject to merchant onboarding and fee confirmation. Do not hardcode provider-specific status or fee assumptions in credit logic.

## 5. Rewarded advertising

Use a web-specific product such as Google Ad Manager Rewarded Web, not AdMob mobile SDKs.

Requirements before activation:
- The page must satisfy Google’s web rewarded-ad requirements and be mobile optimized.
- Reward is opt-in and clearly described before the ad begins.
- Reward must be non-cash, non-transferable, and usable only within Lexora.
- Use server-side verification where supported; bind reward callback to a unique server-generated session/nonce and make grants idempotent.
- MVP rewarded-ad credit is login-only. Guest uses a configurable non-ad trial grant tied to the Guest session. Reconsider Guest rewarded ads only after written/provider-level confirmation that web SSV can bind a Guest session securely and policy permits it.
- Do not activate ads until account eligibility, policy, consent, inventory, and server-side verification have been reviewed.

## 6. AI provider strategy

### Humanizer
Use a provider adapter with a common contract:
- `humanize(input, style, context, limits)`
- `estimateUsage(input, style)`
- `cancel(requestId)` where provider supports cancellation
- `getUsage(requestId)`
- `healthCheck()`

OpenAI API is the first provider candidate because API inputs/outputs are not used for model training by default. This is not a zero-retention guarantee: abuse-monitoring/application-state retention and endpoint-specific storage controls must be checked. Use non-stored request modes where supported; Zero Data Retention requires eligibility/approval. Cross-border processing remains blocked until DEC-170 review.

Evaluate OpenAI and Gemini candidates on:
- Preservation of facts, names, numbers, citations, and meaning.
- Style adherence for all six built-in styles.
- Indonesian and English quality, including code-switching.
- Latency, output length, refusal behavior, and retry behavior.
- Cost per 1,000 jobs at expected input/output sizes.
- Data retention, provider training settings, DPA, processing region, and deletion behavior.

**Do not select a fixed model ID in the SRS.** Store provider/model/config version in an audited configuration registry. Production selection follows benchmark and privacy review.

### Detector
Keep inference behind a versioned Python API. Compare:
1. Majority baseline.
2. TF-IDF + Logistic Regression.
3. TF-IDF + Linear SVM.
4. IndoBERT.
5. XLM-R or another multilingual candidate.

Select using group-based holdout, per-language/domain metrics, HUMAN false-positive rate, calibration, latency, and memory. Do not choose based on accuracy alone.

## 7. Deployment recommendation

### MVP deployment shape
- One Next.js web container.
- One Node worker container (can scale separately).
- One Python Detector API/worker container.
- Managed PostgreSQL.
- Managed Redis.
- Private object storage.
- External payment, email, and AI providers through server-side adapters.
- Reverse proxy/WAF and HTTPS.
- Centralized logs/metrics/traces with text redaction.

Use Docker images and environment-based configuration. Next.js supports Node server and Docker deployment; avoid a serverless-only design for the worker and inference processes.

### Region and data residency
Prefer an Indonesia region for primary database/object storage where service availability and cost permit. If a provider processes data outside Indonesia, keep production traffic blocked until the transfer basis, contract, subprocessor, retention, and safeguards are reviewed under the Privacy and Legal Readiness checklist.

### Development environment
Given the project’s low-resource laptop constraints, do not require all infrastructure and ML models to run locally at once. Run the Next.js app locally, use isolated development services/remote dev instances for Postgres and Redis, and keep model inference mocked or hosted in a development environment until needed. Never use production user text as development fixtures.

## 8. Recommended monorepo structure

```text
lexora/
├── apps/
│   ├── web/                 # Next.js UI + BFF/API routes
│   ├── worker/              # BullMQ workers and scheduled jobs
│   └── detector-api/        # Python FastAPI inference service
├── packages/
│   ├── domain/              # Domain types, rules, state machines
│   ├── db/                  # Drizzle schema and migrations
│   ├── contracts/           # Zod schemas and API/event contracts
│   ├── ui/                  # Shared UI primitives and tokens
│   └── config/              # Typed configuration
├── infra/
│   ├── docker/
│   ├── deployment/
│   └── monitoring/
├── docs/
└── plan/
```

## 9. Decisions intentionally deferred

- Exact Humanizer model/provider and model ID.
- Detector final model and threshold.
- Payment gateway final merchant contract/fees.
- Rewarded-ad provider activation and Guest eligibility.
- Email provider and sending region.
- Object storage provider/region.
- Hosting region and vendor.
- Performance/availability targets, RPO/RTO, and capacity.
- File size limits, OCR strategy, token limits, and chunking implementation.

These are not hidden assumptions. They are explicit evaluation gates for System Design and pre-production.

## 10. Official technical references

- [Next.js App Router](https://nextjs.org/docs/app) and [deployment options](https://nextjs.org/docs/app/getting-started/deploying).
- [Node.js release schedule](https://nodejs.org/en/about/previous-releases/).
- [PostgreSQL 18 documentation](https://www.postgresql.org/docs/18/).
- [BullMQ introduction and worker model](https://docs.bullmq.io/guide/introduction).
- [Better Auth sessions](https://better-auth.com/docs/concepts/session-management) and [OAuth](https://better-auth.com/docs/concepts/oauth).
- [FastAPI documentation](https://fastapi.tiangolo.com/).
- [Drizzle ORM documentation](https://orm.drizzle.team/docs/overview).
- [Midtrans Snap](https://docs.midtrans.com/docs/snap).
- [Google Ad Manager Rewarded Web](https://developers.google.com/publisher-tag/samples/display-rewarded-ad).
- [Google Ad Manager server-side verification](https://support.google.com/admanager/answer/9116812).
- [Privacy and Legal Readiness](../docs/PRIVACY-AND-LEGAL-READINESS.md).

# Task Plan: System Design and UI/UX Handoff

- **Tanggal:** 2026-11-17
- **Status:** Design baseline complete; visual generation and local tool installation remain external handoff actions.
- **Delegation:** Tahap 1–6 didelegasikan penuh; tahap 7 (website implementation) secara eksplisit tidak termasuk.
- **SRS:** Approved for System Design, review record dated 2026-11-17.

## 1. Deliverables

| Deliverable | Artifact | Status |
|---|---|---|
| User flows | `plan/USER-FLOWS.md` | Complete |
| Modular architecture | `plan/SYSTEM-DESIGN.md` | Complete |
| System flow diagrams | `plan/SYSTEM-DESIGN.md` and `plan/USER-FLOWS.md` | Complete |
| Data flow and lifecycle | `plan/DATA-FLOW-AND-DATA-LIFECYCLE.md` | Complete |
| API and event contracts | `plan/API-CONTRACTS.md` | Baseline complete |
| Technology evaluation | `plan/TECHNOLOGY-EVALUATION.md` | Complete with conditional provider gates |
| Security threat model | `plan/SECURITY-ARCHITECTURE-AND-THREAT-MODEL.md` | Baseline complete |
| Privacy/legal readiness | `docs/PRIVACY-AND-LEGAL-READINESS.md` | Checklist complete; legal review pending |
| UI/UX specification | `plan/UI-UX-SPECIFICATION.md` | Complete |
| Google Stitch prompt pack | `plan/STITCH-DESIGN-PROMPTS.md` | Complete |
| Antigravity skill setup | `docs/ANTIGRAVITY-SKILL-SETUP.md` | Commands prepared; local install not executed |

## 2. Recommended architecture

- Next.js 16.x + React 19.x + TypeScript + Node 26 LTS.
- Better Auth.
- PostgreSQL 18 + Drizzle ORM.
- Redis 8 + BullMQ worker.
- Python 3.13 + FastAPI for Detector inference.
- Provider adapter for Humanizer; OpenAI API is the first benchmark candidate, not a production selection.
- Midtrans Snap is the first payment integration candidate, subject to merchant fee/contract confirmation.
- Google Ad Manager Rewarded Web is conditional; login-only reward, SSV and account correlation must pass sandbox verification.
- Private S3-compatible object storage; provider/region subject to privacy review.
- Containerized deployment; no serverless-only architecture.

## 3. Design constraints

- Detector never claims proof of authorship and does not display uncalibrated percentages.
- MIXED and UNCERTAIN remain distinct.
- User text is not used for model training by default.
- Guest rewarded ads are disabled; Guest trial credit is non-ad, session-bound, and configurable.
- Payment and reward credits are granted only after verified, idempotent server-side events.
- Raw text is excluded from queue payloads and general logs.
- Admin raw-text access is not a default capability.
- Legal/privacy gates, child-safety assessment, and DPIA applicability must be resolved before production.

## 4. Stage 6 completion checklist

- [x] User flows cover Guest, Detector, Humanizer, profiles, payments, credits, support, Admin, privacy, and rewarded ads.
- [x] Modular architecture and service boundaries are documented.
- [x] Job, payment, credit, and deletion state transitions are documented.
- [x] Data classification, data flow, retention, and deletion propagation are documented.
- [x] API/event contracts and error catalogue are documented.
- [x] Technology alternatives and recommended stack are documented with external references.
- [x] Security threat model and release gates are documented.
- [x] UI/UX design system, screen inventory, responsive rules, accessibility, and microcopy are documented.
- [x] Google Stitch prompts are prepared for the primary MVP screens.
- [x] Skill setup instructions are prepared for local Antigravity.
- [x] Stage 7 implementation is explicitly excluded.

## 5. External handoff items (not blockers for design baseline)

1. Run UI UX Pro Max locally in Antigravity and compare generated design system with the approved tokens.
2. Generate visual mockups in Google Stitch using the prompt pack.
3. Confirm merchant rates and account eligibility with Midtrans.
4. Test Google Ad Manager Rewarded Web SSV fields in sandbox; keep ads disabled until account correlation is proven.
5. Complete privacy/legal review of provider contracts, cross-border transfer, child-safety classification, and DPIA applicability.
6. Set numerical performance/availability targets after provider and hosting selection.

These are clearly separated from completed design documentation. No production integration or website implementation has been performed.

# Lexora UI/UX Specification

- **Tanggal:** 2026-11-17
- **Status:** MVP design direction and screen specification.
- **Product:** AI Text Detector + AI Humanizer.
- **Source of truth:** SRS, Decision Log, User Flows, and System Design.
- **Implementation:** not started; this document is a design handoff.

## 1. Design direction

### Concept: Calm Editorial Intelligence

Lexora should feel like a careful writing workspace, not a novelty AI toy or an academic surveillance dashboard.

Design traits:
- Editorial, spacious, quiet, and precise.
- Strong typography and readable text surfaces.
- Deep teal as the primary brand color.
- Neutral surfaces; color is reserved for status and actions.
- Minimal decoration; no default purple-to-blue gradients, glassmorphism, or card nesting.
- Explain limitations where users make decisions.
- Keep the user's original text visible and under their control.

### Brand voice
- Clear and measured.
- Never claim that Detector proves who wrote a text.
- Explain what happened, what is uncertain, and what the user can do next.
- Prefer concise Indonesian copy, with English localization available.

Suggested tagline: **“Analisis tulisan. Revisi dengan kendali.”**

## 2. Design tokens

### Color palette

| Token | Value | Usage |
|---|---|---|
| Brand 900 | `#134E4A` | Strong brand text/hover |
| Brand 700 | `#0F766E` | Primary action |
| Brand 600 | `#0D9488` | Active states |
| Brand 100 | `#DDF3EF` | Soft brand surface |
| Canvas | `#F7F8F7` | App background |
| Surface | `#FFFFFF` | Cards, editor panels |
| Surface muted | `#EEF2F0` | Secondary panels |
| Text primary | `#17231F` | Main text |
| Text secondary | `#66736E` | Supporting text |
| Border | `#DCE5E1` | Dividers and outlines |
| Info | `#2563EB` | Informational status |
| Success | `#15803D` | Successful operation |
| Warning | `#B45309` | Uncertain/attention |
| Danger | `#B42318` | Destructive/error |
| Mixed | `#6D5BD0` | MIXED result distinction only |

Rules:
- Do not use color alone to communicate Detector labels or payment/job status.
- AI/HUMAN are not green/red moral judgments. Use neutral label treatments and clear text.
- UNCERTAIN uses a warning treatment with an explanation.
- MIXED uses a distinct label, never as a synonym for uncertainty.
- Every color pair must pass WCAG 2.2 AA contrast testing.

### Typography

- Display/headings: **Plus Jakarta Sans**, 600–700.
- Body/UI: **Inter**, 400–600.
- IDs, hashes, counters, and technical metadata: **JetBrains Mono**.
- Body size 16px baseline; helper text no smaller than 12px where essential.
- Use tabular numerals for counters, credit amounts, and timestamps.

### Spacing and shape

- Base spacing unit: 4px.
- Content max width: 1,280px public; 1,440px app workspace.
- Main sidebar: 240px desktop.
- Admin sidebar: 256px desktop.
- Header: 64px.
- Panel radius: 14px.
- Input/button radius: 10px.
- Card border: 1px neutral; shadow only for overlays and elevated surfaces.
- Button and touch target height: 44px minimum.
- Editor line-height: 1.6.

## 3. Navigation and information architecture

### Public site
- Home
- AI Text Detector
- AI Humanizer
- Pricing
- How it works
- Help/FAQ
- Privacy and Terms
- Login / Register

### User application
- Overview
- AI Text Detector
- AI Humanizer
- Style Profiles
- History
- Credits & Transactions
- Notifications
- Support
- Privacy Center
- Account Settings

### Admin application
- Overview
- Users
- Detector/Humanizer operations
- Jobs and failed queue
- Transactions and reconciliation
- Credit ledger
- Packages and reward configuration
- AI provider/model configuration
- Support tickets
- Sensitive access requests
- Audit logs
- Service status
- Roles and permissions (Super Admin only)

## 4. Public landing page

### Layout
1. Header with Lexora wordmark, navigation, Login, and primary CTA.
2. Hero:
   - Headline: “Pahami tulisanmu. Perbaiki dengan kendali.”
   - Supporting line: “Analisis pola tulisan dengan hati-hati, lalu rapikan teks tanpa kehilangan kendali atas maknanya.”
   - Primary CTA: “Coba AI Detector”.
   - Secondary CTA: “Gunakan Humanizer”.
3. Two product panels:
   - Detector: analysis, sentence-level explanation, limitations.
   - Humanizer: style control, personal profiles, before/after comparison.
4. How it works: Input → Analyze/Rewrite → Review → Export.
5. Privacy and trust section: no default model-training use; user controls; Detector is not proof.
6. Pricing/credit overview, values loaded from effective configuration.
7. FAQ and footer.

Avoid a fake live demo that implies a model result without running a real, clearly labeled demo pipeline.

## 5. User application shell

### Desktop wireframe

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Lexora                                      Credits  • Notifications • Avatar │
├──────────────────┬───────────────────────────────────────────────────────────┤
│ Overview         │ Page title                                  Help / status │
│ Detector         │                                                           │
│ Humanizer        │ Main content area                                         │
│ Style Profiles   │                                                           │
│ History          │                                                           │
│ Credits          │                                                           │
│ Support          │                                                           │
│ Privacy Center   │                                                           │
│ Settings         │                                                           │
└──────────────────┴───────────────────────────────────────────────────────────┘
```

### Mobile
- Compact header with brand and account actions.
- Bottom navigation: Home, Detector, Humanizer, Account.
- Secondary pages are reached through Account/More.
- Editor controls remain sticky only when they do not obscure content.
- Tables collapse into labeled cards; never require horizontal scrolling for primary actions.

## 6. Dashboard

Content order:
1. Welcome + account status.
2. Available credit balance and “Top up” action.
3. Two primary action cards: Detector and Humanizer.
4. Recent jobs with status, timestamp, and open-result action.
5. Style profile summary (registered accounts only).
6. Notifications/support shortcut.
7. Privacy notice/update banner when needed.

Empty state should explain the first useful action, not show decorative charts without data.

## 7. AI Text Detector screen

### Input state
- Large text editor with placeholder: “Tempel tulisan yang ingin dianalisis…”
- Upload button for TXT, DOCX, PDF.
- Character counter using extended grapheme clusters, maximum 20,000.
- Language hint selector is optional; detected language remains authoritative.
- Credit estimate shown before confirmation.
- Primary action: “Analisis tulisan”.
- Short-text warning is advisory; no hard minimum rejection.
- File extraction errors must preserve any existing editor content.

### Processing state
- Show job status and a progress description based on real stages.
- Do not invent percentage progress if the backend cannot measure it.
- Provide cancel action when job state permits.
- Explain that the page can be left and result revisited if job persistence supports it.

### Result state

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Hasil analisis                                                               │
│ [MIXED]  /  [HUMAN]  /  [AI]  /  [UNCERTAIN]                                 │
│ Ringkasan: ...                                                               │
│ Peringatan: Hasil ini bukan bukti pasti asal tulisan.                        │
├──────────────────────────────────────────────────────────────────────────────┤
│ Analisis per kalimat                                                        │
│ 01  [HUMAN]     Kalimat sumber ...             Penjelasan ...                 │
│ 02  [UNCERTAIN] Kalimat sumber ...             Bukti belum cukup ...          │
│ 03  [AI]        Kalimat sumber ...             Penjelasan ...                 │
├──────────────────────────────────────────────────────────────────────────────┤
│ [Salin ringkasan] [Unduh TXT] [Unduh DOCX] [Unduh PDF] [Buka Humanizer]       │
└──────────────────────────────────────────────────────────────────────────────┘
```

Rules:
- Never show a numeric probability/percentage in MVP.
- Show limitations and warnings near the result label, not hidden in a tooltip.
- Each sentence row preserves source order and exact source text.
- A sentence without enough context is UNCERTAIN.
- MIXED requires evidence for both patterns in different segments.
- The handoff to Humanizer is an explicit user action.

## 8. AI Humanizer screen

### Layout
- Top controls: built-in style, personal profile, tone/strength if approved by SRS, estimate.
- Main editor: source and result panes.
- Source remains unchanged.
- Result shows generated text with a clear copy/download action.
- Diff/compare view can highlight changes, but must not imply factual correctness.
- Character count range: 100–50,000 extended grapheme clusters.
- “Save to history” is explicit; no silent permanent saving.
- File format on download follows the source file format where applicable.

### Wireframe

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ Humanizer     Style [Natural ▼] Profile [None ▼]      Estimate  •  Run        │
├────────────────────────────────┬─────────────────────────────────────────────┤
│ Original text                  │ Humanized result                            │
│                                │                                             │
│ Editable source                │ Generated output                            │
│                                │                                             │
├────────────────────────────────┴─────────────────────────────────────────────┤
│ [Compare changes] [Copy result] [Download] [Save to history]                 │
└──────────────────────────────────────────────────────────────────────────────┘
```

Error behavior:
- Extraction failure leaves the old editor content untouched.
- Provider failure releases/refunds credits according to the ledger rules.
- A retry is a new user-confirmed action unless the worker performs a safe automatic retry.
- Show a warning when the result may alter meaning; users remain responsible for reviewing it.

## 9. Style Profiles

- Profile list shows name, status, sample count, and main-profile marker.
- Create profile flow has sample upload/paste, per-sample counter, provenance/consent notice, and quality evaluation.
- Show “3 samples minimum” as a hard gate, not a promise of activation.
- Adaptive evaluation can request more samples.
- Maximum 20 samples/profile and six profiles/account.
- Sample states: Active, Recently Deleted, Restored, Purged.
- Profile deletion is distinct from sample deletion and has a clear confirmation.
- Never label a profile “Ready” before the adaptive assessment passes.

## 10. Credits and payments

- Balance card shows available balance, reserved balance, and expiring credits.
- Ledger view shows source, amount, status, creation, and expiry.
- Package cards use effective server-side configuration; never hardcode price in UI.
- Checkout clearly shows amount, currency, package, payment method, and transaction status.
- Payment success is shown only after backend verification.
- Pending state explains that the payment provider is still confirming.
- Rewarded ads are login-only in MVP and optional, only displayed when enabled and eligible.
- Guest sees sign-in or a configured non-ad trial grant, not an ad reward.
- Before a rewarded ad starts, show the reward, conditions, expiry, and non-transferability.
- Never show an ad as a blocking step in payment checkout or an active AI job.

## 11. Support, notifications, and Privacy Center

### Support
- Ticket list with category, ID, status, last update.
- Ticket detail with chronological messages and status.
- No attachment uploader in MVP.
- Resolved ticket can be reopened within seven calendar days.

### Notifications
- Notification center with read/unread states.
- Separate preferences for optional categories.
- Security and essential transaction notifications remain enabled.
- Promotional opt-in is separate.

### Privacy Center
- Consent preferences with version and purpose.
- Data export request.
- Account/data deletion request.
- Access/correction/deletion/objection request status.
- Processor/retention explanation and contact channel.

## 12. Admin Panel

- Separate route and visual shell; no user-facing navigation leakage.
- Dense but readable tables with search, filters, and pagination.
- Every privileged action requires confirmation and a reason.
- Role-specific navigation hides unavailable actions and backend permission checks remain authoritative.
- Sensitive text is not shown in tables, search previews, or analytics.
- Sensitive access request page shows ticket, consent, object scope, expiry, and audit state.
- No raw text access by default for any role.
- Credit adjustments create ledger entries; never edit balances in place.

## 13. Components

- App shell, sidebar, topbar, breadcrumbs.
- Primary/secondary/ghost/destructive buttons.
- Form field, text area, file dropzone, character counter.
- Credit balance chip and estimate panel.
- Job status stepper and cancellation control.
- Result label and limitation callout.
- Sentence analysis row.
- Diff viewer.
- Profile/sample card and evaluation state.
- Transaction table and payment status.
- Ticket thread and status control.
- Notification item and preference switch.
- Privacy request timeline.
- Admin audit table and sensitive-access dialog.

## 14. Interaction and motion

- Use short 120–180ms transitions for hover/focus/expand.
- Avoid scroll-jacking, parallax, and animation that delays critical actions.
- Respect `prefers-reduced-motion`.
- Loading states should reflect real operations; skeletons only where layout is known.
- Destructive actions use explicit confirmation with the consequence stated.
- Toasts are supplementary; persistent status remains in the page.

## 15. Accessibility

Target WCAG 2.2 AA:
- Keyboard-only completion for every primary flow.
- Visible focus indicator and logical focus order.
- Semantic headings, labels, tables, and landmarks.
- Screen-reader announcements for job status and validation errors.
- Contrast at least 4.5:1 for normal text and 3:1 for large text/UI components where required.
- No color-only status communication.
- Touch targets designed at 44×44px or larger.
- Modal focus trap, Escape behavior, and focus restoration.
- Accessible error summaries and inline field messages.
- Test zoom/reflow and reduced motion.
- Review screen-reader behavior on Detector results, Humanizer editor, payment, and Admin tables.

## 16. UI copy baseline

| Context | Copy |
|---|---|
| Detector disclaimer | “Hasil ini menunjukkan pola teks, bukan bukti pasti siapa penulisnya.” |
| UNCERTAIN | “Bukti belum cukup untuk memberi kesimpulan yang andal.” |
| Unsupported language | “Bahasa teks ini belum didukung untuk analisis kepengarangan.” |
| MIXED | “Ada indikasi pola HUMAN dan AI pada bagian teks yang berbeda.” |
| Insufficient credits | “Saldo kredit belum cukup untuk estimasi ini.” |
| Payment pending | “Pembayaran sedang dikonfirmasi oleh penyedia pembayaran.” |
| Humanizer caution | “Periksa kembali fakta, angka, kutipan, dan makna sebelum menggunakan hasil.” |
| Profile evaluation | “Sampel sudah terkumpul. Kami sedang memeriksa konsistensi gaya.” |
| Sensitive Admin access | “Akses ini dibatasi pada dokumen dan tiket yang disetujui, lalu berakhir otomatis.” |

W3C reference: [Web Content Accessibility Guidelines (WCAG) 2.2](https://www.w3.org/TR/WCAG22/).

## 17. Design skill usage

Reviewed project-provided skill sources:
- **UI UX Pro Max:** recommended for design-system exploration and visual pattern selection. It has an Antigravity-specific initialization path; use it during local design exploration.
- **Impeccable:** recommended for critique, accessibility/responsive audit, and polish when the UI implementation exists. Its documented installer supports Google Antigravity.
- **Huashu Design:** not selected for the core SaaS UI; its strongest use cases are launch animation, interactive prototypes, motion pieces, and presentation artifacts.
- **Stop Slop:** useful for reviewing public copy and documentation, not a UI component system.
- **Task Observer:** useful for recording workflow observations; project observations should remain in the repository log.

The local Antigravity installation was not modified from this remote repository session. Setup instructions are recorded separately.

## 18. Design handoff checklist

- [ ] Generate a design-system preview in Antigravity using the approved tokens.
- [ ] Create desktop and mobile wireframes for all MVP flows.
- [ ] Validate color contrast and focus behavior.
- [ ] Validate Detector labels and disclaimers with no numeric score.
- [ ] Validate Humanizer editor behavior and source preservation.
- [ ] Validate payment pending/failed/paid states.
- [ ] Validate privacy and sensitive Admin access states.
- [ ] Review with accessibility tooling and manual keyboard/screen-reader tests.
- [ ] Freeze design tokens and component variants before frontend implementation.

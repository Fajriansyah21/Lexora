# Google Stitch Design Prompt Pack — Lexora

- **Tanggal:** 2026-11-17
- **Purpose:** generate visual UI concepts from the approved UX specification.
- **Authoritative source:** [UI/UX Specification](UI-UX-SPECIFICATION.md).
- **Important:** Stitch output is a visual proposal. It must not override SRS behavior or Decision Log rules.

## 1. Global design prompt

```text
Design a responsive SaaS web application named Lexora, an Indonesian-first AI writing workspace with two tools: AI Text Detector and AI Humanizer.

Visual direction: Calm Editorial Intelligence. Make it feel like a careful writing workspace, not a generic AI startup template. Use a warm off-white canvas (#F7F8F7), white surfaces, deep teal primary (#0F766E), dark ink text (#17231F), muted gray-green secondary text (#66736E), thin neutral borders (#DCE5E1), and minimal shadows. Avoid purple/blue gradients, glassmorphism, excessive rounded cards, decorative charts, and unnecessary illustrations.

Typography: Plus Jakarta Sans for headings and Inter for body/UI. Use a clear hierarchy, readable 16px body text, and tabular numerals for counters/credits.

Layout: spacious editorial grid, clear alignment, 240px desktop app sidebar, 64px topbar, content max width 1440px. Mobile layout must be intentionally designed, not merely compressed.

Accessibility: WCAG 2.2 AA, visible focus, keyboard-friendly controls, clear labels, high contrast, no color-only status, 44px touch targets, reduced-motion support.

Brand voice: concise, measured, helpful Indonesian. Never claim the Detector proves authorship. Never show an uncalibrated numeric authorship percentage. Use explicit UNCERTAIN and MIXED states.

Use the UI/UX specification as the behavior source. Generate coherent reusable components and consistent spacing/tokens across all screens.
```

## 2. Landing page

```text
Create the Lexora public landing page for desktop and mobile.

Header: Lexora wordmark, Produk, Cara Kerja, Harga, Bantuan, Login, and primary CTA.

Hero headline: “Pahami tulisanmu. Perbaiki dengan kendali.”
Supporting copy: “Analisis pola tulisan dengan hati-hati, lalu rapikan teks tanpa kehilangan kendali atas maknanya.”
Primary CTA: “Coba AI Detector”. Secondary CTA: “Gunakan Humanizer”.

Below the hero, show two clear product sections:
1. AI Text Detector: analyze text patterns, show sentence-level explanations, communicate uncertainty and limitations.
2. AI Humanizer: revise text with style control, optional personal profile, and original/result comparison.

Include a concise how-it-works section, privacy/trust section, configurable pricing preview, FAQ, and footer. Do not invent user counts, accuracy claims, testimonials, or fake live results.
```

## 3. User dashboard

```text
Create the authenticated Lexora dashboard.

Use the shared app shell: 240px left sidebar, 64px topbar, account avatar, notification entry, and credit balance.

Main content:
- Welcome message.
- Credit balance card with Top Up action.
- Two primary tool cards: AI Text Detector and AI Humanizer.
- Recent jobs list with real status labels and timestamps.
- Style Profile summary.
- Support and Privacy Center shortcuts.

Avoid vanity metrics or charts when there is no real data. Include a thoughtful empty state for a new user.
```

## 4. AI Text Detector

```text
Create the AI Text Detector workspace.

Input screen:
- Large text area with placeholder “Tempel tulisan yang ingin dianalisis…”
- Upload TXT/DOCX/PDF action.
- Extended grapheme character counter with 20,000 maximum.
- Optional language hint.
- Credit estimate and “Analisis tulisan” CTA.
- Short text warning is advisory only; do not show a hard minimum.

Result screen:
- Clear label: HUMAN, AI, MIXED, or UNCERTAIN.
- No numeric score, no percentage, no probability meter.
- Show a nearby disclaimer: “Hasil ini menunjukkan pola teks, bukan bukti pasti siapa penulisnya.”
- Sentence-level list preserving original order and source text.
- Clear distinction between UNCERTAIN and MIXED.
- Export TXT/DOCX/PDF and explicit “Buka Humanizer” handoff.

Use neutral labels; do not imply HUMAN is morally good or AI is misconduct.
```

## 5. AI Humanizer editor

```text
Create the Lexora Humanizer editor.

Use a focused two-pane workspace:
- Left: original source text, editable, unchanged until user edits.
- Right: generated Humanizer result.
- Top controls: built-in style dropdown, personal profile dropdown, character count, credit estimate, primary Run action.
- Bottom actions: Compare changes, Copy result, Download, Save to history.

Show the 100–50,000 extended grapheme cluster range. Add a subtle warning: “Periksa kembali fakta, angka, kutipan, dan makna sebelum menggunakan hasil.”

Do not show a fake quality score or promise that the result is undetectable. Keep the editor readable on mobile by switching to tabs or stacked panels.
```

## 6. Style Profiles

```text
Create a Style Profiles management page.

Show profile cards with name, main-profile marker, status, and sample count. Include a create-profile flow with sample upload/paste, per-sample character counter, minimum three eligible samples, adaptive quality evaluation, and a clear “more samples needed” state.

Show maximum 20 samples per profile and six profiles per account. Sample deletion and profile deletion must be visually distinct. Include Recently Deleted for samples only, with a 30-day recovery window. Do not show a restore action for a permanently deleted profile.
```

## 7. Credits and checkout

```text
Create a Credits & Transactions page.

Show available balance, reserved balance, expiring credit lots, and an append-only transaction ledger. Package cards should use placeholders for server-configured price and credit amounts, not invented values.

Checkout must clearly show package, amount, currency, selected payment method, and pending/paid/failed states. Do not show payment success until the backend verifies the provider callback.

Rewarded ads are optional and login-only for MVP. Guest users see sign-in or configured non-ad trial credit, not an ad reward. Before a rewarded ad, show exact reward, expiry, and non-transferability.
```

## 8. Support and Privacy Center

```text
Create Support and Privacy Center pages using the same Lexora app shell.

Support: ticket list, status, ticket ID, chronological message thread, and clear reopen window. Do not include a file attachment uploader in MVP.

Privacy Center: consent preferences separated by purpose, data export request, data deletion request, access/correction/deletion/objection request status, and a clear explanation of processors and retention. Keep the interface understandable and avoid legal-wall copy.
```

## 9. Admin Panel

```text
Create a separate Lexora Admin Panel shell with a restrained operational interface.

Navigation: Overview, Users, Jobs, Payments, Credit Ledger, Support, Provider Configuration, Sensitive Access Requests, Audit Logs, Operations, Roles & Permissions.

Use dense but readable tables, filters, pagination, status chips, and explicit confirmation dialogs. Show no raw user text in tables or previews. Sensitive text access is not a default Admin capability; show scoped, consented, time-limited access requests only.

Every privileged action requires a reason and leaves an audit record. Make Super Admin, Admin, and Moderator roles visually and functionally distinct.
```

## 10. Output review checklist

- [ ] The visual system matches the global prompt.
- [ ] Desktop and mobile layouts are both coherent.
- [ ] Detector does not show percentages or proof claims.
- [ ] MIXED and UNCERTAIN are distinct.
- [ ] Humanizer preserves the original pane and shows comparison.
- [ ] Guest rewarded ads are absent.
- [ ] Payment success is not shown before verification.
- [ ] Admin has no default raw-text preview.
- [ ] Privacy Center exposes consent and request status.
- [ ] Color contrast, focus, and keyboard states are represented.
- [ ] All price/credit values remain placeholders until configured.

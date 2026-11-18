# Stage 7 Implementation Mandate — Lexora

- **Tanggal:** 2026-11-18
- **Status:** **Authorized (Revised Final)**
- **Referensi:** SRS, System Design, Technology Evaluation, API Contracts, Security Architecture, Data Flow.

## 1. Otorisasi Stage 7

Implementasi website Lexora (Stage 7) telah resmi diotorisasi mulai tanggal 18 November 2026. Tahap ini menandai transisi dari fase desain dan riset sintetis ke fase pembangunan aplikasi fungsional.

## 2. Tujuan dan Batasan Implementasi

### Tujuan utama
- Membangun aplikasi web Lexora fungsional yang mencakup modul **AI Text Detector** dan **AI Humanizer**.
- Mengimplementasikan infrastruktur pendukung: autentikasi, manajemen kredit, pembayaran, profil gaya, riwayat, pusat bantuan, panel admin, dan privasi.
- Menghasilkan sistem yang aman, privat, dan sesuai dengan spesifikasi desain "Calm Editorial Intelligence".

### Batasan tegas
- **Cakupan MVP:** Hanya modul Detector dan Humanizer. Modul DOCX Metadata Cleaner tetap **out of scope**.
- **No Drive-by Refactor:** Fokus pada implementasi sesuai System Design. Jangan melakukan refactor pada modul riset dataset tanpa alasan kuat.
- **Data Privacy:** Jangan pernah menyimpan teks mentah pengguna dalam log, queue payload, atau URL.
- **Provider & Technology Status:** Ikuti status klasifikasi pada dokumen sumber (Recommended/Candidate). Tidak ada teknologi yang dianggap final sebelum evaluasi teknis/biaya spesifik milestone disetujui.
- **Visual Baseline:** Ikuti desain yang telah dibekukan secara kondisional di `docs/DESIGN-FREEZE-REVIEW-2026-11-18.md`.

## 3. Status Arsitektur dan Teknologi

Berdasarkan `plan/TECHNOLOGY-EVALUATION.md`, `plan/SYSTEM-DESIGN.md`, dan `plan/DECISION-LOG.md`:

### Rekomendasi Arsitektur (Baseline)
- **Architecture:** Modular Monolith dengan background worker (Node.js) dan inference service (Python FastAPI).
- **Frontend/BFF:** Next.js 16.x (App Router), React 19.x, Tailwind CSS 4.x, shadcn/ui.
- **Backend Core:** Node.js 26 LTS, Better Auth, Drizzle ORM.
- **Database & Queue:** PostgreSQL 18, Redis 8 + BullMQ.
- **Inference:** Python 3.13 + FastAPI.
- **Monorepo:** pnpm workspaces + Turborepo.

### Status Keputusan Penting
- **Payment:** Midtrans Snap telah dipilih sebagai integrasi pembayaran pertama (DEC-183). Aktivasi tetap bersyarat pada: merchant onboarding, written fee quote, settlement/refund review, dan webhook sandbox tests.
- **AI Humanizer:** OpenAI API (Kandidat Utama/Conditional). Model final menunggu benchmark (DEC-185).
- **Conditional Gated:** Hosting & Storage Region (menunggu review legal/privacy), Rewarded Ads (menunggu SSV & policy approval).
- **Skema Kredit:** Sesuai Decision Log (DEC-001 s/d DEC-189), mencakup lot, ledger, reservation, settlement, dan expiry.

## 4. Prinsip Keamanan dan Privasi

- **Least Privilege:** Akses admin dibatasi oleh peran, izin, dan 2FA.
- **Auditability:** Setiap mutasi kredit, akses admin, dan perubahan konfigurasi harus dicatat.
- **Data Isolation:** Upload file masuk karantina; ekstraksi di sandbox; penyimpanan di private object storage.
- **No-Training-by-Default:** Konten pengguna tidak digunakan untuk training model tanpa persetujuan eksplisit.
- **Idempotency:** Semua side-effect (pembayaran, kredit, reward) harus idempotent.

## 5. Milestone Stage 7 (M0 - M7)

### M0: Formalisasi Mandat dan Implementation Readiness
- **Deliverables:** Mandat disahkan, dokumen pendukung selaras, roadmap diperbarui.
- **Dependencies:** Stage 1-6 design freeze.
- **Acceptance Criteria:** Mandat ditandatangani project owner; roadmap mencerminkan milestone yang disetujui.
- **Verification:** Git diff review pada AGENTS.md, ACTIVE-ROADMAP.md, dan docs/.

### M1: Project Bootstrap dan Fondasi Proyek
- **Scope:** Struktur monorepo, konfigurasi tooling (pnpm, turbo), linting/formatting (ESLint, Prettier), testing framework (Vitest/Pytest), CI dasar, dokumentasi setup development.
- **Non-Scope:** Implementasi bisnis/domain logic.
- **Dependencies:** M0 Approval.
- **Acceptance Criteria:** `pnpm install` berhasil; linter/format lulus; `pnpm test` menjalankan dummy test; CI pipeline (GitHub Actions) hijau.
- **Verification:** Periksa file konfigurasi (root/packages); log CI.

### M2: Database dan Backend Foundation
- **Scope:** Database schema (Drizzle), migrations, authentication (Better Auth), authorization logic, domain services baseline, backend API foundation, security baseline (headers, CORS, rate limiting).
- **Non-Scope:** Integrasi provider AI atau payment.
- **Dependencies:** M1 Approval.
- **Acceptance Criteria:** Migrasi berhasil di local/dev DB; login/logout fungsional; API endpoint mengembalikan response terproteksi 401 tanpa session.
- **Verification:** Drizzle studio/SQL check; test suite autentikasi.

### M3: AI Text Detector
- **Scope:** FastAPI inference service, job queue (BullMQ), integrasi worker, estimasi karakter, hasil analisis per kalimat, metadata versi model.
- **Non-Scope:** Humanizer logic.
- **Dependencies:** M2 Approval.
- **Acceptance Criteria:**
  1. Pipeline API, queue, worker, dan database terbukti melalui mock integration.
  2. Integrasi model nyata berhasil setelah keputusan model disetujui.
  3. Lulus benchmark dan validasi kualitas sebelum hasil Detector dinyatakan siap produksi (Mock bukan bukti kualitas model).
- **Verification:** Integration test (API -> Queue -> Worker -> DB); Benchmark report.

### M4: AI Humanizer
- **Scope:** Provider adapter framework, integrasi kandidat AI provider (mock/dev), manajemen profil gaya dan sampel, evaluasi kualitas adaptif, snapshot versi profil.
- **Non-Scope:** Payment gateway integration.
- **Dependencies:** M3 Approval.
- **Acceptance Criteria (DEC-157):**
  1. Reservasi dilakukan sebelum pekerjaan masuk antrean.
  2. Jika berhasil, settlement berdasarkan konsumsi yang dapat diverifikasi; sisa reservasi dilepaskan.
  3. Jika gagal sebelum hasil diberikan, seluruh reservasi dilepaskan.
  4. Pembatalan ketika provider telah memproses mengikuti aturan biaya terverifikasi.
- **Verification:** Test suite profil gaya; Humanizer worker integration test; Ledger settlement check.

### M5: Sistem Pendukung (Credits, Payment, Support, Privacy, Admin)
- **Scope:** Credit ledger (lot/ledger entries), Payment integration (setelah aktivasi bersyarat Midtrans disetujui), Support ticket system, Privacy request workflow, Admin panel core.
- **Non-Scope:** UI Dashboard lengkap.
- **Dependencies:** M4 Approval, Merchant Approval (Midtrans).
- **Acceptance Criteria:** Top-up kredit menambah saldo via verified webhook; reservasi kredit dilakukan sebelum job AI; audit log mencatat aksi admin.
- **Verification:** Ledger consistency check; webhook simulation.

### M6: Integrasi Frontend dan Backend
- **Scope:** Implementasi halaman UI (Landing, Dashboard, Editor) sesuai Stitch baseline; integrasi API penuh; user history; penanganan error dan loading states.
- **Non-Scope:** Production deployment.
- **Dependencies:** M5 Approval.
- **Acceptance Criteria:** Navigasi fungsional sesuai User Flows; data riwayat muncul di dashboard; editor dapat mengirim/menerima hasil AI secara visual.
- **Verification:** Manual walkthrough; frontend integration tests.

### M7: Quality Assurance dan Deployment Readiness
- **Scope:** End-to-end testing, security review (SAST/DAST), browser visual QA, WCAG 2.2 AA review, performance benchmarking, deployment automation.
- **Dependencies:** M6 Approval.
- **Acceptance Criteria:**
  1. Seluruh 275 AC memiliki status yang dapat ditelusuri.
  2. AC yang dapat diuji wajib lulus; AC yang blocked tetap tercatat sebagai blocked.
  3. Kriteria WCAG 2.2 AA lulus melalui pengujian otomatis dan manual.
  4. Tidak ada launch-blocker yang memengaruhi keamanan, privasi, legal, atau fungsi inti.
- **Verification:** Test reports; audit security log; accessibility checklist.

## 6. Mandatory Review Gate

1. **Persetujuan Milestone:** Persetujuan project owner wajib diperlukan sebelum setiap perpindahan milestone.
2. **Keputusan Kritis:** Setiap keputusan yang memengaruhi biaya (provider), keamanan, privasi, atau arsitektur wajib mendapatkan persetujuan eksplisit sebelum implementasi keputusan tersebut dilakukan.
3. **Audit Regresi:** Setiap perubahan pada skema dataset sintetis (Stage 5) harus melalui regression test (29/29 lulus).

**Dilarang keras memulai M1 sebelum M0 dinyatakan selesai dan disetujui oleh project owner.**

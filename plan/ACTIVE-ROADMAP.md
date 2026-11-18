# Lexora Active Roadmap

Terakhir diperbarui: 2026-11-18

## Cakupan produk MVP

Keputusan **DEC-001** menetapkan dua modul untuk MVP pertama:
1. AI Text Detector.
2. AI Humanizer.

DOCX Metadata Cleaner ditunda ke fase setelah MVP. Arsitektur produk tetap modular, tetapi infrastruktur untuk modul yang ditunda tidak perlu dibangun sekarang. Sistem referral dan fitur perbandingan dua teks mandiri juga tidak masuk MVP berdasarkan DEC-010.

## Status analisis kebutuhan sistem

SRS berstatus **Approved for System Design** melalui delegated project lead review pada 2026-11-17. Lihat [SRS Review Record](../docs/SRS-REVIEW-AND-APPROVAL-2026-11-17.md) dan [Requirements Elicitation Status](REQUIREMENTS-ELICITATION-STATUS.md).

Posisi dokumentasi pada 2026-11-17:
- 189 catatan keputusan: 187 Accepted dan 2 Superseded (DEC-018 dan DEC-019).
- 276 requirement unik dalam SRS: 255 FR dan 21 NFR. Distribusi: GEN 9, FILE 9, DET 17, HUM 124, ACC 21, CRED 25, PAY 9, SUP 8, NOT 8, OPS 12, ADM 13.
- Audit requirement Humanizer selesai; gap teknis provider/model, token/chunking, benchmark kualitas, dan retensi teknis tercatat sebagai pekerjaan desain/pre-production.
- Audit requirement Detector selesai dengan 17 FR; model, threshold, kalibrasi, dan target kualitas memerlukan benchmark.
- Audit modul pendukung selesai; harga/unit economics, merchant terms, provider, permission matrix rinci, dan target operasional tetap conditional.

SRS siap menjadi dasar System Design. Detail provider, harga, retensi legal, token limits, dan target operasional tetap harus ditentukan/diuji pada tahap desain sebelum implementasi atau produksi. Ringkasan status bukan pengganti SRS atau Decision Log.

## Tahap perencanaan sistem MVP

| Tahap | Pekerjaan | Status | Bukti |
|---:|---|---|---|
| 1 | Audit requirement Humanizer | Complete | Humanizer Requirements Audit |
| 2 | Elisitasi/audit AI Text Detector | Complete | Detector Requirements Audit |
| 3 | Audit modul pendukung dan NFR | Complete | Supporting Modules Requirements Audit |
| 4 | Acceptance criteria | Complete baseline | 275 AC aktif + 55 skenario Gherkin |
| 5 | Review dan pengesahan SRS | Approved for System Design | SRS Review Record |
| 6 | User flow, System Design, teknologi, keamanan, UI/UX | Conditional Design Freeze v1.0; browser visual QA/WCAG review pending | [Design Freeze Review](../docs/DESIGN-FREEZE-REVIEW-2026-11-18.md) |
| 7 | Pembangunan website (Stage 7) | **Authorized / In Progress** | [Stage 7 Mandate](../docs/STAGE-7-IMPLEMENTATION-MANDATE-2026-11-18.md) |

### Milestone Stage 7 (Website Implementation)

| Milestone | Pekerjaan | Status |
|---|---|---|
| M0 | Formalisasi Mandat dan Implementation Readiness | **Completed** (2026-11-18) |
| M1 | Project Bootstrap dan Fondasi Proyek | **In Progress (Current)** |
| M2 | Database dan Backend Foundation | Not Started |
| M3 | AI Text Detector | Not Started |
| M4 | AI Humanizer | Not Started |
| M5 | Sistem Pendukung (Credits, Payment, Support, Privacy, Admin) | Not Started |
| M6 | Integrasi Frontend dan Backend | Not Started |
| M7 | Quality Assurance dan Deployment Readiness | Not Started |

Tahap 1–5 selesai. Tahap 6 memiliki baseline dokumentasi dan delapan ekspor visual yang telah direview. Desain dibekukan secara kondisional sebagai acuan frontend; browser visual QA, screenshot refresh, dan verifikasi WCAG 2.2 AA masih menjadi gerbang eksternal. Instalasi skill lokal Antigravity belum dijalankan. Tahap 7 (pembangunan website) diotorisasi dan dijalankan secara bertahap melalui milestone M0 sampai M7 dengan mandatory review gate per perpindahan milestone.

## Fokus riset aktif: uji prosedur sintetis dataset

Jalur riset dataset tetap berjalan terpisah dari analisis sistem produk. Pengembangan requirement produk tidak membatalkan gerbang metodologi dataset sebelum pilot nyata dan training detector.

### Task pengujian

| Urutan | Pengujian | Bukti yang harus dihasilkan | Status |
|---:|---|---|---|
| 1 | JSON Schema | Draft 2020-12 schema check; fixture valid dan 5 mutasi invalid | Verified (6 test methods) |
| 2 | Sentence offset | Substring, batas, overlap, Unicode combining mark, emoji, CRLF, tab, dan teks kosong | Verified (5 tests) |
| 3 | Editing history & lineage | Parent-child, parent hilang, ID duplikat, siklus, urutan, timestamp, dan riwayat kosong | Verified (8 tests) |
| 4 | Deduplikasi | Exact, normalized exact, near-duplicate candidate, Unicode normalization, dan false-merge guard | Verified (4 tests) |
| 5 | Group-based split | Group/pair integrity, missing group, deterministic assignment, dan explicit challenge holdout | Verified (6 tests) |

Harness tersedia di `scripts/synthetic_dataset_checks.py` dengan fixture dan 29 test cases di `tests/synthetic_dataset/`. Pengujian lokal awal menghasilkan 27/27 lulus; setelah integrasi template-to-export ditambahkan, suite diperluas dan diverifikasi di GitHub Actions. Workflow GitHub Actions run #4 berhasil pada commit `f7c0a620f68e41c8f72c8f966c8a903ca8e55c96`: 29/29 test lulus pada Python 3.12.16 dan jsonschema 4.26.0. Termasuk uji mapping editing-history template ke export schema. [Log CI](https://github.com/Fajriansyah21/Website-AI-Ditector/actions/runs/44026960961).

## Gerbang kelulusan pengujian sintetis

Tahap ini hanya dapat ditandai **Verified** jika:
- [x] Fixture valid diterima dan fixture invalid ditolak sesuai alasan yang diharapkan.
- [x] Offset setiap kalimat menunjuk tepat ke substring sumber, dengan konvensi indeks yang konsisten.
- [x] Editing history membentuk lineage yang dapat ditelusuri dan menolak referensi versi yang rusak.
- [x] Deduplikasi mendeteksi duplikat tanpa menggabungkan teks berbeda yang hanya mirip secara wajar.
- [x] Group-based split menjaga semua pasangan, turunan, dan kelompok terkait berada pada split yang sama.
- [x] Pengujian dapat diulang dengan command terdokumentasi dan menghasilkan output yang dapat diperiksa.
- [x] Kegagalan dan keterbatasan dicatat, bukan disembunyikan.

Bukti dan keterbatasan: `tests/synthetic_dataset/README.md`, `docs/EDITING-HISTORY-MAPPING-v1.md`, dan `results/synthetic-dataset-test-2026-11-17.md`. Near-duplicate threshold 0.88 hanya parameter fixture, bukan threshold produksi. Hash-bucket split hanya membagi grup secara deterministik dan tidak menjamin stratifikasi kelas atau rasio persis. Kelulusan ini tidak mengesahkan sumber data, consent, label, pilot, atau training.

## Bukan prioritas implementasi saat ini

- Implementasi DOCX Metadata Cleaner dalam MVP.
- Implementasi referral atau fitur pembanding teks mandiri.
- Membangun UI/frontend/backend di Stitch atau Antigravity sebagai implementasi sebelum tahap 7.
- Implementasi frontend/backend di Antigravity sebelum acceptance criteria tersedia.
- Memilih provider AI/model final, merchant contract, rewarded-ad activation, storage region, email provider, atau hosting region sebelum benchmark/legal/merchant verification.
- Mengumpulkan pilot dataset nyata sebelum prosedur dan sumber data siap.
- Training model sebelum gerbang dataset dipenuhi.

## Langkah berikutnya

Tahap 1–5 telah selesai dan SRS disahkan untuk System Design. Baseline tahap 6 tersedia:
- [User Flows](USER-FLOWS.md)
- [System Design](SYSTEM-DESIGN.md)
- [Data Flow and Data Lifecycle](DATA-FLOW-AND-DATA-LIFECYCLE.md)
- [API Contracts](API-CONTRACTS.md)
- [Technology Evaluation](TECHNOLOGY-EVALUATION.md)
- [Security Architecture and Threat Model](SECURITY-ARCHITECTURE-AND-THREAT-MODEL.md)
- [UI/UX Specification](UI-UX-SPECIFICATION.md)
- [Google Stitch Design Prompts](STITCH-DESIGN-PROMPTS.md)

Acceptance Criteria baseline memetakan 275 requirement aktif dan 55 skenario Gherkin. Test execution produk belum dimulai. Synthetic Dataset Test tetap Verified 29/29 dan tidak mengesahkan pilot/training.

Task tahap 6: [System Design and UI/UX Handoff](tasks/2026-11-17-system-design-and-ui-ux.md). Task audit requirement: [SRS Readiness Audit](tasks/2026-11-17-srs-readiness-audit.md) — Complete.

Sisa handoff eksternal: jalankan UI UX Pro Max/Google Stitch di Antigravity lokal, konfirmasi merchant/provider/policy, legal/privacy review, dan tetapkan target operasional setelah benchmark. Pekerjaan tersebut tidak mengubah batas mandat: **tahap 7, pembangunan website, belum dimulai dan tidak dikerjakan dalam sesi ini.**

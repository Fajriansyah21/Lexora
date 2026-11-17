# Lexora Active Roadmap

Terakhir diperbarui: 2026-11-17

## Cakupan produk MVP

Keputusan **DEC-001** menetapkan dua modul untuk MVP pertama:
1. AI Text Detector.
2. AI Humanizer.

DOCX Metadata Cleaner ditunda ke fase setelah MVP. Arsitektur produk tetap modular, tetapi infrastruktur untuk modul yang ditunda tidak perlu dibangun sekarang. Sistem referral dan fitur perbandingan dua teks mandiri juga tidak masuk MVP berdasarkan DEC-010.

## Status analisis kebutuhan sistem

SRS berstatus **Approved for System Design** melalui delegated project lead review pada 2026-11-17. Lihat [SRS Review Record](../docs/SRS-REVIEW-AND-APPROVAL-2026-11-17.md) dan [Requirements Elicitation Status](REQUIREMENTS-ELICITATION-STATUS.md).

Posisi dokumentasi pada 2026-11-17:
- 189 catatan keputusan: 187 Accepted dan 2 Superseded (DEC-018 dan DEC-019).
- 276 baris kebutuhan fungsional/nonfungsional terstruktur dalam SRS, termasuk 124 requirement Humanizer, 17 requirement Detector, dan modul pendukung.
- Audit konsistensi requirement Humanizer telah diselesaikan pada 2026-11-17; gap desain teknis dan acceptance criteria tetap menjadi pekerjaan tahap berikutnya.
- Audit requirement awal Detector selesai; metodologi model, threshold, dan acceptance criteria masih perlu divalidasi.
- Audit requirement inti akun, dashboard, kredit, pembayaran, dukungan, notifikasi, Admin, dan operasional telah diperluas; nilai komersial, provider, permission matrix rinci, dan target operasional tetap terbuka.

SRS siap menjadi dasar System Design. Detail provider, harga, retensi legal, token limits, dan target operasional tetap harus ditentukan/diuji pada tahap desain sebelum implementasi atau produksi. Ringkasan status bukan pengganti SRS atau Decision Log.

## Tahap perencanaan sistem MVP

| Urutan | Pekerjaan | Status | Kriteria keluaran |
|---:|---|---|---|
| 1 | Elisitasi kebutuhan, audit konsistensi, dan acceptance criteria | In progress; Humanizer mendalam, Detector dan modul pendukung belum lengkap | Seluruh area kebutuhan ditinjau, konflik/ketidakjelasan ditutup, setiap requirement memiliki acceptance criteria |
| 2 | User flow Detector dan Humanizer | Planned | Alur normal, validasi, persetujuan handoff, pembatalan, dan kegagalan |
| 3 | Modular architecture | Planned | Batas modul, tanggung jawab, dependensi, dan kontrak komunikasi |
| 4 | System flowchart | Planned | Diagram jalur sukses, gagal, retry, refund, dan antrean |
| 5 | Data flow dan data lifecycle | Planned | Klasifikasi data, alur penyimpanan, consent, retensi, penghapusan |
| 6 | Evaluasi opsi teknologi | Planned | Perbandingan trade-off framework, backend, database, AI, payment, storage, queue, dan deployment |
| 7 | Spesifikasi MVP dan acceptance criteria | Planned | Spesifikasi yang dapat diuji dan menjadi dasar implementasi |

Jangan mulai implementasi aplikasi hanya karena SRS telah dibuat. Kebutuhan perlu ditinjau dan diterjemahkan menjadi alur, desain, serta kriteria penerimaan yang dapat diverifikasi.

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
- Membuat UI website di Stitch sebelum user flow dan spesifikasi cukup jelas.
- Implementasi frontend/backend di Antigravity sebelum acceptance criteria tersedia.
- Memilih framework, database, provider AI, payment gateway, produk iklan, atau deployment tanpa analisis kebutuhan dan validasi sumber.
- Mengumpulkan pilot dataset nyata sebelum prosedur dan sumber data siap.
- Training model sebelum gerbang dataset dipenuhi.

## Langkah berikutnya

Tahap 1–5 selesai. Tahap 6 aktif: user flow, modular architecture, system flow/data lifecycle, evaluasi teknologi, dan UI/UX. Tahap 7 (pembangunan website) belum dimulai dan berada di luar mandat.

Acceptance criteria baseline tersedia di `plan/ACCEPTANCE-CRITERIA.md` dengan 264 requirement aktif dan 45 skenario rinci di `plan/ACCEPTANCE-TEST-SCENARIOS.md`. Test execution belum dimulai; target performa/availability menunggu desain teknis.

Task aktif: [SRS Readiness Audit](tasks/2026-11-17-srs-readiness-audit.md). Gerbang dataset sintetis telah lulus; tahap website menunggu penutupan dan review kebutuhan produk.

1. Lanjutkan ke elisitasi AI Text Detector; gap Humanizer yang tersisa dipindahkan ke System Design dan acceptance criteria sesuai audit.
2. Verifikasi laporan audit AI Text Detector dan lanjutkan ke modul pendukung.
3. Verifikasi audit modul pendukung; lanjutkan audit lintas modul, keamanan, privasi, dan data lifecycle.
4. Audit konflik/dependensi dan susun acceptance criteria sebelum review akhir SRS.
5. Setelah gerbang kebutuhan terpenuhi dan pemilik proyek meninjau SRS, susun user flow Detector dan Humanizer.
6. Pertahankan jalur uji prosedur sintetis dataset sesuai urutan dan gerbang yang sudah ditetapkan.

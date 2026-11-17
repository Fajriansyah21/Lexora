# Lexora Active Roadmap

Terakhir diperbarui: 2026-11-17

## Cakupan produk MVP

Keputusan **DEC-001** menetapkan dua modul untuk MVP pertama:
1. AI Text Detector.
2. AI Humanizer.

DOCX Metadata Cleaner ditunda ke fase setelah MVP. Arsitektur produk tetap modular, tetapi infrastruktur untuk modul yang ditunda tidak perlu dibangun sekarang. Sistem referral dan fitur perbandingan dua teks mandiri juga tidak masuk MVP berdasarkan DEC-010.

## Status analisis kebutuhan sistem

SRS tetap berstatus **Draft** dan elisitasi kebutuhan masih berlangsung. Rekap terperinci berada di [Requirements Elicitation Status](REQUIREMENTS-ELICITATION-STATUS.md).

Posisi dokumentasi pada 2026-11-17:
- 144 catatan keputusan: 142 Accepted dan 2 Superseded (DEC-018 dan DEC-019).
- 195 baris kebutuhan fungsional dalam SRS, termasuk 124 requirement Humanizer dan 11 requirement Detector.
- Humanizer telah dibahas mendalam, tetapi masih memiliki isu terbuka dan belum memiliki acceptance criteria lengkap.
- Detector baru memiliki fondasi kebutuhan; elisitasi belum menyeluruh.
- Akun, dashboard, kredit, pembayaran, dukungan, Admin, dan operasional sudah memiliki fondasi, tetapi detail kebutuhan belum lengkap.

SRS belum siap menjadi dasar System Design. Elisitasi seluruh modul, audit konflik/dependensi, dan acceptance criteria harus diselesaikan terlebih dahulu. Ringkasan status bukan pengganti SRS atau Decision Log.

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

Task aktif: [SRS Readiness Audit](tasks/2026-11-17-srs-readiness-audit.md). Gerbang dataset sintetis telah lulus; tahap website menunggu penutupan dan review kebutuhan produk.

1. Lanjutkan elisitasi pada gap Humanizer yang benar-benar belum dibahas; lihat Requirements Elicitation Status.
2. Lengkapi elisitasi AI Text Detector.
3. Lengkapi akun, dashboard, kredit, transaksi, pembayaran, Admin, dukungan, dan operasional.
4. Audit konflik/dependensi dan susun acceptance criteria sebelum review akhir SRS.
5. Setelah gerbang kebutuhan terpenuhi dan pemilik proyek meninjau SRS, susun user flow Detector dan Humanizer.
6. Pertahankan jalur uji prosedur sintetis dataset sesuai urutan dan gerbang yang sudah ditetapkan.

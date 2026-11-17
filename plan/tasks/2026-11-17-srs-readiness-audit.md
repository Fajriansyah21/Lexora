# Task Plan: SRS Readiness Audit Before Website Development

- **Tanggal:** 2026-11-17
- **Status:** Complete (2026-11-17)
- **Delegasi:** Pada 2026-11-17, pemilik proyek memberikan kewenangan kepada project lead untuk menyelesaikan urutan 1–6 secara mandiri tanpa persetujuan per langkah. Tahap 7 (pembangunan website) secara eksplisit di luar cakupan.
- **Tujuan:** memastikan requirement produk Lexora cukup lengkap, konsisten, dan dapat diuji sebelum user flow, System Design, UI/UX final, atau implementasi website.
- **Gerbang sebelumnya:** Synthetic Dataset Procedure Tests lulus 29/29 pada GitHub Actions run #4.

## Temuan audit awal

- SRS berstatus Approved for System Design dan berisi 276 requirement unik tanpa ID duplikat (255 FR + 21 NFR).
- Distribusi FR: GEN 9, FILE 9, DET 17, HUM 124, ACC 21, CRED 25, PAY 9, SUP 8, NOT 8, OPS 12, ADM 13; ditambah 21 NFR.
- Decision Log memuat DEC-001 sampai DEC-189: 187 Accepted dan 2 Superseded.
- Audit Humanizer selesai; gap provider/model, token/chunking, benchmark kualitas, dan retensi teknis dipindahkan ke System Design/pre-production.
- Audit Detector selesai dengan 17 requirement; metode model, threshold, dan target kualitas tetap memerlukan benchmark.
- Audit modul pendukung selesai: akun 21 FR, kredit 25 FR, payment 9 FR, support 8 FR, notifications 8 FR, Admin 13 FR, operations 12 FR.
- Acceptance Criteria memetakan 275 requirement aktif dan 55 skenario Gherkin rinci tersedia. SRS telah disahkan untuk System Design. Implementasi website belum dimulai dan di luar mandat.

## Ruang lingkup

1. Audit seluruh requirement terhadap keputusan terbaru.
2. Identifikasi requirement ambigu, konflik, duplikasi, dependency, dan kondisi tepi.
3. Bedakan hal yang dapat diturunkan langsung dari keputusan dengan hal yang membutuhkan keputusan pemilik proyek.
4. Susun acceptance criteria terukur tanpa mengubah requirement secara diam-diam.
5. Perbarui status elisitasi dan roadmap berdasarkan bukti.

## Di luar ruang lingkup

- Memilih framework, database, provider AI, payment gateway, atau deployment sebelum evaluasi.
- Membuat wireframe final atau mengimplementasikan frontend/backend.
- Menetapkan harga, kredit, batas penggunaan, kebijakan retensi, atau perilaku produk yang belum disetujui.
- Menganggap Synthetic Dataset Test lulus sebagai izin pilot data nyata atau training model.

## Urutan kerja

1. Audit konsistensi Humanizer dan tutup gap yang dapat diselesaikan melalui keputusan delegasi; sisanya diklasifikasikan sebagai pekerjaan desain, kalibrasi, atau verifikasi.
2. Elisitasi Detector secara menyeluruh.
3. Lengkapi akun, dashboard, kredit, pembayaran, Admin, dukungan, dan operasional.
4. Audit konflik lintas modul, dependensi, keamanan, privasi, dan data lifecycle.
5. Susun acceptance criteria untuk seluruh requirement yang disepakati.
6. Konsolidasikan SRS dan Feature Plans, lalu minta review pemilik proyek.
7. Setelah disetujui, susun user flow, arsitektur modular, data flow, evaluasi teknologi, dan rencana UI/UX.
8. Mulai implementasi website setelah gerbang System Design dan acceptance criteria dipenuhi.

## Progress per 2026-11-17

- [x] Tahap 1: audit struktur dan konsistensi Humanizer FR-HUM-01 sampai FR-HUM-124.
- [x] Perbaiki konflik/ketertinggalan FR-HUM-06, FR-HUM-14, FR-HUM-38, FR-HUM-71, FR-HUM-75, FR-HUM-117, serta pemetaan FR-HUM-118 sampai FR-HUM-124.
- [x] Catat DEC-145 sampai DEC-149 di bawah delegasi project lead.
- [x] Publikasikan laporan audit Humanizer.
- [x] Tahap 2: audit kebutuhan produk AI Text Detector dan catat DEC-150 sampai DEC-155.
- [x] Laporan audit Detector: `docs/AI-TEXT-DETECTOR-REQUIREMENTS-AUDIT-2026-11-17.md`.
- [x] Tahap 3: perluas requirement modul pendukung (akun, dashboard, kredit, transaksi, pembayaran, dukungan, notifikasi, Admin, operasional) dan NFR.

## Kriteria selesai

- [x] Seluruh 255 requirement fungsional dan 21 requirement nonfungsional telah diperiksa terhadap Decision Log terbaru.
- [x] Konflik, duplikasi, dependensi, dan kondisi tepi dicatat serta diselesaikan atau ditandai blocked.
- [x] Keputusan yang berada dalam ruang lingkup delegasi dicatat di Decision Log; keputusan yang memerlukan bukti eksternal/validasi hukum tetap ditandai sebagai asumsi atau prasyarat, bukan diklaim tervalidasi.
- [x] Acceptance criteria baseline tersedia untuk 275 requirement aktif; 55 skenario Gherkin rinci disiapkan.
- [x] SRS dan Feature Plans konsisten dan direview melalui delegated project lead approval untuk System Design.
- [x] User flow dan System Design memiliki dasar requirement yang disahkan.

## Aturan pelaporan

Jangan menyebut SRS siap implementasi hanya karena semua ID requirement sudah ada. Laporkan coverage, unresolved decisions, testability, serta risiko yang masih terbuka secara terpisah.


## Closeout

Tahap 1–5 selesai. Lanjutkan hanya dengan [System Design and UI/UX Handoff](2026-11-17-system-design-and-ui-ux.md) untuk tahap 6. Tahap 7 (pembangunan website) tidak termasuk mandat ini.

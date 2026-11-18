# Design Freeze Review — Lexora

- **Tanggal:** 2026-11-18
- **Status keputusan:** **Conditional Design Freeze v1.0**
- **Cakupan:** 8 screen exports, 1 design system, UI/UX specification, dan pemeriksaan kesesuaian terhadap SRS, Decision Log, serta Acceptance Criteria.
- **Implementasi website:** belum dimulai; tahap 7 tetap di luar mandat.

## 1. Keputusan

Delapan halaman visual Lexora ditetapkan sebagai **baseline resmi untuk handoff frontend** dengan status *conditional freeze*. Struktur, arah visual, navigasi, dan pola komponen dapat dijadikan acuan implementasi.

Status ini bukan persetujuan produksi. Dua gerbang masih terbuka:
1. Browser-based visual QA pada desktop, tablet, dan mobile.
2. Verifikasi aksesibilitas WCAG 2.2 AA secara menyeluruh, termasuk keyboard, focus, screen reader, dan seluruh pasangan warna.

Ekspor HTML dari Stitch adalah artefak desain/prototipe. Jangan menggunakan JavaScript demo, angka contoh, atau state simulasi sebagai logika produksi. Frontend produksi tetap harus dibangun sesuai System Design dan kontrak API.

## 2. Artefak desain yang dibekukan

| Halaman | Artefak |
|---|---|
| Landing Page | `Desain/lexora_landing_page/code.html` |
| User Dashboard | `Desain/lexora_user_dashboard/code.html` |
| AI Text Detector | `Desain/lexora_ai_text_detector_hasil_analisis/code.html` |
| AI Humanizer Editor | `Desain/lexora_ai_humanizer_editor/code.html` |
| Style Profiles | `Desain/lexora_style_profiles/code.html` |
| Credits & Transactions | `Desain/lexora_credits_transaksi/code.html` |
| Support & Privacy Center | `Desain/lexora_support_privacy_center/code.html` |
| Admin Panel | `Desain/lexora_admin_panel/code.html` |
| Design System | `Desain/calm_editorial_intelligence/DESIGN.md` |

Arah visual tetap **Calm Editorial Intelligence**. Tidak ada redesign menyeluruh; perubahan bersifat korektif agar desain konsisten dengan keputusan proyek.

## 3. Koreksi yang diterapkan

### P0 — Klaim keamanan dan kepatuhan yang tidak terbukti

- Menghapus klaim ISO 27001, Zero-Knowledge, enkripsi end-to-end, AES-256/TLS 1.3 sebagai implementasi yang sudah tersedia, SHA-256 tervalidasi, serta klaim audit kriptografis permanen.
- Mengganti copy Admin menjadi prinsip akses teks tanpa akses default, dengan tiket relevan, persetujuan eksplisit, permission yang sesuai, batas maksimum 60 menit, dan pencatatan audit.
- Menghapus janji kerahasiaan 100% dan penghapusan tanpa jejak.
- Menjelaskan bahwa detail algoritma enkripsi, pengelolaan kunci, retensi backup, dan retensi provider harus diverifikasi sebelum produksi.

### P1 — Ketidaksesuaian terhadap keputusan produk

- Support menampilkan target respons awal maksimal **2 hari kerja**, bukan janji 15–30 menit. Target bukan jaminan penyelesaian.
- Tiket Resolved tidak diklaim otomatis berubah menjadi Closed; setelah jendela 7 hari, pengguna membuat tiket baru.
- Kredit pembelian dinyatakan tidak kedaluwarsa. Contoh bonus harian menggunakan 20 kredit dan masa berlaku 7 hari.
- Nilai reward iklan tidak ditetapkan secara hardcoded. Rewarded Ads dinonaktifkan pada prototipe sampai provider, kebijakan, dan server-side verification lolos pemeriksaan.
- Menghapus simulasi frontend yang sebelumnya dapat menampilkan pembayaran berhasil dan seolah-olah menambahkan kredit tanpa backend.
- Menghapus klaim harga final, e-Faktur/PPN tertentu, WhatsApp support, dan fitur multi-akun sebagai kemampuan yang sudah disetujui.
- Menghapus paket langganan Pro Editorial sebagai status akun. Nama paket kredit yang tersisa diberi konteks contoh dan belum final.
- Memisahkan persetujuan penggunaan teks untuk training/penelitian sebagai opt-in spesifik, opsional, dan nonaktif secara default.
- Mengubah copy privasi agar tidak menjanjikan pemrosesan RAM-only atau penghapusan menyeluruh yang belum diverifikasi.

### P2 — Konsistensi batas dan istilah

- Batas Detector ditampilkan sebagai 20.000 extended grapheme clusters; batas Humanizer 50.000 per pekerjaan dan minimum 100.
- Menghapus nama model Detector yang belum dipilih serta label metodologi non-probabilistik yang belum ditetapkan.
- Menghapus progress bar diagnostik di landing yang dapat disalahartikan sebagai persentase kemungkinan AI.
- Mengubah batas Style Profiles menjadi maksimal 6 profil per akun, bukan 6 profil aktif.
- Memperbarui tanggal contoh yang sudah kedaluwarsa dan memperjelas bahwa data dalam ekspor HTML bersifat ilustratif.
- Menambahkan judul dokumen HTML, penanda data contoh, dan menu navigasi seluler.

## 4. Pemeriksaan responsivitas pada level sumber

Pemeriksaan statis pada delapan HTML menemukan:
- Semua halaman memiliki `lang="id"`, meta viewport, dan elemen `title`.
- Enam halaman aplikasi pengguna menyembunyikan sidebar desktop di bawah breakpoint `lg`, memakai navigasi bawah seluler, dan memberi ruang bawah agar konten tidak tertutup navigasi.
- Landing Page memiliki menu seluler.
- Admin Panel memiliki menu dropdown seluler dan sidebar desktop hanya pada breakpoint `lg` ke atas.
- Tabel pada halaman Dashboard, Style Profiles, Credits, Support, dan Admin berada di dalam wrapper horizontal-scroll.
- Pemeriksaan keseimbangan tag dasar tidak menemukan selisih buka/tutup untuk tag struktural yang diperiksa.

**Batas pemeriksaan:** ini adalah audit sumber HTML/CSS, bukan hasil render browser. Tidak ada screenshot desktop/mobile yang dihasilkan ulang pada sesi ini. Berkas `screen.png` yang sudah ada di folder Admin dan Support belum diperbarui mengikuti revisi HTML.

## 5. Pemeriksaan kontras warna

Perhitungan relative luminance untuk pasangan warna utama:

| Pasangan | Rasio | Hasil |
|---|---:|---|
| `#17231F` pada `#FFFFFF` | 16,20:1 | Lulus AA normal |
| `#5D6964` pada `#EEF2F0` | 5,07:1 | Lulus AA normal |
| `#0F766E` pada `#FFFFFF` | 5,47:1 | Lulus AA normal |
| `#A3FAEF` pada `#0F766E` | 4,56:1 | Lulus AA normal |

Token teks sekunder diperbarui dari `#66736E` menjadi `#5D6964`. Nilai sebelumnya hanya sekitar 4,38:1 pada surface `#EEF2F0`, di bawah ambang 4,5:1 untuk teks normal.

Perhitungan ini tidak menggantikan audit kontras seluruh komponen, hover, disabled, focus, dan status.

## 6. Cross-check terhadap sumber normatif

| Area | Rujukan utama | Hasil review desain |
|---|---|---|
| Detector | FR-DET-01 s.d. FR-DET-17; DEC-150 s.d. DEC-155; AC-019 s.d. AC-035 | Empat label dipertahankan; MIXED/UNCERTAIN berbeda; tanpa persentase; batas 20.000; disclaimer bukan bukti kepengarangan |
| Humanizer | FR-HUM; DEC-146 s.d. DEC-149; AC-068 s.d. AC-149 | Batas 50.000 dan minimum 100; gaya bawaan; kontrol makna; peringatan pemeriksaan fakta |
| Style Profiles | FR-HUM-Profile; DEC-149; AC-HUM-01/02 | Maksimum 6 profil per akun; 20 sampel per profil; minimal 3 sampel eligible, masing-masing minimal 500 cluster |
| Credits & Ads | FR-CRED; DEC-156 s.d. DEC-159; DEC-167; DEC-175/176; AC-180 s.d. AC-204 | Kredit pembelian tidak kedaluwarsa; bonus harian/reward login 7 hari; Guest tidak menerima rewarded ads; reward menunggu verifikasi |
| Payments | FR-PAY; DEC-160; AC-PAY | Tidak ada simulasi pembayaran sukses di frontend; verifikasi dan pemberian kredit tetap server-side |
| Support | FR-SUP-05 s.d. FR-SUP-08; DEC-161; AC-218 s.d. AC-221 | Status tiket dan jendela reopen 7 hari konsisten; target respons awal 2 hari kerja |
| Privacy | NFR-PRIV-01 s.d. NFR-PRIV-09; DEC-168 s.d. DEC-174 | Tidak ada klaim penghapusan total/retensi RAM-only; opt-in training terpisah; hak data dan keberatan ditampilkan |
| Admin | FR-ADM-01 s.d. FR-ADM-13; DEC-163; AC-242 s.d. AC-254 | Tiga role RBAC; akses teks bukan default; tiket, consent, permission, batas 60 menit, dan audit |
| Accessibility | NFR-ACC-01; AC-265 | Target WCAG 2.2 AA tetap menjadi gerbang; belum dinyatakan lulus |

Acceptance Criteria berjumlah **275 aktif** dan skenario Gherkin berjumlah **55**. Status seluruh pengujian penerimaan tetap **Not executed** karena website belum diimplementasikan. Cross-check desain tidak mengubah status tersebut.

## 7. Gerbang sebelum full design sign-off

1. Buka semua delapan HTML dalam browser pada viewport 390×844, 768×1024, 1024×768, dan 1440×900.
2. Periksa horizontal overflow, sticky header, bottom navigation, modal/dropdown, editor, tabel, dan panjang teks Bahasa Indonesia.
3. Uji keyboard-only, focus visibility, semantic labels, screen reader, dan seluruh pasangan kontras sesuai WCAG 2.2 AA.
4. Regenerasi `screen.png` untuk Admin dan Support setelah tampilan akhir diverifikasi.
5. Pastikan penghitung karakter pada implementasi produksi menggunakan aturan extended grapheme cluster Unicode 18.0.0 yang sama dengan backend. JavaScript counter di ekspor HTML masih bersifat placeholder dan tidak boleh digunakan sebagai validasi produksi.
6. Pastikan nilai harga, paket, reward, dan provider tetap berasal dari konfigurasi server serta tidak diperlakukan sebagai keputusan komersial final.

## 8. Batas cakupan

- Baseline desain ini mengesahkan acuan visual untuk frontend, bukan implementasi aplikasi.
- Tidak ada frontend/backend, integrasi provider, autentikasi, pembayaran, atau pemrosesan AI yang dibangun dalam review ini.
- Tahap 7 tetap **out of scope** sampai ada mandat baru.

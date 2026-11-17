# Requirements Elicitation Status

- **Produk:** Lexora
- **Tanggal rekap:** 2026-11-17
- **Status keseluruhan:** Elisitasi kebutuhan masih berlangsung
- **Cakupan MVP:** AI Text Detector dan AI Humanizer
- **Sumber utama:** [Decision Log](DECISION-LOG.md) dan [System Requirements Analysis](SYSTEM-REQUIREMENTS-ANALYSIS.md)

## 1. Ringkasan kuantitatif dokumentasi

Berdasarkan pemeriksaan dokumen GitHub pada 2026-11-17:

- **149** catatan keputusan, DEC-001 sampai DEC-149.
- **147** keputusan berstatus `Accepted`.
- **2** keputusan berstatus `Superseded`, yaitu DEC-018 dan DEC-019. Keduanya dipertahankan sebagai jejak historis, bukan aturan aktif.
- **265** baris kebutuhan fungsional dan nonfungsional terstruktur pada SRS.
- **124** requirement Humanizer, FR-HUM-01 sampai FR-HUM-124.
- **17** requirement Detector, FR-DET-01 sampai FR-DET-17.

Rincian jumlah requirement lain dalam SRS:

| Kelompok | Jumlah |
|---|---:|
| Umum (FR-GEN) | 9 |
| File dan ekstraksi (FR-FILE) | 9 |
| AI Text Detector (FR-DET) | 11 |
| AI Humanizer (FR-HUM) | 124 |
| Akun (FR-ACC) | 15 |
| Kredit (FR-CRED) | 16 |
| Dukungan (FR-SUP) | 3 |
| Notifikasi (FR-NOT) | 3 |
| Operasional (FR-OPS) | 5 |
| **Total** | **195** |

Jumlah baris requirement bukan ukuran kelengkapan produk. Requirement masih perlu ditinjau, diuji konsistensinya, dan diberi acceptance criteria.

## 2. Materi yang sudah dibahas

### 2.1 Fondasi produk dan cakupan MVP

**Keputusan terkait:** DEC-001 sampai DEC-014, dengan DEC-003 juga menjadi dasar kebutuhan Detector.

Pokok pembahasan:
- MVP terdiri dari AI Text Detector dan AI Humanizer.
- DOCX Metadata Cleaner ditunda ke fase setelah MVP.
- Target utama mahasiswa dan pelajar, dengan penggunaan akademik maupun umum.
- Detector dan Humanizer memiliki prioritas setara dan dapat digunakan mandiri.
- Hasil Detector hanya dikirim ke Humanizer setelah tindakan pengguna.
- Bahasa utama Bahasa Indonesia dan Bahasa Inggris; teks campuran diterima dengan peringatan keterbatasan.
- Hak akses Guest dan pengguna terdaftar.
- Draft Guest dipertahankan ketika autentikasi dibatalkan dan dibawa setelah autentikasi berhasil.
- Fondasi akun, dashboard, kredit, reward, pembayaran, Admin Panel, dukungan, notifikasi, dan fitur di luar MVP.

### 2.2 AI Text Detector

**Keputusan terkait:** DEC-003 dan DEC-015 sampai DEC-019.

Pokok pembahasan:
- Ringkasan analisis keseluruhan, analisis per kalimat, dan penjelasan.
- Kategori produk HUMAN, AI, MIXED, dan UNCERTAIN.
- Hasil merupakan estimasi, bukan bukti pasti kepengarangan.
- Input teks langsung dan unggahan TXT, DOCX, atau PDF.
- Batas maksimum input 20.000 extended grapheme clusters berlaku sama bagi Guest dan pengguna terdaftar (DEC-150).
- Tidak ada batas minimum karakter input Detector yang disepakati.

**Klarifikasi penting:** DEC-018 dan DEC-019 berstatus Superseded. DEC-020 mengklarifikasi bahwa batas minimum karakter berlaku untuk setiap sampel profil gaya Humanizer, bukan untuk input Detector.

**Status:** Audit requirement Detector tahap 2 selesai pada 2026-11-17. Laporan audit: [AI Text Detector Requirements Audit](../docs/AI-TEXT-DETECTOR-REQUIREMENTS-AUDIT-2026-11-17.md). Hasilnya mencakup batas input 20.000 extended grapheme clusters, tidak ada hard minimum, perilaku UNCERTAIN, definisi MIXED, tidak ada skor numerik pada MVP, penjelasan yang dapat ditelusuri, dan ekspor laporan. Metode model, threshold, agregasi, target false-positive, serta acceptance criteria masih memerlukan benchmark dan desain.

### 2.3 Profil gaya personal Humanizer

Keputusan terbaru untuk gaya bawaan, minimum tiga sampel, dan konvensi hitung karakter tercatat pada DEC-146, DEC-148, dan DEC-149. Audit konsistensi Humanizer selesai pada 2026-11-17; rincian koreksi dan gap desain berada di [Humanizer Requirements Audit](../docs/HUMANIZER-REQUIREMENTS-AUDIT-2026-11-17.md).

**Keputusan terkait:** DEC-020 sampai DEC-051.

Pokok pembahasan:
- Sampel dapat ditempel atau diunggah dan dikelola sebagai entri terpisah.
- Kecukupan dinilai terhadap kumpulan sampel secara adaptif.
- Perubahan sampel memicu evaluasi ulang.
- Profil yang tidak memadai tetap terlihat tetapi tidak dapat dipilih.
- Kegagalan teknis evaluasi dibedakan dari hasil penilaian sampel.
- Versi aktif sebelumnya dipertahankan selama evaluasi/pembangunan versi baru.
- Versioning, masa retensi historis, pemulihan versi, batas versi historis, prioritas antrean, dan penanganan konkurensi.
- Snapshot evaluasi yang konsisten dan batas pengulangan evaluasi otomatis.
- Metadata audit evaluasi dan kontrol akses investigasi Admin.
- Masa persetujuan, pencabutan, notifikasi, serta retry notifikasi akses investigasi.

### 2.4 Input, pemrosesan, hasil, dan riwayat Humanizer

**Keputusan terkait:** DEC-052 sampai DEC-070.

Pokok pembahasan:
- Penggabungan teks hasil ekstraksi dan teks manual dalam satu editor.
- Maksimal satu dokumen unggahan per proses.
- Konfirmasi sebelum mengganti dokumen.
- Pengeditan bebas sebelum pemrosesan.
- Format keluaran mengikuti sumber dokumen atau dipilih pengguna untuk input manual.
- Hasil tidak disimpan otomatis.
- Riwayat menyimpan teks asli dan hasil revisi jika pengguna memilih menyimpan.
- Penghapusan entri riwayat.
- Kapasitas riwayat berdasarkan ukuran data, bukan jumlah entri.
- Ambang peringatan 90%, indikator kapasitas, banner, dan perilaku ketika kapasitas penuh.
- Hasil tetap dapat disalin/diunduh dan dapat disimpan kembali tanpa pemrosesan ulang setelah kapasitas tersedia.

### 2.5 Hasil belum tersimpan dan aksesibilitas

**Keputusan terkait:** DEC-071 sampai DEC-086.

Pokok pembahasan:
- Hasil yang belum disimpan hilang setelah halaman/sesi ditutup.
- Konfirmasi sebelum navigasi yang meninggalkan hasil.
- Perilaku tombol Tetap di halaman, Lanjutkan, X, Escape, dan backdrop.
- Pemeliharaan kondisi halaman saat navigasi dibatalkan.
- Focus trap, fokus awal, pengembalian fokus, dan dukungan screen reader.
- Modal menggunakan semantik alert dialog dan pengumuman yang terkoordinasi.

### 2.6 Batasan Humanizer, sampel, dan file

**Keputusan terkait:** DEC-087 sampai DEC-105.

Pokok pembahasan:
- Input Humanizer maksimum 50.000 karakter dan minimum 100 karakter per pekerjaan.
- Setiap sampel profil gaya minimum 500 karakter.
- Maksimal 6 profil gaya per akun.
- Profil privat dan dikelola pemilik akun.
- Penghapusan profil dan pergantian profil utama.
- Maksimal 20 sampel per profil.
- Ukuran maksimal file sampel 10 MB dan maksimal 5 file per batch.
- TXT, DOCX, PDF; ekstraksi independen per file.
- Pratinjau dan konfirmasi teks hasil ekstraksi.
- Nama sampel, aturan duplikasi, karakter Unicode, dan batas panjang nama.
- Pengunduhan sampel individual dan ZIP.

### 2.7 Recently Deleted, aktivitas akun, dan penghapusan akun

**Keputusan terkait:** DEC-106 sampai DEC-119.

Pokok pembahasan:
- Sampel terhapus dapat dipulihkan selama 30 hari.
- Konflik nama saat pemulihan.
- Restore All bersifat atomik.
- Penghapusan permanen sampel dan audit log.
- Riwayat aktivitas penghapusan untuk pengguna dengan retensi 90 hari.
- Penghapusan riwayat aktivitas dan sinkronisasi lintas perangkat.
- Perilaku riwayat saat akun dihapus.
- Pembatalan permintaan penghapusan akun.
- Masa penundaan penghapusan akun 30 hari.
- Akses terbatas selama status Pending Deletion.

### 2.8 Ekspor data pribadi dan riwayat ekspor

**Keputusan terkait:** DEC-120 sampai DEC-137.

Pokok pembahasan:
- Ekspor data pribadi dalam satu paket ZIP.
- Isi paket dan pengecualian data sensitif.
- Maksimal 3 permintaan ekspor dalam jendela bergulir 24 jam.
- Paket berlaku 24 jam dan dapat diunduh ulang selama tersedia.
- Pembatalan proses ekspor dan satu proses aktif per akun.
- Notifikasi hasil ekspor melalui aplikasi dan email.
- Halaman riwayat ekspor dan retensi 90 hari.
- Penghapusan satu entri atau seluruh riwayat.
- Sinkronisasi lintas perangkat dan audit log internal.
- Notifikasi penghapusan hanya dalam aplikasi.
- Autentikasi ulang untuk penghapusan seluruh riwayat dan masa berlaku 5 menit.
- Tidak ada pembatalan setelah konfirmasi akhir.
- Penghapusan seluruh riwayat bersifat atomik.
- Percobaan ulang memerlukan autentikasi ulang dan konfirmasi baru.
- Rate limiting jeda minimal 30 detik setelah kegagalan, dihitung per akun lintas perangkat.

## 3. Status per area

Audit modul pendukung selesai pada 2026-11-17. Lihat [Supporting Modules Requirements Audit](../docs/SUPPORTING-MODULES-REQUIREMENTS-AUDIT-2026-11-17.md) untuk koreksi dan keputusan akun, kredit, pembayaran, dukungan, notifikasi, Admin, dan operasional.

| Area | Status saat ini | Catatan |
|---|---|---|
| Fondasi produk | Sudah dibahas | Cakupan MVP dan aturan dasar sudah tercatat |
| Humanizer | Elisitasi mendalam, belum ditutup | 124 FR; masih ada isu produk/teknis dan acceptance criteria |
| Detector | Audit requirement awal selesai | 17 FR; definisi label, panjang input, abstention, penjelasan, ekspor, dan batas bahasa telah diperjelas; metodologi model dan acceptance criteria masih terbuka |
| Akun dan dashboard | Requirement inti dilengkapi | 19 FR; account linking, session revocation, email change, dan security notification telah ditetapkan; UI dan detail token masih perlu desain |
| Kredit dan pembayaran | Requirement inti dilengkapi | 24 FR-CRED dan 9 FR-PAY; ledger, reserve/settlement, expiry, webhook, idempotency, dan rekonsiliasi ditetapkan; tarif/provider tetap terbuka |
| Dukungan dan notifikasi | Requirement inti dilengkapi | 8 FR-SUP dan 8 FR-NOT; status tiket, target respons, preferensi, opt-in promosi, dan retry telah ditetapkan |
| Admin dan operasional | Requirement inti dilengkapi | 13 FR-ADM dan 12 FR-OPS; RBAC, akses teks terbatas, job cancellation, retry, dan recovery telah ditetapkan; detail implementasi tetap perlu System Design |
| Audit konsistensi | Belum diselesaikan | Perlu pemeriksaan lintas requirement dan keputusan |
| Acceptance criteria | Baseline tersusun | 264 requirement aktif telah dipetakan ke acceptance statement dan edge/negative test; 45 skenario Gherkin rinci tersedia. Target numerik performa/availability dan test execution masih pending |
| Wireframe/System Design/implementasi | Belum dimulai | Tidak boleh dimulai sebelum gerbang kebutuhan dipenuhi |

## 4. Hal yang masih terbuka

### 4.1 Humanizer

- Provider/model AI dan estimasi biaya.
- Daftar final gaya bawaan.
- Algoritma profiling serta kriteria adaptif untuk menilai kecukupan keseluruhan kumpulan sampel.
- Bentuk representasi profil dan retensi sampel mentah.
- Batas token internal, strategi chunking, penjagaan konteks, dan batas provider.
- Library ekstraksi dokumen, OCR, serta generator TXT/DOCX/PDF.
- Target kualitas, metrik, protokol evaluasi, dan dataset benchmark Humanizer.
- Nilai kuota penyimpanan riwayat, satuan penghitungan, dan detail teknis penghitungan kapasitas.
- Kebijakan teknis retensi cache, file sementara, backup, serta data yang diproses penyedia AI.
- Acceptance criteria terukur.

Rincian berada di bagian 8 [AI Humanizer Plan](AI-HUMANIZER-PLAN.md) dan bagian 8 SRS.

### 4.2 AI Text Detector

- Angka batas maksimum input dan batas token internal.
- Definisi operasional label serta panduan anotasi.
- Confidence, threshold, dan kalibrasi.
- Penjelasan hasil yang dapat ditelusuri.
- Perilaku untuk teks pendek, campuran bahasa, domain berbeda, dan hasil tidak pasti.
- Strategi chunking dan konteks.
- Format laporan final.
- Target kualitas, monitoring drift, dan evaluasi ulang.
- Model dan skema inference final.

Rincian berada di [AI Text Detector Plan](AI-TEXT-DETECTOR-PLAN.md) dan bagian 8 SRS.

### 4.3 Akun, kredit, pembayaran, Admin, dan operasional

- Detail halaman dan pengaturan dashboard.
- Batas reward iklan Guest/login dan nilai kredit per iklan, menunggu unit economics dan validasi provider.
- Formula biaya per fitur, tarif, pembulatan, dan unit economics.
- Paket/harga komersial awal dan payment gateway.
- Produk iklan yang sesuai kebijakan resmi.
- Detail teknis guest checkout dan pemulihan transaksi.
- Permission matrix per aksi/objek, implementasi 2FA, dan approval akses sensitif.
- Retensi tiket dan notifikasi.
- Detail teknis observability, SLA uptime, backup/restore, dan disaster recovery.

Daftar lengkap dan statusnya mengacu pada bagian 8 SRS.

## 5. Pertanyaan terbuka dari sesi sebelumnya

**Pertanyaan terbuka terkait titik awal rate limiting ekspor telah diselesaikan melalui DEC-145.** Jeda 30 detik dimulai setelah transaksi gagal mencapai status akhir Failed berdasarkan timestamp server. Pembatasan berlaku per akun lintas perangkat.

## 6. Keputusan terbaru dari audit Humanizer

- **DEC-144:** Pengguna dapat membatalkan permintaan penghapusan sebelum tahap eksekusi; data tetap utuh dan pekerjaan yang dibatalkan tidak dilanjutkan otomatis.
- Requirement normatif: **FR-HUM-124**.

- **DEC-143:** Kegagalan penghapusan harus dijelaskan kepada pengguna; percobaan berikutnya diajukan sebagai permintaan baru.
- Requirement normatif: **FR-HUM-123**.

- **DEC-141:** Penghapusan profil tidak membatalkan pekerjaan Humanizer untuk dokumen yang sudah mulai diproses. Pekerjaan tersebut menyelesaikan proses dengan snapshot profil saat mulai; profil yang dihapus tidak dapat dipakai untuk pekerjaan baru.
- Requirement normatif: **FR-HUM-121** dan klarifikasi ruang lingkup **FR-HUM-118**.

- **DEC-140:** Jika profil utama dihapus sementara masih ada profil lain, pengguna wajib memilih profil pengganti sebelum konfirmasi. Profil pengganti menjadi profil utama setelah penghapusan berhasil.
- Requirement normatif: **FR-HUM-120**; dibaca bersama **FR-HUM-73** dan pengecualian profil terakhir pada **FR-HUM-119**.

- **DEC-139:** Profil gaya utama terakhir boleh dihapus tanpa profil pengganti. Setelah penghapusan, Humanizer menggunakan gaya bawaan yang dipilih pengguna untuk pekerjaan berikutnya.
- Requirement normatif: **FR-HUM-119**; pengecualian terhadap aturan profil utama pada **FR-HUM-73**.

- **DEC-138:** Penghapusan profil gaya membatalkan seluruh pekerjaan terkait yang masih tertunda atau berjalan. Hasil pekerjaan yang terlambat tidak boleh mengaktifkan kembali atau membuat ulang profil yang telah dihapus.
- Requirement normatif: **FR-HUM-118** pada SRS bagian 4.4.

## 7. Urutan pekerjaan berikutnya

1. Verifikasi hasil audit Humanizer dan gunakan [Humanizer Requirements Audit](../docs/HUMANIZER-REQUIREMENTS-AUDIT-2026-11-17.md) sebagai catatan koreksi, konflik, dan gap desain.
2. Lanjutkan elisitasi Humanizer pada gap yang benar-benar terbuka.
3. Lakukan elisitasi AI Text Detector secara menyeluruh.
4. Lengkapi akun, dashboard, kredit, transaksi, pembayaran, Admin, dukungan, dan operasional.
5. Audit konflik, dependensi, duplikasi, serta keputusan superseded.
6. Susun acceptance criteria yang dapat diuji untuk setiap requirement.
7. Konsolidasikan SRS dan Feature Plans.
8. Minta review pemilik proyek sebelum user flow, wireframe, Google Stitch, atau System Design.

## 8. Batas tahap

Rekap ini tidak mengesahkan:
- Pemilihan framework, database, provider AI, payment gateway, atau deployment.
- Wireframe atau desain visual.
- System Design final.
- Implementasi aplikasi.
- Klaim bahwa fitur sudah dibangun atau diuji.

Roadmap dan prioritas riset dataset tetap mengikuti [Active Roadmap](ACTIVE-ROADMAP.md) serta instruksi proyek di `AGENTS.md`.

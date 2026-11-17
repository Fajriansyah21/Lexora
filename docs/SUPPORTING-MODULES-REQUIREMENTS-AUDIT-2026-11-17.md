# Supporting Modules Requirements Audit

- **Tanggal:** 2026-11-17
- **Status:** Audit requirement inti modul pendukung selesai; evaluasi provider, harga, kebijakan hukum, dan desain teknis tetap berlanjut.
- **Ruang lingkup:** akun/dashboard, kredit, pembayaran, dukungan, notifikasi, Admin Panel, operasional, dan kebutuhan nonfungsional.
- **Kewenangan:** Keputusan baru dicatat sebagai delegated project decisions sesuai mandat pemilik proyek untuk menyelesaikan tahap 1–6 secara mandiri.

## 1. Cakupan SRS setelah audit

SRS kini memiliki **254 requirement fungsional dan 21 requirement nonfungsional**, total 275 baris requirement unik tanpa ID duplikat.

| Kelompok | Jumlah |
|---|---:|
| FR-GEN | 9 |
| FR-FILE | 9 |
| FR-DET | 17 |
| FR-HUM | 124 |
| FR-ACC | 19 |
| FR-CRED | 24 |
| FR-PAY | 9 |
| FR-SUP | 8 |
| FR-NOT | 8 |
| FR-OPS | 12 |
| FR-ADM | 13 |
| NFR | 13 |
| **Total** | **265** |

Decision Log memuat DEC-001 sampai DEC-174: 172 Accepted dan 2 Superseded.

## 2. Temuan dan perbaikan per modul

### 2.1 Akun dan dashboard
- Menambahkan pengelolaan sesi aktif dan pencabutan sesi.
- Menetapkan bahwa akun email/password dan Google tidak digabung otomatis hanya karena alamat email sama.
- Menambahkan alur perubahan email dengan autentikasi ulang dan verifikasi alamat baru.
- Menambahkan notifikasi keamanan.
- Menegaskan bahwa draft teks Guest dapat dibawa ke alur autentikasi, tetapi saldo reward Guest tidak ikut dipindahkan.

### 2.2 Kredit
- Menetapkan ledger append-only; saldo tidak diedit langsung.
- Menambahkan reservasi kredit sebelum job masuk antrean.
- Menetapkan settlement berdasarkan konsumsi terverifikasi dan pelepasan sisa reservasi.
- Menetapkan bahwa biaya aktual di atas estimasi yang disetujui menjadi risiko operasional Lexora, bukan tagihan tambahan tanpa persetujuan.
- Bonus 20 kredit diberikan sekali per tanggal kalender pukul 03.00 Asia/Jakarta.
- Kredit reward Guest berlaku 24 jam, terikat sesi, dan tidak dapat dipindahkan.
- Reward iklan hanya diberikan setelah server memverifikasi callback/receipt yang sah.
- Nilai reward, paket, dan tarif dikelola sebagai konfigurasi berversi.

### 2.3 Pembayaran
- Menambahkan kelompok requirement FR-PAY-01 sampai FR-PAY-09.
- Status transaksi meliputi Created, Pending, Paid, Failed, Expired, Cancelled, Refund Pending, Partially Refunded, dan Refunded.
- Kredit hanya diberikan setelah verifikasi backend atas status, nominal, mata uang, identitas transaksi, dan signature/callback.
- Callback pembayaran harus idempotent dan tidak boleh menurunkan status Paid.
- Guest harus autentikasi sebelum kredit diberikan; transaksi dapat dipulihkan dan dikaitkan ke akun.
- Rekonsiliasi transaksi menjadi kebutuhan Admin/operasional.

### 2.4 Dukungan
- Menetapkan kategori tiket dan status Open, In Progress, Waiting for User, Resolved, Closed.
- Pengguna dapat membalas tiket sebelum Closed.
- Tiket Resolved dapat dibuka kembali dalam 7 hari kalender.
- Target respons awal maksimal 2 hari kerja, bukan jaminan penyelesaian.
- Lampiran file tidak disediakan pada MVP untuk mengurangi risiko data sensitif masuk tanpa pemeriksaan.

### 2.5 Notifikasi
- Notifikasi keamanan dan transaksi penting tetap tersedia.
- Notifikasi promosi memerlukan opt-in terpisah dan dapat dihentikan.
- Event notifikasi memiliki ID unik dan idempotent.
- Retry maksimal tiga kali untuk kegagalan sementara; kegagalan kanal tidak mengubah status transaksi/job.

### 2.6 Admin Panel
- RBAC MVP memiliki Super Admin, Admin, dan Moderator.
- Permission ditentukan per aksi dan objek.
- Tidak ada peran dengan akses default ke isi teks pengguna.
- Akses isi teks hanya untuk laporan/tiket relevan dengan persetujuan eksplisit, cakupan minimum, maksimal satu jam, dan audit log.
- Penyesuaian kredit harus melalui ledger, bukan edit saldo langsung.
- Perubahan role, harga, reward, model, dan konfigurasi sensitif memiliki alasan, nilai sebelum/sesudah, waktu efektif, versi, dan audit log.

### 2.7 Operasional
- Job memiliki ID unik, status, waktu, referensi reservasi kredit, dan versi model/config.
- Retry otomatis hanya untuk kegagalan sementara, maksimal dua kali, dengan exponential backoff dan jitter.
- Job idempotent.
- Pembatalan saat Waiting langsung menghentikan job dan melepas reservasi.
- Pembatalan saat Processing bersifat best-effort; status akhir mengikuti konfirmasi provider/worker.
- Job gagal yang tidak pulih otomatis masuk manual recovery dengan audit trail.

### 2.8 Nonfungsional
Ditambahkan 13 NFR untuk validasi backend, enkripsi, password hashing, rate limiting, keamanan unggahan, privasi log, retensi per lapisan, idempotensi, backup/restore, observability, aksesibilitas, performa, availability, dan lokalisasi.

## 3. Keputusan baru

- **DEC-156:** bonus harian menggunakan Asia/Jakarta, pukul 03.00, satu kali per tanggal kalender.
- **DEC-157:** model reservasi dan settlement kredit, tanpa tagihan di atas estimasi yang disetujui.
- **DEC-158:** kredit reward Guest berlaku 24 jam dan terikat sesi.
- **DEC-159:** reward iklan harus diverifikasi server-side; batas/nilai belum diaktifkan sebelum kebijakan provider diverifikasi.
- **DEC-160:** lifecycle transaksi pembayaran, verifikasi webhook, dan idempotensi.
- **DEC-161:** lifecycle tiket dan target respons awal dua hari kerja.
- **DEC-162:** preferensi notifikasi, opt-in promosi, dan retry.
- **DEC-163:** prinsip RBAC dan pembatasan akses isi teks.
- **DEC-164:** cancellation dan retry pekerjaan antrean.
- **DEC-165:** account linking tidak otomatis berdasarkan kesamaan email.
- **DEC-166:** pengguna dapat melihat dan mencabut sesi aktif.
- **DEC-167:** paket, tarif, reward, dan harga dikelola sebagai konfigurasi bertanggal efektif dan diaudit.

## 4. Hal yang sengaja belum difinalkan

Berikut tetap menjadi pekerjaan tahap 6 atau prasyarat validasi eksternal, bukan kekurangan requirement:
1. Payment gateway final dan metode yang benar-benar didukung provider.
2. Produk rewarded ads yang sah, kelayakan inventory, dan kebijakan Google/provider.
3. Harga paket, nilai kredit, tarif fitur, batas reward, dan unit economics.
4. Provider/model AI dan biaya per fitur.
5. Detail legal retensi, penghapusan, backup, dan pemrosesan oleh provider eksternal.
6. Implementasi 2FA, session token, encryption key management, dan secret management.
7. Target uptime/SLO, response time, concurrency, RPO/RTO, dan kapasitas.
8. Retensi tiket/notifikasi serta kalender hari kerja.
9. Permission matrix rinci per endpoint/aksi dan approval investigasi.
10. Detail UI dashboard, Admin Panel, tiket, notifikasi, dan pembayaran.

## 5. Batas klaim

- Audit ini melengkapi requirement dan keputusan produk tingkat tinggi; bukan bukti integrasi pembayaran, iklan, atau autentikasi telah dibangun.
- Nilai komersial tidak ditetapkan tanpa unit economics.
- Reward ads tidak boleh diaktifkan sebelum provider dan kebijakannya diverifikasi.
- NFR telah ditulis, tetapi target numerik performa dan availability masih menunggu benchmark/infrastruktur.
- Implementasi website tetap di luar cakupan tahap 1–6.

## 6. Sumber normatif

- [System Requirements Analysis](../plan/SYSTEM-REQUIREMENTS-ANALYSIS.md)
- [Decision Log](../plan/DECISION-LOG.md)
- [Requirements Elicitation Status](../plan/REQUIREMENTS-ELICITATION-STATUS.md)
- [Active Roadmap](../plan/ACTIVE-ROADMAP.md)

## 7. Addendum privacy dan legal readiness

SRS kemudian diperluas dengan FR-ACC-20/21 dan NFR-SEC-06 serta NFR-PRIV-03 sampai NFR-PRIV-09. DEC-168 sampai DEC-174 menetapkan no-training-by-default, consent terpisah, inventaris processor, cross-border transfer gate, incident response, data-subject requests, child-safety self-assessment, dan DPIA. Rincian checklist serta sumber resmi berada di [Privacy and Legal Readiness](PRIVACY-AND-LEGAL-READINESS.md). Ini adalah persyaratan desain dan launch gate, bukan klaim bahwa Lexora telah patuh atau terdaftar.

# AI Humanizer Plan

- **Status:** Rencana fitur tingkat tinggi; kebutuhan fungsional dirujuk ke SRS
- **Modul:** AI Humanizer
- **Bahasa:** Bahasa Indonesia dan Bahasa Inggris; teks campuran diproses dengan memperhatikan keterbatasan
- **Terakhir diperbarui:** 2026-11-17

## Peran dan sumber kebenaran

Dokumen ini menjelaskan arah fitur, alur konseptual, risiko kualitas, dan pekerjaan yang masih terbuka. Dokumen ini **bukan salinan kedua dari requirement**.

- Requirement normatif Humanizer berada di [System Requirements Analysis, bagian 4.4](SYSTEM-REQUIREMENTS-ANALYSIS.md#44-ai-humanizer), dengan ID FR-HUM-01 sampai FR-HUM-124.
- Penghapusan profil membedakan pekerjaan pengelolaan profil dari pekerjaan pemrosesan dokumen: pekerjaan pengelolaan profil yang terkait dibatalkan/ditolak, sedangkan pekerjaan dokumen yang sudah mulai berjalan menyelesaikan proses memakai snapshot profil saat mulai. Rincian normatif berada pada FR-HUM-118 dan FR-HUM-121.
- Alasan dan riwayat keputusan berada di [Decision Log](DECISION-LOG.md).
- Ringkasan kemajuan dan area elisitasi yang belum selesai berada di [Requirements Elicitation Status](REQUIREMENTS-ELICITATION-STATUS.md).

Jika ringkasan dalam dokumen ini berbeda dengan requirement atau keputusan yang disahkan, SRS dan Decision Log menjadi acuan.

## 1. Tujuan

Membantu pengguna menyunting teks agar lebih alami, jelas, dan sesuai gaya yang dipilih tanpa sengaja mengubah makna, fakta, atau maksud utama.

Humanizer adalah alat bantu penyuntingan. Fitur ini tidak boleh menjanjikan bahwa hasilnya pasti lolos AI Detector atau tidak dapat dikenali sebagai teks AI.

## 2. Cakupan kemampuan

Rincian perilaku dan batas setiap kemampuan tercatat satu kali di SRS. Peta berikut hanya membantu navigasi:

| Area | Cakupan | Requirement |
|---|---|---|
| Gaya bawaan dan profil personal | Enam gaya bawaan, sampel, kecukupan, versioning, pemulihan, privasi, dan akses audit | FR-HUM-01–36 |
| Input, editor, hasil, dan navigasi | Dokumen, editor, pemrosesan, hasil revisi, penyimpanan, perlindungan hasil belum tersimpan, dan aksesibilitas | FR-HUM-37–67 |
| Batas input dan pengelolaan profil/sampel | Batas karakter, file, profil, sampel, unduhan, Recently Deleted, dan pemulihan massal | FR-HUM-68–99 |
| Penghapusan akun dan ekspor data | Pending Deletion, ekspor data pribadi, riwayat ekspor, autentikasi ulang, dan rate limiting | FR-HUM-100–117 |
| Penghapusan profil dan konsistensi pekerjaan | Pembatalan, snapshot pekerjaan aktif, kegagalan atomik, dan retry penghapusan profil | FR-HUM-118–124 |

Catatan: FR-HUM-14 ditempatkan sesuai urutan ID di SRS dan menetapkan batas minimum setiap sampel. Peta ini tidak mengubah isi maupun status requirement.

## 2.1 Gaya bawaan MVP

Daftar gaya bawaan yang dipakai pada MVP mengikuti DEC-148:

| Gaya | Perilaku penyuntingan |
|---|---|
| **Akademik** | Mengutamakan struktur argumen, terminologi bidang, ketepatan, dan nada objektif. Tidak mengubah sitasi atau klaim sumber. |
| **Formal** | Menggunakan bahasa baku, kalimat tertata, dan ungkapan sopan untuk komunikasi umum. |
| **Profesional** | Mengutamakan kejelasan, keringkasan, fokus pada tujuan, dan nada kerja yang tepat. |
| **Santai** | Menggunakan bahasa percakapan yang natural dan mudah dibaca tanpa menghilangkan informasi penting. |
| **Informatif** | Mengutamakan penjelasan yang runtut, eksplisit, dan mudah dipahami pembaca. |
| **Kreatif** | Memberi ruang variasi diksi, ritme, dan ekspresi dengan tetap mempertahankan fakta serta maksud sumber. |

Gaya adalah preset register dan cara penyampaian, bukan tingkat intensitas. Semua gaya tunduk pada prinsip pelestarian makna, fakta, angka, nama, kutipan, dan terminologi penting.

## 3. Konsep profil gaya personal

Profil memerlukan minimal tiga sampel yang memenuhi 500 extended grapheme clusters per entri sebelum dapat digunakan. Batas ini adalah hard gate awal, bukan jaminan kecukupan. Sistem tetap menilai konsistensi dan keberagaman keseluruhan kumpulan, dapat meminta sampel tambahan, dan membatasi jumlah sampel hingga 20 per profil. Exact duplicate setelah normalisasi perbandingan tidak dihitung sebagai sampel independen kedua. Baseline tiga sampel harus dievaluasi kembali menggunakan hasil pilot.

Secara konseptual, siklus profil gaya terdiri dari:

1. Pengguna menyediakan satu atau lebih sampel tulisan.
2. Sistem memeriksa validitas sampel dan menilai kecukupan kumpulan sampel.
3. Jika memadai, sistem membangun representasi profil gaya.
4. Perubahan sampel pada profil yang telah terbentuk memicu evaluasi ulang sesuai aturan versioning.
5. Profil yang tersedia dapat dipilih oleh pemilik akun untuk pekerjaan Humanizer.

Profil gaya merupakan data yang berbeda dari dokumen sumber. Profil bersifat privat dan dikelola pemilik akun. Algoritma profiling, bentuk representasi internal, serta kebijakan retensi sampel mentah belum ditentukan secara teknis.

Aturan terperinci mengenai evaluasi, versi aktif/historis, pemulihan, konkurensi, dan audit berada di SRS serta Decision Log, bukan diulang di sini.

## 4. Dokumen dan ekstraksi

Format sumber yang direncanakan adalah TXT, DOCX, dan PDF. Sistem mengekstrak teks untuk ditinjau pengguna sebelum pemrosesan. Struktur dokumen yang kompleks tidak dijamin dipertahankan secara identik pada hasil keluaran. PDF berbasis gambar dapat memerlukan OCR.

Dokumen sumber tidak boleh ditimpa. Library ekstraksi, OCR, dan generator dokumen belum dipilih. Batas dan perilaku produk yang sudah disepakati tetap mengacu pada FR-HUM di SRS.

## 5. Alur pengguna konseptual

1. Pengguna login dan membuka Humanizer.
2. Pengguna mengetik/menempel teks atau mengunggah satu dokumen sesuai batas yang ditetapkan di SRS.
3. Jika dokumen diunggah, sistem mengekstrak teks dan menampilkannya di editor.
4. Pengguna meninjau serta mengedit isi editor.
5. Pengguna memilih gaya bawaan atau profil gaya personal yang tersedia.
6. Sistem memvalidasi input, profil, dan kapasitas yang relevan.
7. Sistem memproses teks, lalu menampilkan teks sumber, hasil revisi, dan perubahan.
8. Pengguna meninjau hasil, menyalin atau mengunduhnya, dan dapat memilih secara eksplisit apakah hasil disimpan ke riwayat.

Alur ini merupakan ringkasan. Validasi, batas, perilaku navigasi, penyimpanan, dan kondisi gagal yang wajib dipenuhi dijabarkan di SRS.

## 6. Siklus hidup sampel, akun, dan ekspor

Siklus penghapusan sampel, pemulihan, aktivitas akun, penghapusan akun, ekspor data pribadi, serta pengelolaan riwayat ekspor telah memiliki requirement tersendiri pada FR-HUM-89 sampai FR-HUM-117. Penghapusan profil dan dampaknya pada pekerjaan profil/dokumen diatur pada FR-HUM-118 sampai FR-HUM-124. FR-HUM-14 dipertahankan sebagai catatan historis dan telah dikonsolidasikan ke FR-HUM-70. Ketentuan ini mencakup pemisahan data yang terlihat oleh pengguna dari audit log internal, retensi, sinkronisasi lintas perangkat, autentikasi ulang, dan penanganan kegagalan.

Dokumen ini sengaja tidak menyalin ulang aturan tersebut. Untuk perilaku yang mengikat, gunakan SRS dan telusuri keputusan terkait melalui Decision Log.

## 7. Prinsip kualitas dan risiko

Prinsip kualitas:
- **Meaning preservation:** jangan mengubah klaim, angka, nama, kutipan, atau hubungan sebab-akibat tanpa dasar.
- **Factual integrity:** jangan menambahkan fakta atau referensi yang tidak ada pada sumber.
- **Traceability:** pengguna dapat membandingkan teks asli dan hasil revisi.
- **User control:** pengguna memutuskan menerima, mengubah, menyalin, menyimpan, atau menolak hasil.
- **Transparency:** hasil adalah saran penyuntingan, bukan jaminan hasil Detector tertentu.
- **Privacy by design:** minimalkan pengumpulan dan penyimpanan teks.

Risiko utama yang perlu diuji:
- Perubahan makna, fakta, angka, nama, kutipan, atau terminologi.
- Hasil terlalu generik dan menghilangkan karakter penulis.
- Bahasa campuran dan konteks yang tidak konsisten.
- Prompt injection di dalam input.
- Kebocoran teks ke layanan pihak ketiga.
- Sampel profil tidak representatif.
- Inkonsistensi akibat pemrosesan teks panjang/chunking.
- Kegagalan ekstraksi atau hilangnya struktur dokumen.

Pengujian kualitas perlu mencakup teks akademik, formal, informal, teknis, teks dengan angka/nama, Bahasa Indonesia, Bahasa Inggris, dan code-switching. Dataset evaluasi Humanizer harus dipisahkan dari data training/evaluasi Detector agar transformasi tidak merusak validitas pengukuran Detector.

## 8. Hal yang belum diputuskan

Daftar berikut hanya memuat isu yang masih terbuka. Keputusan produk yang sudah disepakati tidak dicantumkan kembali sebagai pekerjaan terbuka.

- Provider/model AI dan estimasi biaya operasional.
- Algoritma profiling serta kriteria adaptif untuk menilai kecukupan keseluruhan kumpulan sampel.
- Bentuk representasi profil dan retensi sampel mentah setelah profiling.
- Batas token internal, strategi chunking, penjagaan konteks, dan batas provider.
- Library ekstraksi dokumen, OCR, serta generator TXT/DOCX/PDF.
- Target kualitas, metrik, protokol evaluasi, dan dataset benchmark Humanizer.
- Nilai kuota penyimpanan riwayat, satuan penghitungan, dan detail teknis penghitungan kapasitas.
- Kebijakan teknis retensi cache, file sementara, backup, serta data yang diproses penyedia AI.
- Detail teknis autentikasi, otorisasi, sinkronisasi, antrean, retry, dan observability.
- Kriteria transaksi atomik dan pemulihan kegagalan penghapusan profil.
- Acceptance criteria terukur untuk setiap requirement Humanizer.

Status keputusan produk dan requirement yang sudah disepakati tetap merujuk pada Decision Log dan SRS. Butir di atas belum menjadi keputusan teknis atau persetujuan implementasi.

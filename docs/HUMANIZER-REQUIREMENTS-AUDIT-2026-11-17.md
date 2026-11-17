# Humanizer Requirements Audit

- **Tanggal:** 2026-11-17
- **Status:** Audit requirement selesai; pekerjaan desain dan acceptance criteria berlanjut pada tahap 4–6.
- **Ruang lingkup:** FR-HUM-01 sampai FR-HUM-124, Decision Log DEC-001 sampai DEC-149, AI Humanizer Plan, dan Requirements Elicitation Status.
- **Kewenangan:** Pemilik proyek mendelegasikan penyelesaian tahap 1–6 secara mandiri pada 2026-11-17. Keputusan baru di bawah ini dicatat sebagai delegated project decisions, bukan diklaim sebagai persetujuan historis dari sesi sebelumnya.

## 1. Hasil pemeriksaan struktur

- 124 requirement Humanizer ditemukan.
- Semua ID FR-HUM-01 sampai FR-HUM-124 tersedia, berurutan, dan unik.
- Tidak ada ID requirement duplikat atau hilang.
- Requirement baru FR-HUM-118 sampai FR-HUM-124 telah tercakup pada peta dokumen Humanizer.
- Decision Log berisi DEC-001 sampai DEC-149: 147 Accepted dan 2 Superseded (DEC-018 dan DEC-019).
- SRS dan Decision Log tetap menjadi sumber normatif; Feature Plan dan status elisitasi adalah dokumen navigasi.

## 2. Konflik dan inkonsistensi yang diperbaiki

| Area | Temuan | Tindakan |
|---|---|---|
| Jumlah profil | FR-HUM-06 masih menyatakan batas belum ditentukan, padahal DEC-090 dan FR-HUM-71 menetapkan 6 profil | FR-HUM-06 diselaraskan menjadi 1 profil utama + maksimal 5 tambahan |
| Penghapusan profil utama | FR-HUM-71 tidak menyebut pengecualian profil utama terakhir, bertentangan dengan FR-HUM-119 | FR-HUM-71 diselaraskan dengan DEC-139 dan DEC-140 |
| Minimum sampel | FR-HUM-14 mengulang dan lebih lemah daripada FR-HUM-70 | FR-HUM-14 dipertahankan sebagai jejak historis dan tidak lagi menjadi acceptance criterion terpisah |
| Hapus semua sampel | FR-HUM-75 tidak eksplisit menyatakan soft-delete, sedangkan FR-HUM-86 memberi masa pemulihan 30 hari | FR-HUM-75 kini secara eksplisit memindahkan sampel ke Recently Deleted |
| Penggantian dokumen | Konfirmasi mengganti dokumen berpotensi menghilangkan teks lama jika ekstraksi file baru gagal | Penggantian dibuat atomik: editor lama hanya diganti setelah ekstraksi baru berhasil |
| Rate limiting ekspor | FR-HUM-117 belum menentukan kapan jeda 30 detik dimulai | DEC-145 menetapkan waktu server setelah transaksi mencapai status akhir Failed |
| Penghitungan karakter | Belum ada konvensi yang konsisten untuk combining marks, emoji, dan CRLF | DEC-146 menetapkan extended grapheme clusters berdasarkan UAX #29, Unicode 18.0.0 |
| Gaya bawaan | Daftar gaya masih berupa kandidat | DEC-148 menetapkan enam gaya MVP |
| Kecukupan profil | Kriteria adaptif belum memiliki hard gate minimum sampel | DEC-149 menetapkan minimum tiga sampel yang memenuhi 500 grapheme clusters per entri; kualitas tetap dinilai adaptif |

## 3. Keputusan baru yang dicatat

- **DEC-145:** cooldown rate limit dihitung sejak transaksi gagal mencapai status akhir Failed menurut waktu server. Cooldown berlaku per akun lintas perangkat.
- **DEC-146:** seluruh batas karakter Humanizer menggunakan extended grapheme clusters sesuai Unicode 18.0.0 UAX #29. Penghitung antarmuka dan backend harus konsisten; backend otoritatif.
- **DEC-147:** penggantian dokumen hanya mengganti isi editor setelah ekstraksi dokumen baru berhasil. Kegagalan ekstraksi mempertahankan seluruh isi lama.
- **DEC-148:** gaya bawaan MVP adalah Akademik, Formal, Profesional, Santai, Informatif, dan Kreatif.
- **DEC-149:** profil memerlukan minimal tiga sampel layak, masing-masing minimal 500 grapheme clusters. Tiga sampel adalah hard gate, bukan jaminan kecukupan. Exact duplicate tidak dihitung sebagai sampel independen kedua. Kualitas dan keberagaman tetap dievaluasi adaptif.

Keputusan minimum tiga sampel adalah baseline produk yang masih harus dikalibrasi pada pilot. Jangan mengklaim angka tersebut sebagai hasil penelitian empiris.

## 4. Interaksi penting yang telah diperjelas

- **FR-HUM-118 dan FR-HUM-121:** penghapusan profil membatalkan pekerjaan pengelolaan profil, tetapi tidak membatalkan pekerjaan Humanizer dokumen yang sudah mulai berjalan. Pekerjaan dokumen tersebut menyelesaikan proses dengan snapshot profil saat mulai.
- **FR-HUM-122 sampai FR-HUM-124:** kegagalan penghapusan harus mempertahankan data secara utuh; retry merupakan permintaan baru; pembatalan hanya diterima sebelum tahap eksekusi.
- **FR-HUM-73, FR-HUM-119, FR-HUM-120:** profil utama terakhir dapat dihapus tanpa pengganti; jika masih ada profil lain, pengguna harus memilih pengganti sebelum menghapus profil utama.
- **FR-HUM-75, FR-HUM-86, FR-HUM-89, FR-HUM-90:** hapus biasa masuk Recently Deleted; penghapusan profil dapat memusnahkan sampel yang berada di Recently Deleted; penghapusan permanen memerlukan konfirmasi.
- **FR-HUM-51 sampai FR-HUM-67:** hasil yang belum disimpan, navigasi, konfirmasi, fokus keyboard, dan pengumuman screen reader harus diperlakukan sebagai satu alur yang saling terkait.
- **FR-HUM-100 sampai FR-HUM-117:** ekspor data, kuota, retensi paket, status pekerjaan, sinkronisasi, autentikasi ulang, transaksi atomik, dan rate limiting perlu dipetakan ke lifecycle yang konsisten.

## 5. Sisa pekerjaan desain Humanizer

Hal berikut tidak lagi merupakan konflik requirement. Hal tersebut merupakan pekerjaan System Design, evaluasi, atau acceptance criteria:

1. **Profil gaya:** desain algoritma profiling, metrik konsistensi/keberagaman, representasi profil, serta kebijakan retensi sampel mentah. Baseline tiga sampel perlu diuji.
2. **Pemrosesan AI:** pemilihan provider/model, biaya, batas token, chunking, context preservation, retry, timeout, dan fallback.
3. **Dokumen:** ekstraksi TXT/DOCX/PDF, dukungan PDF berbasis gambar/OCR, batas file input pekerjaan, penanganan struktur, dan generator hasil.
4. **Hasil dan riwayat:** kuota riwayat, satuan kapasitas, retensi, penyimpanan sementara, dan perilaku saat kuota penuh.
5. **Privasi dan keamanan:** retensi cache/temp files/backup, penghapusan turunan data, akses audit, RBAC, dan data yang dikirim ke provider AI.
6. **Concurrency dan reliability:** state machine pembaruan/pemulihan/penghapusan profil, idempotensi, snapshot, cancellation, dan transaksi atomik.
7. **Kualitas:** benchmark Humanizer, meaning preservation, factual integrity, style similarity, readability, code-switching, dan human review.
8. **Aksesibilitas:** validasi modal/alert dialog dan pengumuman screen reader pada kombinasi browser dan teknologi bantu yang didukung.
9. **Acceptance criteria:** setiap requirement harus diturunkan menjadi kondisi Given/When/Then atau bentuk uji ekuivalen pada tahap 4.

## 6. Risiko dan batas klaim

- Kelulusan audit ini berarti requirement telah diperiksa dari sisi struktur, konsistensi lintas dokumen, dan gap yang dapat diidentifikasi. Ini bukan bukti bahwa model Humanizer berkualitas atau bahwa semua perilaku sudah diuji.
- Minimum tiga sampel adalah baseline keputusan, bukan ambang empiris final.
- Gaya bawaan telah ditetapkan, tetapi contoh hasil dan evaluasi tiap gaya masih perlu dibuat.
- Kebijakan retensi, backup, dan data provider harus diperiksa terhadap kebutuhan hukum dan kontrak sebelum produksi.
- Provider/model AI, harga, kuota riwayat, dan target kualitas belum diputuskan.
- Tahap implementasi website tetap di luar cakupan.

## 7. Sumber

- [System Requirements Analysis](../plan/SYSTEM-REQUIREMENTS-ANALYSIS.md)
- [Decision Log](../plan/DECISION-LOG.md)
- [AI Humanizer Plan](../plan/AI-HUMANIZER-PLAN.md)
- [Requirements Elicitation Status](../plan/REQUIREMENTS-ELICITATION-STATUS.md)
- [Unicode Standard Annex #29, Unicode 18.0.0](https://www.unicode.org/reports/tr29/tr29-49.html)

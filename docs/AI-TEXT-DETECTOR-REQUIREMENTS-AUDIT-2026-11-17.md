# AI Text Detector Requirements Audit

- **Tanggal:** 2026-11-17
- **Status:** Audit requirement produk selesai; pemilihan model, benchmark, dan acceptance criteria tetap menjadi pekerjaan tahap berikutnya.
- **Ruang lingkup:** FR-DET-01 sampai FR-DET-17, FR-GEN/FR-FILE/FR-ACC terkait, DEC-003, DEC-015 sampai DEC-019, dan DEC-150 sampai DEC-155.
- **Kewenangan:** Pemilik proyek mendelegasikan penyelesaian tahap 1–6 secara mandiri pada 2026-11-17. Keputusan baru dicatat sebagai delegated project decisions.

## 1. Temuan audit awal

SRS sebelumnya hanya memiliki 11 requirement Detector. Cakupannya belum cukup untuk mendefinisikan perilaku hasil, ketidakpastian, bahasa yang tidak didukung, ekspor laporan, dan agregasi analisis kalimat.

Audit memperluas cakupan menjadi 17 requirement. Semua ID FR-DET-01 sampai FR-DET-17 kini berurutan dan unik.

## 2. Perubahan requirement

| Area | Hasil audit |
|---|---|
| Ringkasan dokumen | Menetapkan satu kategori keseluruhan, ringkasan, dan peringatan |
| Analisis per kalimat | Menyediakan indikasi dan penjelasan yang dapat ditelusuri; segmen pendek dapat menjadi UNCERTAIN |
| Penjelasan | Hanya menjelaskan sinyal yang benar-benar dihitung; tidak mengarang alasan |
| Kategori | Memisahkan MIXED dari UNCERTAIN |
| Keterbatasan | Memberi peringatan untuk teks pendek, bahasa campuran, bahasa/domain tidak didukung, ekstraksi tidak lengkap, dan bukti lemah |
| Batas klaim | Tidak boleh menjadi bukti pasti atau satu-satunya dasar tindakan akademik/disipliner |
| Skor | MVP tidak menampilkan skor numerik/persentase sebelum kalibrasi terbukti |
| Handoff | Hasil hanya dikirim ke Humanizer setelah tindakan eksplisit pengguna |
| Panjang input | Maksimal 20.000 extended grapheme clusters, sama untuk Guest dan pengguna terdaftar |
| Input | Mengetik/menempel dan unggah TXT, DOCX, PDF |
| Minimum input | Tidak ada hard minimum; teks pendek dapat menghasilkan UNCERTAIN |
| MIXED | Hanya jika terdapat indikasi memadai untuk pola HUMAN dan AI pada bagian berbeda |
| Bahasa | Bahasa Indonesia dan Inggris; code-switching dengan peringatan; bahasa lain tidak diberi kesimpulan kepengarangan |
| Agregasi | Berdasarkan bukti segmen dan metode tervalidasi, bukan simple majority vote tanpa evaluasi |
| Ekspor | Laporan dapat diunduh sebagai TXT, DOCX, atau PDF |
| Audit | Metadata internal mencatat waktu, model/config version, bahasa, dan warning |

## 3. Keputusan baru

- **DEC-150:** maksimum 20.000 extended grapheme clusters, berlaku sama untuk Guest dan pengguna terdaftar; validasi backend dilakukan sebelum antrean, pemanggilan model, atau pemotongan kredit.
- **DEC-151:** definisi MIXED dan UNCERTAIN dipisahkan secara eksplisit.
- **DEC-152:** MVP tidak menampilkan skor numerik atau persentase kepengarangan.
- **DEC-153:** analisis per kalimat menandai segmen tanpa bukti memadai sebagai UNCERTAIN; agregasi dokumen harus divalidasi dan tidak memakai simple majority vote tanpa evaluasi.
- **DEC-154:** bahasa utama Indonesia dan Inggris; code-switching diberi peringatan; bahasa di luar cakupan tidak mendapat label kepengarangan.
- **DEC-155:** laporan Detector dapat diunduh sebagai TXT, DOCX, atau PDF.

Konvensi penghitungan karakter mengikuti DEC-146, yaitu extended grapheme clusters Unicode 18.0.0. Batas 20.000 adalah batas produk MVP, bukan batas token model.

## 4. Temuan riset eksternal

### 4.1 Performa detector bergantung pada konteks

Hadra, Cambridge, dan Mesbah (2026) menguji dua detector komersial pada 192 teks akademik. Akurasi yang dilaporkan adalah 0,69 dan 0,61; kedua alat kesulitan membedakan teks hybrid. Kinerja juga berubah menurut panjang teks dan genre. Temuan ini mendukung kebutuhan label UNCERTAIN, pengujian per domain, dan larangan menggunakan hasil sebagai satu-satunya dasar keputusan.

### 4.2 Hasil benchmark tidak selalu searah

Van Vlasselaer, Van Droogenbroeck, dan Spruyt (2026) menguji empat detector pada 160 dokumen sintetis dengan empat kondisi authorship. Satu alat tampil lebih baik pada dataset tersebut, tetapi para penulis tetap menyarankan agar hasil detector tidak menjadi satu-satunya bukti untuk keputusan berisiko tinggi. Studi ini tidak membatalkan temuan lain; hasil yang berbeda justru menunjukkan ketergantungan pada data, tool, dan setup evaluasi.

### 4.3 Bukti khusus Bahasa Indonesia masih terbatas

Hakim, Umam, dan Yuniarti (2026) mengevaluasi IndoBERT, SVM, dan Naive Bayes pada subset M4 Indonesia. Mereka menggunakan group split berdasarkan ID sumber untuk mencegah pasangan artikel manusia dan AI bocor lintas split. Pada test set, SVM memperoleh accuracy 97,06% dan IndoBERT 95,85%. Dataset tersebut terbatas pada berita dan satu generator ChatGPT; penulis menyatakan generalisasi ke esai akademik dan model lain masih perlu diuji. Studi itu juga menunjukkan bahwa split yang tidak dikelompokkan sebelumnya memberi kesan keunggulan model yang ternyata berasal dari data leakage.

### 4.4 Implikasi untuk Lexora

- Model final tidak dipilih hanya dari satu angka accuracy.
- SVM/TF-IDF harus menjadi baseline pembanding bagi Transformer.
- Group split wajib dipertahankan untuk pasangan dan turunan sumber.
- Evaluasi harus mencakup Bahasa Indonesia, Bahasa Inggris, code-switching, genre, panjang, dan beberapa generator.
- False positive pada tulisan manusia harus menjadi metrik keselamatan utama.
- MIXED, human-edited AI, AI-assisted human writing, dan paraphrase harus diuji terpisah.
- Threshold dan kalibrasi hanya dipilih dari validation set.
- Test set harus dikunci dan tidak digunakan untuk tuning.

## 5. Pekerjaan yang masih terbuka

1. Definisi operasional label dataset dan panduan anotasi per kalimat.
2. Model final, konfigurasi training, tokenizer, dan strategi inference.
3. Token limit internal, chunking, overlap, context preservation, dan agregasi final.
4. Threshold, kalibrasi, dan target false-positive rate per bahasa/domain.
5. Benchmark multi-domain dan multi-generator dengan ground truth yang dapat ditelusuri.
6. Batas ukuran file, OCR, ekstraksi, dan perilaku PDF yang tidak terbaca mengikuti audit modul pendukung.
7. Format visual laporan dan accessibility acceptance criteria.
8. Monitoring drift, versi model, rollback, dan evaluasi ulang.
9. Acceptance criteria terukur untuk seluruh FR-DET pada tahap 4.

## 6. Batas klaim

- Audit ini memverifikasi kelengkapan dan konsistensi requirement, bukan performa model Lexora.
- Angka dari penelitian eksternal tidak dapat dipindahkan menjadi klaim akurasi Lexora.
- Batas 20.000 karakter adalah keputusan produk MVP; kelayakan token dan biaya harus diuji pada desain teknis.
- Kategori HUMAN/AI/MIXED/UNCERTAIN tetap merupakan indikasi berdasarkan pola teks, bukan bukti asal-usul atau niat penulis.
- Training model tetap menunggu audit sumber, pilot, kualitas anotasi, dan protokol evaluasi.

## 7. Sumber

- [Hadra et al. (2026), Evaluating the accuracy and reliability of AI content detectors in academic contexts](https://link.springer.com/article/10.1007/s40979-026-00213-1).
- [Van Vlasselaer et al. (2026), Who wrote this? Evaluating the reliability of AI detection tools in higher education](https://link.springer.com/article/10.1007/s40979-026-00226-w).
- [Hakim et al. (2026), Fine-Tuning IndoBERT for Detecting AI-Generated Indonesian Text](https://doi.org/10.59562/intec.v5i4.14451).
- [NIST (2025), 2024 GenAI Pilot Study: Text-to-Text Evaluation](https://www.nist.gov/publications/2024-nist-genai-pilot-study-text-text-evaluation-overview-and-results).

# AI Text Detector Plan

Status: **Draft rancangan produk dan riset; kebutuhan produk awal telah dielisitasi**  
Modul: AI Text Detector  
Bahasa: Bahasa Indonesia dan Bahasa Inggris; code-switching dengan peringatan keterbatasan  
Terakhir ditinjau: 2026-11-17

Rincian kebutuhan produk yang disepakati berada di [System Requirements Analysis](SYSTEM-REQUIREMENTS-ANALYSIS.md), khususnya bagian 4.3 AI Text Detector. Dokumen ini mempertahankan fokus rencana produk tingkat tinggi dan riset metodologi model; ringkasan kemajuan elisitasi berada di [Requirements Elicitation Status](REQUIREMENTS-ELICITATION-STATUS.md).

## 1. Tujuan

Membantu pengguna memperoleh indikasi apakah suatu teks memiliki karakteristik tulisan manusia, teks yang dihasilkan AI, atau campuran keduanya.

Detector tidak boleh diposisikan sebagai alat pembuktian mutlak. Hasil model adalah estimasi berdasarkan data dan distribusi yang dipelajari. Tulisan manusia dapat salah ditandai sebagai AI dan teks AI dapat tidak terdeteksi.

## 2. Kebutuhan produk yang telah disepakati

- Target utama pengguna adalah mahasiswa dan pelajar, untuk kebutuhan akademik maupun umum.
- Detector dan Humanizer memiliki prioritas setara dan dapat digunakan mandiri.
- Hasil Detector dapat dikirim ke Humanizer hanya setelah tindakan pengguna.
- Bahasa yang didukung adalah Bahasa Indonesia dan Bahasa Inggris.
- Teks campuran Indonesia-Inggris dapat dianalisis dengan peringatan keterbatasan.
- Input Detector menyediakan dua cara: mengetik/menempelkan teks langsung dan mengunggah file TXT, DOCX, atau PDF.
- AI Text Detector memiliki batas maksimum 20.000 extended grapheme clusters, sama untuk Guest dan pengguna terdaftar. Tidak ada batas minimum karakter produk; teks yang terlalu pendek untuk menghasilkan bukti memadai memperoleh hasil UNCERTAIN, bukan dipaksa menjadi HUMAN/AI.
- Batas yang ditampilkan kepada pengguna menggunakan extended grapheme clusters sesuai Unicode 18.0.0 UAX #29. Sistem tetap membatasi token internal sesuai model.
- Batas input Detector dapat berbeda dari Humanizer.
- Pemrosesan pendek/panjang bersifat adaptif; teks panjang dapat dipecah dengan chunking.
- Output mencakup satu kategori keseluruhan, ringkasan, analisis per kalimat, penjelasan yang dapat ditelusuri, dan peringatan/keterbatasan.
- Kategori MIXED hanya digunakan jika terdapat indikasi memadai untuk pola HUMAN dan AI pada bagian berbeda. UNCERTAIN digunakan ketika bukti tidak cukup, bertentangan, atau berada di luar bahasa/domain yang didukung.
- MVP tidak menampilkan skor numerik atau persentase kepengarangan. Skor internal tidak boleh disebut probabilitas terkalibrasi sebelum validasi kalibrasi.
- Label keseluruhan diturunkan dari bukti segmen dengan metode agregasi yang divalidasi; bukan simple majority vote tanpa evaluasi.
- Laporan hasil dapat diunduh sebagai TXT, DOCX, atau PDF.
- Kategori produk: HUMAN, AI, MIXED, UNCERTAIN.
- Hasil dapat ditampilkan di website dan diunduh sebagai TXT, DOCX, atau PDF.
- Pengguna dapat menyalin seluruh atau sebagian hasil.

## 3. Kategori label produk dan metodologi

| Label produk | Makna umum |
|---|---|
| HUMAN | Karakteristik teks lebih konsisten dengan tulisan manusia |
| AI | Karakteristik teks lebih konsisten dengan teks yang dihasilkan AI |
| MIXED | Teks menunjukkan indikasi kontribusi manusia dan AI |
| UNCERTAIN | Bukti tidak cukup untuk kesimpulan yang dapat diandalkan |

Kategori produk tersebut belum menggantikan definisi operasional label dataset. Label dokumen tidak otomatis boleh diwariskan ke setiap kalimat. Anotasi tingkat kalimat memerlukan bukti dan aturan tersendiri.

UNCERTAIN adalah kategori hasil produk. Penanganannya dalam training/evaluasi tetap mengikuti keputusan metodologis terpisah dan belum menjadi kelas training utama.


### 3.1 Aturan interpretasi hasil MVP

| Label | Penggunaan | Bukan berarti |
|---|---|---|
| **HUMAN** | Pola teks lebih konsisten dengan data tulisan manusia yang menjadi dasar model | Bukti bahwa seseorang pasti menulis seluruh teks |
| **AI** | Pola teks lebih konsisten dengan data teks AI yang menjadi dasar model | Bukti bahwa seluruh teks dibuat AI atau bukti pelanggaran |
| **MIXED** | Ada indikasi memadai untuk pola HUMAN dan AI pada bagian teks yang berbeda | Sekadar hasil yang tidak stabil atau banyak segmen UNCERTAIN |
| **UNCERTAIN** | Bukti tidak cukup, bertentangan, input terlalu pendek, bahasa/domain tidak didukung, atau kualitas ekstraksi tidak memadai | Kategori HUMAN atau AI yang tersamar |

Hasil per kalimat bersifat indikatif. Kalimat yang terlalu pendek atau tidak memiliki konteks memadai ditandai UNCERTAIN/insufficient context. Ringkasan dokumen tidak boleh dihitung dengan mayoritas jumlah kalimat tanpa validasi; metode agregasi harus diuji pada validation set dan dibekukan sebelum evaluasi final.

Penjelasan hanya boleh menyebut sinyal yang benar-benar dihitung dan dapat ditelusuri. Sistem tidak boleh mengarang alasan linguistik menggunakan generative model tanpa bukti terukur.

### 3.2 Batas bahasa dan panjang input

- Bahasa yang didukung MVP: Bahasa Indonesia dan Bahasa Inggris.
- Teks campuran Indonesia-Inggris diproses dengan peringatan keterbatasan.
- Jika bahasa dominan di luar cakupan atau tidak dapat diidentifikasi dengan memadai, sistem menampilkan UNCERTAIN/unsupported language dan tidak memberi label kepengarangan.
- Batas input maksimum: 20.000 extended grapheme clusters. Tidak ada minimum input yang menolak proses; teks pendek dapat menghasilkan UNCERTAIN.
- Backend menjadi otoritas validasi panjang. Penghitungan mengikuti DEC-146 dan harus sama dengan penghitung antarmuka.
- Batas token internal dan chunking tetap ditentukan oleh model dan diuji terpisah dari batas karakter produk.

## 4. Rencana pendekatan eksperimen

Urutan eksperimen kandidat:
1. Majority-class baseline.
2. TF-IDF dengan Logistic Regression dan SVM sebagai baseline kuat yang wajib dibandingkan.
3. IndoBERT-Lite sebagai kandidat backbone.
4. IndoBERT Base sebagai kandidat backbone.
5. XLM-RoBERTa atau mDeBERTa sebagai kandidat multilingual pembanding.
6. Perbandingan model berbasis kalimat dengan pendekatan yang menggunakan konteks dokumen.
7. Evaluasi optimasi inference, termasuk ONNX INT8 dibanding FP32 jika relevan.

Jangan mengasumsikan Transformer selalu lebih baik daripada model klasik. Pemilihan harus berdasarkan held-out group split dan evaluasi lintas domain/model generator.

Nama model di atas adalah kandidat pretrained backbone, bukan detector siap pakai dan bukan keputusan final pemilihan model.

Kandidat yang pernah disebut:
- indobenchmark/indobert-lite-base-p2
- indobenchmark/indobert-base-p2
- XLM-RoBERTa-base
- mDeBERTa-v3-base

Pemilihan akhir harus didasarkan pada evaluasi data, lisensi, biaya komputasi, latensi, dan performa pada domain target.

## 5. Metrik dan protokol evaluasi

Metrik minimum:
- Macro F1.
- Precision, recall, dan F1 per kelas.
- False Positive Rate pada kelas HUMAN sebagai metrik keselamatan utama.
- False Negative Rate pada kelas AI.
- Confusion matrix dan balanced accuracy.
- AUROC dan PR-AUC bila sesuai dengan distribusi kelas.
- Brier score, Expected Calibration Error, dan reliability diagram jika model menghasilkan skor internal.
- Latency, throughput, dan peak RAM.

Protokol evaluasi wajib:
1. Pisahkan train/validation/test berdasarkan group/source lineage; pasangan human-AI, parafrasa, dan turunan sumber tidak boleh tersebar lintas split.
2. Simpan test set terkunci. Threshold, kalibrasi, dan model selection hanya menggunakan validation set.
3. Laporkan metrik terpisah untuk Bahasa Indonesia, Bahasa Inggris, code-switching, domain akademik, berita, profesional, teknis, dan informal.
4. Laporkan metrik menurut rentang panjang teks, termasuk input pendek yang harus dapat menghasilkan UNCERTAIN.
5. Uji HUMAN, AI, MIXED, serta kondisi AI-assisted/human-edited dan AI-paraphrased. UNCERTAIN dievaluasi sebagai perilaku abstention, bukan dipaksakan menjadi kelas training utama.
6. Uji beberapa generator/provider dan versi model, bukan hanya satu generator.
7. Laporkan confidence interval, ukuran sampel, dan jumlah false positive secara eksplisit. Jangan hanya melaporkan accuracy.
8. Pilih threshold dengan prioritas membatasi false positive pada HUMAN. Jika suatu bahasa/domain belum memenuhi target keselamatan yang ditetapkan sebelum test, fitur harus memberi peringatan pembatasan atau tidak mengklaim dukungan untuk domain tersebut.

Target numerik kualitas dan batas false positive belum ditetapkan; target harus disahkan setelah pilot dan sebelum test set final dibuka. Test set tidak boleh dipakai untuk memilih target atau threshold.

## 6. Risiko metodologis dan batas klaim

- Dataset publik tidak otomatis berlabel HUMAN.
- Gaya penulisan, topik, panjang teks, bahasa, dan sumber dapat menjadi shortcut bagi model.
- Teks turunan, parafrasa, pasangan prompt-output, dan versi suntingan dapat menyebabkan data leakage.
- Generator AI dari sedikit provider dapat membuat evaluasi tidak mewakili penggunaan nyata.
- False positive terhadap tulisan manusia dapat merugikan pengguna.
- Skor probabilitas tidak boleh dipresentasikan sebagai persentase kepastian kepengarangan tanpa kalibrasi dan penjelasan yang benar.
- Penjelasan hasil tidak boleh mengarang alasan yang tidak didukung analisis.

## 7. Hal yang belum diputuskan

- Model final dan konfigurasi training.
- Definisi operasional kelas dan panduan anotasi.
- Mekanisme confidence, threshold, dan kalibrasi.
- Skema inference dan API.
- Batas token internal, strategi chunking, dan metode agregasi final.
- Format laporan final dan desain UI.
- Target akurasi/performa yang realistis.
- Strategi monitoring drift dan evaluasi ulang.
- Apakah model berjalan pada server sendiri atau layanan eksternal.

## 8. Riset eksternal dan implikasi desain

Riset terbaru menunjukkan bahwa performa detector berubah menurut domain, panjang teks, tipe penulis, model generator, dan campuran human-AI. Studi Hadra et al. (2026) pada 192 teks akademik melaporkan performa dua detector komersial yang moderat dan kesulitan besar pada teks hybrid. Studi Van Vlasselaer et al. (2026) menemukan variasi antartool pada data uji terkontrol dan menegaskan bahwa hasil tidak boleh menjadi satu-satunya dasar keputusan berisiko tinggi.

Bukti khusus Bahasa Indonesia juga perlu dibaca hati-hati. Hakim et al. (2026) menggunakan M4 Indonesian dengan group split berdasarkan ID sumber untuk mencegah pasangan human/AI bocor lintas split. Dalam studi tersebut SVM mencapai 97,06% accuracy dan IndoBERT 95,85%; data terbatas pada domain berita dan satu generator ChatGPT. Studi itu juga menunjukkan keunggulan IndoBERT pada split non-group sebelumnya sebagian besar berasal dari data leakage. Karena itu, Lexora wajib memakai group split dan menguji lintas domain/generator.

Sumber:
- Hadra, M., Cambridge, K., & Mesbah, M. (2026), [Evaluating the accuracy and reliability of AI content detectors in academic contexts](https://link.springer.com/article/10.1007/s40979-026-00213-1).
- Van Vlasselaer, M., Van Droogenbroeck, F., & Spruyt, B. (2026), [Who wrote this? Evaluating the reliability of AI detection tools in higher education](https://link.springer.com/article/10.1007/s40979-026-00226-w).
- Hakim, F. I., Umam, K., & Yuniarti, W. D. (2026), [Fine-Tuning IndoBERT for Detecting AI-Generated Indonesian Text](https://doi.org/10.59562/intec.v5i4.14451).
- NIST (2025), [2024 GenAI Pilot Study: Text-to-Text Evaluation](https://www.nist.gov/publications/2024-nist-genai-pilot-study-text-text-evaluation-overview-and-results).

Temuan eksternal ini menjadi dasar kehati-hatian desain, bukan jaminan bahwa model Lexora akan memperoleh hasil yang sama.

## 9. Gerbang sebelum implementasi model

Jangan mulai training serius sebelum:
1. Struktur data dan schema ditetapkan.
2. Uji prosedur sintetis lulus.
3. Sumber data, provenance, dan lisensi diaudit.
4. Pilot 200-500 dokumen dikumpulkan dan dievaluasi kualitasnya.
5. Aturan anotasi dan split berbasis grup ditetapkan.
6. Baseline dan protokol evaluasi dapat diulang.

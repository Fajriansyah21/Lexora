# Dataset and Model Research Plan

Status: **Rencana riset; beberapa keputusan metodologis telah disepakati**  
Modul terkait: AI Text Detector  
Terakhir ditinjau: 2026-11-17

## 1. Prinsip sumber data

Rencana dataset menggunakan pendekatan hybrid:
- Sumber publik yang telah melalui audit sumber, lisensi, dan kelayakan penggunaan.
- Data terkontrol yang dikumpulkan dengan provenance dan dasar penggunaan yang jelas.

Tidak ada sumber publik yang otomatis dianggap sebagai teks HUMAN atau otomatis disetujui untuk training. Label, hak penggunaan, dan provenance harus diverifikasi.

## 2. Kategori data

Kelas utama:
- `HUMAN`
- `AI`
- `MIXED`

`UNCERTAIN` dikelola di luar kelas training utama sampai ada keputusan metodologis lebih lanjut.

Setiap record perlu memiliki provenance yang cukup untuk menelusuri sumber, proses pengumpulan, transformasi, dan anotasinya. Dataset Record JSON Schema v1.0 dan logical database schema tersedia sebagai rancangan untuk menguji prosedur; keduanya belum disahkan sebagai schema produksi final.

## 3. Target dan urutan pengumpulan

Urutan yang disepakati:
1. Menyelesaikan blueprint pengumpulan data.
2. Menjalankan pilot 200–500 dokumen.
3. Mengevaluasi prosedur dan kualitas data.
4. Merevisi prosedur berdasarkan bukti.
5. Memperluas dataset menuju target 5.000–10.000 dokumen.
6. Menyiapkan training dan eksperimen model.

Target 5.000–10.000 adalah sasaran skala dataset jangka lanjut, bukan jumlah pilot awal dan bukan klaim bahwa data tersebut sudah tersedia.

## 4. Pengujian prosedur sintetis sebelum pilot

Prioritas aktif saat ini adalah menguji mekanisme pengolahan dataset menggunakan fixture sintetis, bukan mengumpulkan data nyata atau melatih model.

Urutan:
1. JSON Schema dan struktur record.
2. Sentence offsets terhadap teks sumber.
3. Editing history, versi, dan lineage.
4. Exact dan near-duplicate detection.
5. Group-based split.

Setiap pengujian harus mencakup kasus valid, invalid, boundary, dan adversarial. Hasil harus dapat diulang dan dicatat.

### 4.1 Hasil uji prosedur sintetis (2026-11-17)

Harness dan fixture telah ditambahkan:
- `scripts/synthetic_dataset_checks.py`
- `tests/synthetic_dataset/fixtures/valid_document.json`
- `tests/synthetic_dataset/fixtures/invalid_documents.json`
- `tests/synthetic_dataset/test_synthetic_pipeline.py`
- `requirements-test.txt`

Hasil pengujian lokal: **27/27 test cases lulus** menggunakan Python 3.13.5 dan jsonschema 4.26.0. Cakupan: JSON Schema (4), sentence offsets (5), editing history/lineage (8), deduplikasi (4), dan group-based split (6). Perintah reproduksi tersedia pada `tests/synthetic_dataset/README.md`.

Batas interpretasi:
- Pengujian ini memverifikasi prosedur dan perilaku fixture sintetis, bukan kualitas atau kebenaran label data nyata.
- Near-duplicate threshold 0.88 hanya parameter pengujian, belum menjadi threshold produksi.
- Split hash-bucket deterministik mendekati 70/15/15 berdasarkan jumlah grup, bukan jumlah dokumen atau distribusi kelas. Desain stratifikasi dan challenge holdout nyata tetap memerlukan keputusan riset.
- Workflow GitHub Actions run #4 berhasil pada commit `f7c0a620f68e41c8f72c8f966c8a903ca8e55c96`: 29/29 test lulus pada Python 3.12.16 dan jsonschema 4.26.0, termasuk uji mapping editing-history template ke export schema. [Log CI](https://github.com/Fajriansyah21/Website-AI-Ditector/actions/runs/44026960961).
- Hasil ini tidak mengesahkan pilot, penggunaan dataset publik, consent, maupun training.


### 4.2 Konsistensi editing history

Template intake dan bentuk ekspor awalnya memiliki struktur berbeda. Mapping eksplisit kini didokumentasikan di [Editing History Mapping v1](../docs/EDITING-HISTORY-MAPPING-v1.md): versions[] dipetakan ke editing_history[], metadata review ke source/provenance, dan bukti per versi dipertahankan. JSON Schema telah diperluas untuk provenance_evidence dan reviewer_note. Uji integrasi template-ke-ekspor menjadi bagian dari suite sintetis. Mapping ini memvalidasi struktur, bukan kebenaran evidence.

## 5. Pencegahan data leakage

- Pasangan prompt-output, parafrasa, revisi, dan turunan dari sumber yang sama perlu dikelompokkan.
- Group/pair/source lineage harus dipertimbangkan sebelum split.
- Tidak boleh ada kelompok terkait yang tersebar ke train, validation, dan test.
- Split berbasis grup lebih penting daripada sekadar random split record.
- Test set harus dijaga sebagai evaluasi akhir yang tidak digunakan untuk tuning.

Skema rasio split 70/15/15 pernah dibahas sebagai kandidat, tetapi perlu disahkan bersama definisi group dan kebutuhan evaluasi sebelum dianggap final.

## 6. Audit sumber dan kandidat data

Sumber yang pernah disebut sebagai kandidat eksplorasi:
- IndoNLU.
- Leipzig Corpora.
- OSCAR.
- CC-100.
- Wikipedia dumps.
- `sansaks/dataset_indonesia`.

Daftar ini bukan daftar sumber yang telah disetujui. Setiap kandidat perlu diperiksa:
- Lisensi dan ketentuan penggunaan.
- Bahasa, domain, dan periode.
- Provenance dan cara pengumpulan.
- Kesesuaian label.
- Duplikasi dan kontaminasi.
- Kualitas serta keterwakilan.
- Batas redistribusi dan penggunaan komersial jika relevan.

## 7. Data terkontrol

Data manusia memerlukan consent dan provenance yang jelas. Data AI perlu menyimpan informasi generator/provider, model jika tersedia, prompt, waktu, dan transformasi yang relevan. Data campuran memerlukan catatan kontribusi manusia dan AI.

Detail protokol pengumpulan, kompensasi, consent, anonimisasi, dan retensi belum final.

## 8. Rencana evaluasi model

Metrik kandidat yang pernah dibahas:
- Macro F1.
- Precision/recall per kelas.
- HUMAN false positive rate.
- PR-AUC jika sesuai.
- Confusion matrix.
- Calibration.
- Latency, throughput, dan peak RAM.

Eksperimen kandidat:
- Majority baseline.
- TF-IDF + Logistic Regression/SVM.
- IndoBERT-Lite.
- IndoBERT Base.
- Sentence-only versus context-aware.
- ONNX INT8 versus FP32.

Semua model dan eksperimen tersebut masih kandidat. Tidak ada model final yang disahkan oleh dokumen ini.

## 9. Gerbang keputusan

Tidak boleh berpindah ke pilot nyata sebelum uji prosedur sintetis dan blueprint memadai. Tidak boleh memulai training serius sebelum sumber data diaudit, label dapat dipertanggungjawabkan, group split tervalidasi, dan protokol evaluasi terdokumentasi.

## 10. Hal yang belum diputuskan

- Schema final dan data dictionary.
- Definisi operasional tiap label dan panduan anotasi.
- Proporsi kelas dan domain.
- Daftar sumber publik yang disetujui.
- Protokol consent dan pengumpulan data terkontrol.
- Rasio split final dan challenge set.
- Model final, hyperparameter, dan lingkungan training.

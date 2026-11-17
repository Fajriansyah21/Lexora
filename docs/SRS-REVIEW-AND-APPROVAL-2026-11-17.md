# SRS Review and Approval Record

- **Tanggal review:** 2026-11-17
- **Reviewer:** Delegated Project Lead
- **Mandat:** Pemilik proyek secara eksplisit mendelegasikan penyelesaian tahap 1–6 secara mandiri tanpa persetujuan per langkah pada 2026-11-17.
- **Hasil:** **Approved for System Design**
- **Batas persetujuan:** Persetujuan ini mengesahkan SRS sebagai dasar tahap System Design dan UI/UX. Ini bukan persetujuan implementasi, pilot data nyata, training model, produksi, atau klaim kepatuhan hukum.

## 1. Cakupan review

Review mencakup:
- System Requirements Analysis.
- Decision Log.
- AI Humanizer Plan dan AI Text Detector Plan.
- Product Overview dan Requirements Elicitation Status.
- Active Roadmap.
- Acceptance Criteria dan Acceptance Test Scenarios.
- Audit report Humanizer, Detector, dan supporting modules.

## 2. Hasil pemeriksaan integritas

| Pemeriksaan | Hasil |
|---|---:|
| Requirement fungsional/nonfungsional | 276 ID unik |
| Requirement fungsional | 252 |
| Requirement nonfungsional | 13 |
| Requirement aktif dengan acceptance criteria | 275 |
| Requirement superseded yang dikecualikan dari AC aktif | 1 (FR-HUM-14, digabung ke FR-HUM-70) |
| Decision Log | 176 ID berurutan, DEC-001 sampai DEC-167 |
| Keputusan Accepted | 165 |
| Keputusan Superseded | 2 |
| Referensi requirement dari Decision Log yang diperiksa | 31, tidak ada yang hilang |
| Skenario Gherkin rinci | 53 |
| Tautan internal pada 14 dokumen utama yang diperiksa | Tidak ada tautan rusak |
| ID requirement duplikat | 0 |
| ID keputusan hilang/duplikat | 0 |

## 3. Review substansi

### Konsistensi requirement
- Batas input Detector dan Humanizer dibedakan dengan jelas.
- Penghitungan karakter menggunakan satu konvensi Unicode yang konsisten.
- Guest, pengguna terdaftar, dan Admin memiliki batas hak akses yang terpisah.
- Saldo kredit, reservasi, settlement, refund, dan pembayaran memiliki alur yang dapat ditelusuri.
- Penghapusan profil, sampel, riwayat, dan akun dibedakan berdasarkan jenis data serta status proses.
- Hasil Detector tidak diposisikan sebagai bukti pasti kepengarangan.
- Status MIXED dan UNCERTAIN tidak disamakan.
- Akses Admin ke teks pengguna dibatasi oleh consent, ticket scope, waktu, dan audit.
- Retry, idempotency, dan cancellation memiliki aturan lintas modul.

### Keterlacakan
- Requirement normatif berada di SRS.
- Keputusan dan alasan berada di Decision Log.
- Feature Plans tidak menggantikan SRS.
- Audit report menjelaskan perubahan dan gap.
- Acceptance Criteria memetakan seluruh requirement aktif.
- Gherkin scenarios memprioritaskan alur berisiko tinggi.

### Kesiapan
SRS cukup matang untuk menjadi input System Design. Detail yang belum diputuskan tidak disamarkan sebagai keputusan. Setiap area terbuka memiliki tempat di bagian 8 SRS atau Feature Plan dan harus diselesaikan pada tahap desain/validasi yang sesuai.

## 4. Hal yang masih menjadi prasyarat sebelum implementasi/produksi

1. Pemilihan provider/model AI dan pengukuran biaya.
2. Payment gateway dan verifikasi dukungan metode pembayaran.
3. Validasi kebijakan produk rewarded ads.
4. Unit economics, harga paket, tarif fitur, dan nilai reward.
5. Validasi hukum/kontrak untuk consent, retensi, backup, dan pemrosesan provider.
6. Penetapan ukuran file, OCR, strategi chunking, token limits, dan kapasitas.
7. Target performa, availability, RPO/RTO, dan concurrency setelah infrastruktur dipilih.
8. Benchmark Detector/Humanizer, kalibrasi, false-positive target, dan kualitas hasil.
9. Uji keamanan, aksesibilitas, dan acceptance test pada implementasi.

Hal-hal tersebut tidak menghalangi System Design, tetapi menghalangi klaim bahwa produk siap dibangun/dirilis tanpa keputusan dan bukti tambahan.

## 5. Keputusan review

**SRS disahkan sebagai baseline untuk tahap 6: User Flow, System Design, evaluasi teknologi, dan UI/UX.**

SRS tidak boleh diubah secara diam-diam. Setiap perubahan requirement harus memperbarui ID/teks terkait, Decision Log jika mengubah keputusan, Acceptance Criteria, Feature Plan, dan status roadmap.

Tahap 7 (pembangunan website) tetap di luar mandat saat ini.


## 6. Addendum privasi dan regulasi (2026-11-17)

SRS diperluas dengan FR-ACC-20/21 dan NFR-SEC-06 serta NFR-PRIV-03 sampai NFR-PRIV-09. DEC-168 sampai DEC-174 menetapkan no-training-by-default, consent terpisah, kontrol transfer lintas negara, incident response, data-subject request, self-assessment perlindungan anak, dan DPIA jika diwajibkan. Lihat [Privacy and Legal Readiness](PRIVACY-AND-LEGAL-READINESS.md). Persetujuan SRS tetap hanya untuk System Design; peluncuran tetap diblokir sampai checklist legal/privacy dipenuhi.


### Addendum rewarded ads

DEC-175 dan DEC-176 menetapkan Google Ad Manager Rewarded Web sebagai kandidat bersyarat dan membatasi rewarded-ad credit MVP untuk akun login. Guest hanya dapat menggunakan trial credit non-iklan yang dikonfigurasi dan terikat sesi. SRS FR-CRED-03/04/21/25 telah diperbarui. Rewarded ads tetap feature-flagged sampai policy, eligibility, SSV, dan merchant/provider review selesai.

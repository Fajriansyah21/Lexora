# Task Plan: Database Foundation (M2.3)

- **Tanggal:** 2026-11-19
- **Status:** Planning Draft
- **Milestone:** Stage 7, M2.3
- **Parent task:** [Database and Backend Foundation](2026-11-19-database-backend-foundation.md)
- **Architecture:** Modular Monolith, Option A

## 1. Objective

Membangun infrastruktur database PostgreSQL dan Drizzle ORM di dalam `apps/web` sebagai fondasi backend Lexora.

## 2. Architecture

- PostgreSQL 18 sebagai database utama.
- Drizzle ORM sebagai ORM.
- Drizzle Kit sebagai migration tooling.
- `node-postgres` (`pg`) sebagai driver.
- Koneksi database terpusat dan menggunakan connection pool.
- Database infrastructure berada di dalam `apps/web`.
- Tetap menggunakan arsitektur modular monolith Opsi A: Next.js menjadi frontend dan BFF, dengan batas modul jelas; bukan microservice baru.

## 3. Keputusan schema dan migration

- M2.3 tidak membuat tabel autentikasi secara manual.
- Schema autentikasi dibuat dari konfigurasi Better Auth dalam M2.4 agar tidak menduplikasi atau bertentangan dengan schema resmi Better Auth.
- M2.3 menyiapkan konfigurasi Drizzle Kit dan membuktikan konfigurasi/tooling serta koneksi database.
- Migration aplikasi pertama yang berisi tabel autentikasi adalah pekerjaan M2.4.
- Jangan membuat tabel sementara atau migration kosong hanya untuk memenuhi checklist.
- Jika Drizzle Kit memerlukan target schema untuk konfigurasi, siapkan lokasi/schema path tanpa membuat tabel atau migration aplikasi. Verifikasi dukungan tooling secara eksplisit; jangan menghasilkan artefak migration kosong.

## 4. Database target

- Database: `lexora_dev`.
- Application role: `lexora_app`.
- Host: `127.0.0.1`.
- Port: `5432`.
- PostgreSQL: versi 18.
- Aplikasi dan tooling runtime memakai role `lexora_app`, bukan superuser `postgres`.
- Password hanya disediakan operator secara lokal melalui environment; jangan tulis nilai credential di dokumen, source code, command yang terekam, log, atau Git.
- Jangan mengasumsikan database/server/role sudah tersedia. Audit dan laporkan prasyarat sebelum koneksi; jangan membuat role/database tanpa otorisasi terpisah.

## 5. Scope

### In Scope

1. Audit konfigurasi dan struktur proyek.
2. Instalasi dependency Drizzle ORM, Drizzle Kit, PostgreSQL driver, dan tipe yang diperlukan.
3. Konfigurasi Drizzle Kit.
4. Implementasi database client dan connection pool terpusat.
5. Konfigurasi environment variable `DATABASE_URL`.
6. Penyediaan `.env.example` tanpa credential asli.
7. Perlindungan file environment lokal melalui `.gitignore`.
8. Struktur direktori database modular di dalam `apps/web`.
9. Script CLI untuk generate, migrate, dan pengecekan schema yang sesuai konfigurasi Drizzle Kit.
10. Pengujian koneksi ke database `lexora_dev` menggunakan role `lexora_app`.
11. Dokumentasi setup database lokal.

### Out of Scope

- Better Auth.
- Login dan registrasi.
- Session dan account tables.
- Tabel credits dan payment.
- AI Detector dan Humanizer.
- Redis dan BullMQ.
- API bisnis.
- Production deployment.
- Tabel/domain schema produk, migration autentikasi, atau migration kosong.

## 6. Rencana implementasi

1. Audit status branch, working tree, `apps/web`, workspace manifests, TypeScript, lint, scripts, environment ignore rules, dan package manager. Pertahankan perubahan lokal dan tujuh file desain pengguna.
2. Periksa versi stabil dan peer/engine requirements untuk Drizzle ORM, Drizzle Kit, `pg`, dan `@types/pg`; pilih versi yang saling kompatibel dan kompatibel dengan Node.js 26 serta TypeScript proyek. Jangan mengubah dependency root tanpa kebutuhan.
3. Tambahkan dependency hanya di `apps/web`, perbarui lockfile melalui pnpm, dan tinjau diff lockfile.
4. Rancang struktur `apps/web` yang memisahkan database client, konfigurasi, schema location, dan migration output tanpa menambahkan model/tabel aplikasi.
5. Konfigurasikan `DATABASE_URL` melalui environment, `.env.example` berisi format placeholder yang aman, serta `.gitignore` agar `.env` dan file credential lokal tetap terabaikan.
6. Implementasikan pool `pg` dan Drizzle client terpusat dengan lifecycle yang sesuai Next.js development/HMR, tanpa membuat koneksi berulang pada setiap import atau request.
7. Tambahkan Drizzle Kit config serta script generate, migrate, dan schema/tooling check. Pastikan tahap ini tidak menghasilkan tabel atau migration kosong.
8. Dokumentasikan prasyarat PostgreSQL 18, pembuatan database/role oleh operator berizin, pengisian URL lokal secara aman, menjalankan app/tool CLI, serta troubleshooting environment variable.
9. Verifikasi dahulu keberadaan PostgreSQL 18, `lexora_dev`, dan role `lexora_app` tanpa menampilkan password. Jika prasyarat tidak ada, laporkan blocker; jangan otomatis membuat/mengubah database atau role.
10. Bila service tersedia dan pengguna memberi izin menjalankan operasi DB, uji koneksi/identitas database dan hak minimum sebagai `lexora_app`; jangan melakukan migration dalam M2.3. Catat hasil aktual, jangan menyamarkan tes yang blocked.
11. Jalankan frozen install, lint, test, build, format check, dan diff/status review. Pastikan source code dan dokumentasi tidak mengekspos credential.

## 7. Acceptance Criteria

- [ ] Drizzle ORM, Drizzle Kit, `pg`, dan tipe yang diperlukan terintegrasi pada workspace `apps/web` dengan versi stabil dan peer/engine-compatible.
- [ ] Aplikasi memiliki database client terpusat dan PostgreSQL connection pool dengan lifecycle development/HMR yang tidak membuat pool berulang.
- [ ] Aplikasi dapat membuat koneksi PostgreSQL menggunakan `DATABASE_URL`.
- [ ] Koneksi target memakai role `lexora_app`, bukan `postgres`.
- [ ] Drizzle Kit dapat memuat konfigurasi dan memeriksa lokasi schema yang disiapkan.
- [ ] Migration tooling siap digunakan; M2.3 tidak membuat tabel autentikasi, tabel sementara, atau migration kosong.
- [ ] `DATABASE_URL` dibaca dari environment dan tidak memiliki fallback credential tertanam.
- [ ] `.env.example` tidak memuat credential nyata; environment lokal diabaikan Git.
- [ ] Script CLI generate, migrate, dan schema/tooling check berfungsi tanpa menjalankan migration selama verifikasi M2.3.
- [ ] Pengujian koneksi ke `lexora_dev` sebagai `lexora_app` berhasil, atau blocker prasyarat dicatat secara eksplisit sebagai belum terverifikasi.
- [ ] Dokumentasi setup database lokal tersedia dan tidak mencantumkan password.
- [ ] TypeScript, lint, test, build, dan format check lulus.
- [ ] `git diff --check` bersih untuk perubahan task ini dan perubahan lokal yang tidak terkait tetap utuh.

## 8. Risiko dan mitigasi

| Risiko | Mitigasi |
|---|---|
| Pool connection berlebihan pada Next.js development/HMR | Gunakan satu pool bersama pada module scope dan pola global singleton khusus development bila perlu; uji reload berulang dan tutup pool pada proses/test lifecycle yang tepat. Jangan membuat pool per request. |
| `DATABASE_URL` tidak terbaca saat CLI dijalankan | Dokumentasikan sumber environment yang eksplisit dan urutan pemuatan untuk Next.js serta Drizzle Kit; tambah validasi yang gagal jelas tanpa mencetak nilai URL/secret. Uji command dari root workspace dan konteks package yang ditetapkan. |
| Credential bocor ke Git | `.env` dan variasinya tetap di-ignore; `.env.example` hanya placeholder; redaksi URL dari log/error; review `git status` dan diff sebelum selesai. |
| Konflik schema Drizzle dengan Better Auth | Jangan membuat tabel auth manual pada M2.3. Generate schema autentikasi dari konfigurasi Better Auth pada M2.4 dan jadikan migration auth pertama pekerjaan M2.4. |
| Ketidakcocokan versi dependency | Audit metadata versi stabil, peerDependencies, engines, dan integrasi Node 26/TypeScript sebelum install; pin versi yang dipilih dan verifikasi frozen lockfile serta build. |

## 9. Batas keamanan dan operasional

- Tidak mencetak `DATABASE_URL`, password, atau objek environment ke log.
- Jangan menaruh credential dalam command line yang tersimpan pada shell history, dokumentasi, test fixture, atau output verifikasi.
- Jangan menjalankan DDL/migration atau mengubah database selama pemeriksaan koneksi.
- Akses role/database harus mengikuti least privilege; kebutuhan grant dibuktikan sebelum meminta operator melakukan provisioning.
- Data lokal hanya data sintetis; jangan memakai data pengguna produksi.

## 10. Verifikasi yang direncanakan

Perintah persis akan mengikuti scripts aktual setelah audit implementasi, tanpa menambahkan script palsu. Baseline yang wajib dijalankan:

1. `corepack pnpm install --frozen-lockfile`
2. `corepack pnpm exec turbo run lint --force`
3. `corepack pnpm exec turbo run test --force`
4. `corepack pnpm format:check`
5. `corepack pnpm --filter @lexora/web build`
6. Script Drizzle Kit untuk memeriksa config/schema tanpa generate migration kosong atau menyentuh database.
7. Tes koneksi read-only/identitas sebagai `lexora_app` hanya jika service dan izin tersedia.
8. `git diff --check` dan `git status --short`.

Semua hasil harus dicatat sebagai output aktual. Bila database tidak tersedia, acceptance koneksi berstatus blocked/belum terverifikasi dan tidak boleh diklaim lulus.

## 11. Review gate

M2.3 selesai setelah acceptance criteria dapat ditelusuri ke bukti. Migration autentikasi dan Better Auth berada pada M2.4. Tidak memulai M2.4 sebelum review dan persetujuan eksplisit project owner.

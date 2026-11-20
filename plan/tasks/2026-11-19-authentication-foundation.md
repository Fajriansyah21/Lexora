# Task Plan: Authentication Foundation (M2.4)

- **Tanggal:** 2026-11-19
- **Status:** Planning Draft
- **Milestone:** Stage 7, M2.4
- **Parent task:** [Database and Backend Foundation](2026-11-19-database-foundation.md)
- **Architecture:** Modular Monolith, Option A

## 1. Objective

Implementasi autentikasi Lexora menggunakan **Better Auth** (versi 1.7.26), terintegrasi dengan Drizzle ORM, PostgreSQL 18, dan Next.js App Router, sebagai fondasi keamanan backend untuk modul Detector dan Humanizer.

## 2. Technology Stack

- **Framework:** Better Auth 1.7.26
- **Adapter:** `@better-auth/drizzle-adapter` 1.7.26
- **ORM:** Drizzle ORM (existing)
- **Database:** PostgreSQL 18 (existing)
- **Authentication:** Email & Password

## 3. Audit baseline M2.3

- `apps/web/src/db/client.ts` menyediakan satu Drizzle client berbasis `pg.Pool`, global singleton pada development/HMR, dan module-scoped pool pada production.
- `apps/web/src/db/index.ts` hanya mengekspor `db`, `pool`, dan `closePool`; `DATABASE_URL` tidak menjadi public API.
- `apps/web/src/db/schema.ts` masih kosong secara sengaja.
- `apps/web/drizzle.config.ts` membaca `apps/web/src/db/schema.ts`, output ke `apps/web/src/db/migrations`, dan memuat environment melalui `@next/env`.
- `apps/web/package.json` sudah memiliki `db:generate` dan `db:migrate` berbasis Drizzle Kit.
- `apps/web/.env.example` hanya memuat placeholder `DATABASE_URL`; `.env.local` diabaikan Git.
- Struktur `apps/web/src` saat ini hanya berisi modul database; `apps/web/app` belum memiliki route auth.

Fondasi M2.3 dipertahankan. Tidak membuat koneksi database kedua dan tidak memindahkan pool.

## 4. Versi dan dependency yang direncanakan

- `better-auth`: `1.7.26`.
- `@better-auth/drizzle-adapter`: `1.7.26`.
- `auth`: `1.7.26` (Better Auth CLI binary).
- Existing `drizzle-orm`: `0.45.4`; `drizzle-kit`: `0.31.11`; `pg`: `8.23.1`.
- Existing Next.js `16.4.6`, React `19.3.1`, dan Node.js 26.

Better Auth 1.7.26 mendukung Next.js 14/15/16, React 18/19, `pg ^8.0.0`, `drizzle-kit >=0.31.4`, dan `drizzle-orm ^0.45.2`; versi existing memenuhi peer requirements. Dependency hanya direncanakan untuk `apps/web`; instalasi membutuhkan persetujuan terpisah.

## 5. Better Auth configuration

- Config server: `apps/web/src/lib/auth.ts`.
- Client: `apps/web/src/lib/auth-client.ts`, tanpa secret.
- Adapter memakai `drizzleAdapter(db, { provider: 'pg', schema })`; `db` berasal dari M2.3, tanpa pool kedua.
- `schema` di-import dari `apps/web/src/db/schema.ts` setelah Better Auth schema digenerate dan diekspor.
- `emailAndPassword.enabled: true`.
- `BETTER_AUTH_SECRET` dan `BETTER_AUTH_URL` wajib dari server environment, tanpa fallback credential.
- `trustedOrigins` hanya berisi origin development dan production yang disetujui; origin request arbitrer ditolak.
- Cookie menggunakan `SameSite=Lax` dan `HttpOnly=true`; `Secure=true` pada production HTTPS, sedangkan development HTTP lokal memakai `Secure=false` agar cookie berfungsi.
- CSRF dan origin validation tetap aktif.

Rencana tidak mencakup OAuth, passkey, 2FA, password reset, atau email verification provider.

## 6. Reproducible schema generation

CLI dipin `auth@1.7.26`. Dari `apps/web`, command resmi yang direncanakan:

```bash
corepack pnpm --filter @lexora/web exec auth generate --config src/lib/auth.ts --output src/db/auth-schema.ts --adapter drizzle --dialect postgresql --yes
```

Binary `auth` berasal dari package `auth@1.7.26` yang terpasang lokal; tidak memakai `auth@latest`, `pnpm dlx`, atau command unpinned. `--adapter drizzle`, `--dialect postgresql`, `--config`, `--output`, dan `--yes` wajib eksplisit. Command tidak dijalankan pada tahap planning.

Output canonical `apps/web/src/db/auth-schema.ts` adalah generated file. Jangan menulis ulang tabel auth manual; perubahan config diikuti regenerate dan review diff.

## 7. Drizzle schema integration

`apps/web/src/db/schema.ts` menjadi entry point utama setelah generation:

```ts
export * from './auth-schema';
```

`drizzle.config.ts` tetap memakai `schema: './src/db/schema.ts'`; Drizzle Kit mengikuti export `auth-schema.ts` dan mendeteksi seluruh tabel, kolom, relasi, index, dan constraint. Output tetap `./src/db/migrations`.

Database client tetap `drizzle(pool)` dari M2.3 dan tidak perlu menerima objek schema untuk query dasar. Namun, adapter Better Auth harus menerima objek schema secara eksplisit agar dapat mengenali tabel auth. Rencana implementasi:

1. `src/db/schema.ts` mengekspor seluruh schema setelah generate:

   ```ts
   export * from './auth-schema';
   ```

2. `src/lib/auth.ts` meng-import schema dari `src/db/schema.ts` dan meneruskannya ke adapter:

   ```ts
   import * as schema from '@/db/schema';
   import { db } from '@/db/client';

   export const auth = betterAuth({
     database: drizzleAdapter(db, { provider: 'pg', schema }),
     // ...
   });
   ```

3. `src/db/schema.ts` tidak boleh meng-import dari `src/lib/auth.ts` agar tidak terjadi circular dependency.

4. `src/db/client.ts` tetap memakai `drizzle(pool)` tanpa schema; pool M2.3 tidak diubah.

## 8. Migration workflow

1. **Schema generation:** Better Auth CLI menghasilkan `auth-schema.ts`; tidak menyentuh database.
2. **Migration generation:** `corepack pnpm --filter @lexora/web db:generate` membaca `schema.ts` dan menghasilkan SQL/snapshot di `src/db/migrations`; tidak menerapkan SQL.
3. **Migration execution:** `corepack pnpm --filter @lexora/web db:migrate` menerapkan SQL ke database; ini satu-satunya langkah yang mengubah database.

Sebelum execution, review generated schema, SQL, snapshot/journal, tabel, tipe, relasi, constraint, index, dan diff tak terduga. Jangan membuat migration kosong. Tidak ada command generation atau migration dijalankan selama planning.

## 9. Authentication API dan client

- Route: `apps/web/app/api/auth/[...all]/route.ts`.
- Handler resmi: `toNextJsHandler(auth)` dengan `GET` dan `POST`.
- Client memakai `createAuthClient` untuk `signUp.email`, `signIn.email`, `signOut`, dan `getSession`/`useSession`.
- UI final login/registrasi bukan scope M2.4.

## 10. Session management dan protected API

Server memvalidasi session dengan `auth.api.getSession({ headers: await headers() })` dari `next/headers`. Session tidak ada, invalid, atau expired diperlakukan unauthenticated.

Buat `apps/web/app/api/protected/example/route.ts`:

```ts
const session = await auth.api.getSession({ headers: await headers() });
if (!session) return Response.json({ error: 'Unauthorized' }, { status: 401 });
return Response.json({ ok: true, userId: session.user.id });
```

Tanpa middleware/proxy global hanya untuk acceptance criteria ini. Request tanpa session wajib HTTP 401; session valid wajib response sukses. Client-only check bukan authorization.

## 11. Authorization Baseline M2.4

M2.4 membedakan autentikasi dari otorisasi:

- Autentikasi menjawab apakah request memiliki session valid dan menghasilkan `currentUserId`.
- Otorisasi kepemilikan menjawab apakah `currentUserId` boleh mengakses resource tertentu.

Buat helper ownership sederhana di modul domain-neutral, tanpa ketergantungan pada Next.js route handler, `next/headers`, database, atau Better Auth. Kontrak helper menerima `currentUserId` dan `resourceOwnerId`:

- Keduanya harus berupa ID string non-kosong setelah `trim`.
- Helper mengizinkan akses hanya jika kedua ID valid dan sama persis.
- Helper menolak akses jika ID berbeda, kosong, whitespace-only, `null`, atau `undefined`.
- Domain service memakai helper ini setelah memperoleh `currentUserId` dari session server-side.

Unit test wajib:

1. User A mengakses resource miliknya sendiri: diizinkan.
2. User A mengakses resource User B: ditolak.
3. `currentUserId` atau `resourceOwnerId` kosong atau invalid: ditolak.

Jangan membuat tabel, fixture database, atau resource domain baru hanya untuk helper ini. Jangan membuat RBAC, role management, permission framework, atau middleware global.

Pembagian milestone:

- M2.4: fondasi autentikasi, validasi session, dan helper ownership authorization.
- Milestone domain pertama: penerapan helper pada resource nyata dan test user A terhadap resource user B.
- RBAC dan permission kompleks: di luar scope M2.4.

## 12. Rate limiting dan IP address

### 12.1 Konfigurasi rate limit

Aktifkan eksplisit agar dapat diuji di development:

- `rateLimit.enabled: true`.
- `'/sign-in/email': { window: 10, max: 3 }`.
- `'/sign-up/email': { window: 60, max: 5 }`.
- Uji HTTP 429 dan retry header (`X-Retry-After`).

Gunakan memory storage tanpa Redis. Storage ini per-process, hilang saat restart, dan tidak konsisten antar instance; baseline ini bukan proteksi multi-instance production. Shared storage ditunda ke keputusan tahap berikutnya. `auth.api` server calls tidak otomatis terkena HTTP limiter.

### 12.2 Resolve client IP

Rate limiter menghitung request per client IP. Default Better Auth membaca `X-Forwarded-For`, dan client dapat mengirim header itu sendiri. Konfigurasi `advanced.ipAddress` harus mengikuti cara request mencapai server. Opsi yang tersedia pada Better Auth 1.7.26: `ipAddressHeaders`, `trustedProxies`, dan `disableIpTracking`.

#### Development lokal (koneksi langsung, tanpa proxy)

Gunakan `ipAddressHeaders: []`. Ini adalah opsi resmi Better Auth 1.7.26 untuk deployment dengan koneksi langsung ke server. Better Auth tidak membaca IP address dari header mana pun, sehingga `X-Forwarded-For` yang dikirim client diabaikan sepenuhnya.

Konsekuensi yang harus diterima secara eksplisit:

- Semua client lokal berbagi satu counter per path. Untuk pengembangan single-developer ini diterima, dan memang lebih baik daripada mempercayai header yang bisa dipalsukan client.
- Bila pemisahan per-client dibutuhkan di development, alternatif resmi adalah menulis connection address ke header sendiri di server code dan mendaftarkan header tersebut di `ipAddressHeaders`. Header itu wajib selalu ditimpa server dan tidak boleh berasal dari client. M2.4 memakai `ipAddressHeaders: []`; opsi header server-side dicatat sebagai material untuk tahap berikutnya.

Production tidak boleh memakai `ipAddressHeaders: []` jika traffic datang dari banyak client karena akan menggabungkan seluruh traffic ke satu counter.

#### Production di belakang reverse proxy

Production hanya boleh mempercayai header yang ditetapkan atau ditimpa oleh proxy tepercaya. Dua pola resmi:

1. **Proxy menambahkan alamat ke `X-Forwarded-For`**: daftarkan alamat proxy spesifik pada `trustedProxies`. Better Auth membaca rantai forwarded dari kanan ke kiri, melewati alamat proxy terdaftar, dan memakai alamat pertama selain proxy sebagai client IP. Gunakan alamat IP atau CIDR spesifik milik proxy, bukan rentang luas, dan jangan pernah memasukkan address client ke daftar tersebut.

   ```ts
   advanced: {
     ipAddress: {
       trustedProxies: ['<ALAMAT_PROXY_SPECIFIK>'],
     },
   }
   ```

2. **Proxy menulis IP client ke header sendiri**: daftarkan hanya header tersebut pada `ipAddressHeaders`, misalnya header platform yang selalu menimpa nilai dari client. Header yang hanya diisi proxy ketika belum ada nilainya tidak aman karena meneruskan nilai client.

Syarat wajib untuk kedua pola:

- Client hanya boleh menjangkau server melalui proxy. Bila server dapat diakses langsung, IP client dapat dipalsukan dan limiter dilewati.
- Daftar `ipAddressHeaders` dan `trustedProxies` diisi dari konfigurasi environment yang dikendalikan operator, bukan daftar hardcoded bebas.
- `disableIpTracking: true` tidak boleh dipakai untuk menyelesaikan masalah ini karena opsi tersebut mematikan rate limiter HTTP secara keseluruhan.
- Konfigurasi final production dikirim operator bersama deployment dan direview pada security review M7.

### 12.3 Perbedaan konfigurasi development dan production

| Aspek | Development lokal | Production di belakang reverse proxy |
|---|---|---|
| Jalur koneksi | Client langsung ke Next.js dev server | Client melalui reverse proxy tepercaya |
| `ipAddressHeaders` | `[]`, tidak membaca header IP dari request | Header yang selalu ditimpa proxy, jika pola header sendiri dipakai |
| `trustedProxies` | Tidak digunakan | Alamat IP atau CIDR proxy spesifik, hanya jika proxy append ke `X-Forwarded-For` |
| Identitas client IP | Tidak diambil dari header; fallback `127.0.0.1` pada development/test | Diturunkan dari rantai forwarded yang sudah diverifikasi proxy |
| Dampak rate limit | Counter bersama per path; cukup untuk single-developer | Counter per client nyata, dengan syarat proxy wajib dikunci |
| Risiko utama | Spoofing header dan counter tidak terpisah | Header yang salah daftarkan membuat client bisa memilih IP sendiri |

Konfigurasi dipilih per environment dan tidak boleh hardcode nilai production di source.

## 13. Security baseline

- `BETTER_AUTH_SECRET` kuat, server-only, tidak masuk client bundle.
- `DATABASE_URL` server-only dan tidak diekspor dari `apps/web/src/db/index.ts`.
- Tidak memakai `NEXT_PUBLIC_` untuk secret.
- `trustedOrigins`, CSRF, dan origin validation aktif.
- Validasi format `trustedOrigins` (origin URL valid) dan `trustedProxies` (IP/CIDR valid) dibuatkan helper validator tersendiri dengan unit test dedicated.
- Cookie `HttpOnly`, `SameSite=Lax`, dan `Secure` production HTTPS.
- Error tidak memuat secret, password, connection string, session token, atau detail internal.
- Default password hashing Better Auth dipertahankan.
- Security integration test yang membutuhkan database (login, logout, session persistence, cookie response HTTP, rate limit HTTP endpoint) tetap menunggu persetujuan dan eksekusi migrasi.
- Tidak menambah Redis, BullMQ, OAuth, passkey, 2FA, RBAC kompleks, email provider, password reset, atau email verification provider.

## 14. Acceptance Criteria

- [ ] `better-auth`, `@better-auth/drizzle-adapter`, dan `auth` versi `1.7.26` terpasang hanya setelah approval.
- [ ] Better Auth config memakai Drizzle `db` M2.3, provider PostgreSQL `pg`, dan objek schema eksplisit tanpa pool kedua.
- [ ] `BETTER_AUTH_SECRET` dan `BETTER_AUTH_URL` tervalidasi dari environment server.
- [ ] CLI generation reproducible, pinned `1.7.26`, memakai `--adapter drizzle` dan `--dialect postgresql`.
- [ ] `src/db/auth-schema.ts` dihasilkan CLI dan tidak ditulis ulang manual.
- [ ] `src/db/schema.ts` mengekspor `auth-schema.ts`; Drizzle Kit mendeteksi seluruh tabel auth.
- [ ] Generated schema direview untuk tabel, kolom, tipe, relasi, index, dan constraint.
- [ ] Migration generation menghasilkan SQL auth yang dapat direview tanpa database change.
- [ ] Setelah approval terpisah, migration auth berhasil diterapkan pada local/dev database.
- [ ] Registrasi, login, dan logout email/password berfungsi.
- [ ] Server memverifikasi session valid melalui `auth.api.getSession({ headers: await headers() })`.
- [ ] Session tidak ada, invalid, atau expired ditolak.
- [ ] Protected API HTTP 401 tanpa session dan sukses dengan session valid.
- [ ] Cookie memenuhi HttpOnly, SameSite Lax, dan Secure production HTTPS.
- [ ] CSRF dan origin validation tetap aktif.
- [ ] Rate limiting aktif di development dan custom sign-in/sign-up rules dapat diuji.
- [ ] Error response tidak membocorkan secret atau credential.
- [ ] Helper ownership authorization (M2.4 baseline) tersedia dengan unit test ketiga skenario.
- [ ] Validator format `trustedOrigins` dan `trustedProxies` tersedia dengan unit test.
- [ ] Lint, test, format, dan build tetap lulus.

## 15. Verification Plan

### Schema dan migration

1. Pastikan binary `auth@1.7.26`.
2. Jalankan schema generation hanya setelah approval; catat exit code dan output path.
3. Review `src/db/auth-schema.ts` untuk seluruh tabel, kolom, tipe, relasi, index, dan constraint.
4. Pastikan `src/db/schema.ts` mengekspor generated schema.
5. Pastikan Drizzle Kit membaca seluruh tabel auth dari entry point tersebut.
6. Jalankan migration generation hanya setelah schema review; periksa SQL, snapshot, journal, dan diff tak terduga.
7. Bedakan hasil: schema generation hanya membuat file schema; migration generation hanya membuat SQL; migration execution mengubah database.
8. Jalankan migration execution hanya setelah persetujuan eksplisit, lalu verifikasi tabel dengan SQL read-only atau Drizzle Studio.

### Authentication behavior

1. Environment validation: secret/URL hilang atau invalid dan origin tidak dipercaya.
2. Registrasi valid, input invalid, dan password terlalu pendek.
3. Login valid dan credential salah tanpa detail sensitif.
4. Session valid melalui client dan server `auth.api.getSession` dengan `await headers()`.
5. Session invalid atau expired ditolak.
6. Logout mengakhiri session.
7. Protected API tanpa cookie/session mengembalikan HTTP 401.
8. Protected API dengan session invalid mengembalikan HTTP 401.
9. Protected API dengan session valid mengembalikan response sukses.
10. Cookie response memiliki HttpOnly, SameSite=Lax, dan Secure sesuai environment.
11. CSRF/origin-invalid request ditolak tanpa bypass.
12. Rate limit sign-in/sign-up menghasilkan HTTP 429 dan retry header.
13. Test IP spoofing mengirim `X-Forwarded-For` palsu pada development; hasilnya harus memakai counter yang sama seperti request tanpa header, membuktikan header client tidak mengubah identitas IP.
14. Test production proxy mengirim forwarded chain dengan proxy tepercaya dan alamat proxy tak terdaftar; hanya chain yang sesuai `trustedProxies` boleh memengaruhi identitas client IP.
15. Secret, password, database URL, dan token tidak muncul di response, log, atau client bundle.

### Authorization baseline

1. Unit test helper ownership: akses resource sendiri diizinkan.
2. Unit test helper ownership: akses resource milik user lain ditolak.
3. Unit test helper ownership: `currentUserId` atau `resourceOwnerId` kosong/whitespace/invalid ditolak.
4. Helper tidak mengimport modul Next.js, `next/headers`, Better Auth, atau database.
5. Verifikasi tidak ada tabel atau resource domain baru yang dibuat hanya untuk pengujian helper.

### Environment validators

1. Unit test validator `trustedOrigins`: origin URL valid diterima; nilai kosong, bukan URL, atau tanpa skema ditolak.
2. Unit test validator `trustedProxies`: IP dan CIDR valid diterima; nilai kosong atau format tidak dikenal ditolak.
3. Konfigurasi produksi tetap menolak nilai kosong untuk kedua variabel.

### Pemisahan status pengujian

Setiap laporan verifikasi wajib memisahkan hasil menjadi tiga kategori dan tidak boleh mencampurnya:

1. **Berhasil**: bukti eksekusi nyata dengan output.
2. **Gagal**: eksekusi nyata yang gagal beserta error.
3. **Blocked**: pengujian yang membutuhkan tabel Better Auth (`user`, `session`, `account`, `verification`) di database dan belum dapat dijalankan karena migrasi belum dieksekusi. Termasuk: registrasi, login, logout, session persistence, protected API dengan session nyata, cookie response HTTP, rate limit HTTP endpoint, CSRF/origin rejection terhadap auth route nyata, dan spoofed `X-Forwarded-For` terhadap server berjalan.

Mock atau pemeriksaan konfigurasi tidak dapat menggantikan kategori Blocked.

### Project gates

- `corepack pnpm install --frozen-lockfile`.
- `corepack pnpm exec turbo run lint --force`.
- `corepack pnpm exec turbo run test --force`.
- `corepack pnpm format:check`.
- `corepack pnpm --filter @lexora/web build`.
- `git diff --check` untuk file task dan `git status --short`.

Tidak boleh mengklaim acceptance criterion lulus tanpa output test atau bukti file/database yang dapat diperiksa.

## 16. Risiko dan keputusan tertunda

| Risiko/keputusan | Mitigasi atau tindak lanjut |
|---|---|
| CLI schema berubah saat config berubah | Pin CLI 1.7.26, regenerate dari config aktual, review diff |
| Generated schema tertimpa manual | Perlakukan `auth-schema.ts` sebagai generated-only dan ekspor melalui `schema.ts` |
| Pool kedua atau adapter memakai koneksi berbeda | Import `db` M2.3; audit import dan connection count |
| Memory rate limit tidak konsisten multi-instance | Single-instance baseline; shared storage ditunda, Redis tidak dipasang |
| Forwarded IP spoofing | Development memakai `ipAddressHeaders: []`; production memakai header yang selalu ditimpa proxy atau `trustedProxies` berisi alamat spesifik, lalu diuji dengan header palsu |
| Cookie gagal pada local HTTP | Secure mengikuti environment; production wajib HTTPS |
| Migration berisi perubahan tak diharapkan | Review SQL/snapshot sebelum execution; stop jika diff tidak sesuai |
| Auth error membocorkan detail | Sanitasi response dan uji log/client bundle |
| Authorization helper tidak reusable | Helper ownership harus murni, tanpa dependensi Next.js/Better Auth/database |
| Trusted origins/proxies format invalid | Sediakan dedicated validator dan unit test; tetap tolak nilai kosong di runtime |

## 17. Non-scope

- Google OAuth, GitHub OAuth, passkey, 2FA, dan complex RBAC.
- Password reset email atau email verification provider.
- AI, payment, credits, Redis, BullMQ.
- UI final login dan registrasi.
- Global middleware/proxy auth guard hanya untuk acceptance criteria M2.4.
- Production multi-instance rate-limit storage.
- Resource domain dan tabel nyata untuk pengujian helper ownership.

## 18. Batasan operasional planning

Task ini hanya revisi perencanaan:

- Tidak mengimplementasikan kode.
- Tidak menginstal paket atau mengubah `package.json`/lockfile.
- Tidak membuat auth config, auth client, route handler, atau migration.
- Tidak menjalankan Better Auth CLI generate, Drizzle migration generation, atau migration execution.
- Tidak membuat atau mengubah tabel/database/role.
- Tidak mengubah tujuh file desain.
- Tidak commit atau push.

## 19. Sumber resmi

- Better Auth installation: https://better-auth.com/docs/installation
- Better Auth Drizzle adapter: https://better-auth.com/docs/adapters/drizzle
- Better Auth CLI: https://better-auth.com/docs/concepts/cli
- Better Auth Next.js integration: https://better-auth.com/docs/integrations/next
- Email/password: https://better-auth.com/docs/authentication/email-password
- Session management: https://better-auth.com/docs/concepts/session-management
- Security: https://better-auth.com/docs/reference/security
- Rate limiting: https://better-auth.com/docs/concepts/rate-limit

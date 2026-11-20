# Task Plan: M2.6 API Foundation

- **Tanggal:** 2026-11-20
- **Status:** Proposed
- **Milestone:** Stage 7, M2 (Backend Foundation)
- **Architecture:** Modular Monolith

## 1. Objective dan Background
Membangun fondasi API generik `/api/v1` untuk Lexora yang mendukung kontrak standar, validasi ketat, dan pemisahan boundary autentikasi/otorisasi sebagai Backend-for-Frontend (BFF). Milestone ini merupakan kelanjutan dari M2.5 (Authentication Foundation).

## 2. Architecture Decisions
- **Shared Contracts:** Inisialisasi `packages/contracts` sebagai package bersama untuk Zod schemas, tipe kontrak API, dan constant error codes.
- **Domain Layer:** `packages/domain` ditunda (Deferred). Logika tetap di modular monolith `apps/web/src`.
- **Validation Policy:** Zod `strict()` untuk semua endpoint guna menolak unknown request fields (HTTP 422).
- **API Utilities:** Terpusat di `apps/web/src/lib/api/`.
- **Timestamp:** ISO 8601 UTC.
- **Tests:** Colocated (berdampingan) dengan modul sumber.

## 3. Scope
### In Scope
- Setup `/api/v1` namespace dan struktur folder.
- Implementasi API response helpers (Success/Error envelopes).
- Integrasi Zod validation wrapper (Body, Query, Path).
- Request ID generation dan propagation.
- Boundary integration: Guest access, Authenticated session (Better Auth), dan Ownership baseline.
- Unit dan integration tests (colocated).

### Out of Scope
- Endpoint bisnis Detector, Humanizer, Payment, dan Credits.
- Database migration baru atau perubahan skema.
- Integrasi Redis, BullMQ, dan AI Provider.
- Security hardening tingkat lanjut (ruang lingkup M2.7).

## 4. API Contract Specification
### Response Envelopes
- **Success:** `{ "data": any, "meta": { "request_id": string, "timestamp": string } }`
- **Error:** `{ "error": { "code": string, "message": string, "field_errors": Record<string, string[]>, "request_id": string } }`
  - Seluruh respons error (HTTP 400, 401, 403, 404, 422, 500) wajib menggunakan struktur ini.
  - `field_errors` selalu tersedia; jika tidak ada kesalahan validasi field, gunakan objek kosong `{}`.

### HTTP Status Mapping
- **200/201**: Success / Created.
- **400**: Malformed JSON atau request syntax error.
- **401**: Unauthenticated (Missing/invalid session).
- **403**: Forbidden (Authenticated but lacking permission/ownership).
- **404**: Not Found (termasuk untuk menyamarkan keberadaan resource milik pengguna lain).
- **422**: Validation failure (Zod schema atau unknown fields).
- **500**: Internal server error (Tanpa stack trace atau detail internal).

## 5. Kebijakan Request ID
1. Server memeriksa header `x-request-id` dari request masuk.
2. Jika header berisi **UUID v4 yang valid** (pemeriksaan format dan versi), server boleh menggunakannya sebagai Request ID.
3. Jika tidak tersedia atau tidak valid (format salah atau bukan v4), server **wajib** membuat UUID v4 baru menggunakan `crypto.randomUUID()`.
4. Request ID wajib konsisten antara header `x-request-id` pada response dan field `request_id` dalam response body (baik pada Success maupun Error envelope).
5. Request ID hanya digunakan untuk korelasi dan pelacakan, bukan sebagai mekanisme keamanan (autentikasi/otorisasi).

## 6. Authentication dan Authorization Boundary
- **Guest Access:** Ditentukan secara eksplisit pada setiap endpoint.
- **Authentication:** Menggunakan `getServerSession()` (Better Auth).
- **Ownership Baseline:** Menggunakan helper pembanding ID yang sudah ada untuk menentukan respons 403 atau 404; bukan implementasi otorisasi database lengkap.
- **Legacy Route:** `/api/protected/example` dipertahankan sementara sebagai test route dan bukan merupakan acuan kontrak API v1.

## 7. Implementation Sequence
1. Setup `packages/contracts` dan Zod sebagai direct dependency.
2. Implementasi response helpers (Success/Error) di `apps/web/src/lib/api/`.
3. Implementasi validation wrapper untuk Body, Query, dan Path.
4. Setup rute `/api/v1` dan implementasi endpoint contoh `/health` (Public) dan `/test-auth` (Authenticated).
5. Penulisan colocated tests untuk memverifikasi seluruh skenario (valid/invalid).

## 8. Acceptance Criteria
- [ ] Zod terpasang sebagai direct dependency di `packages/contracts`.
- [ ] Success dan Error envelope sesuai spesifikasi kontrak 1:1 untuk seluruh status HTTP (400, 401, 403, 404, 422, 500).
- [ ] Unknown fields ditolak dengan HTTP 422 melalui Zod `strict()`.
- [ ] Malformed JSON menghasilkan HTTP 400 dengan Error Envelope standar.
- [ ] Request ID konsisten pada header dan body.
- [ ] Request ID divalidasi format dan versinya (UUID v4) jika berasal dari client; dibuat baru jika invalid atau absen.
- [ ] Guest endpoint dapat diakses tanpa session.
- [ ] Authenticated endpoint menghasilkan 401 ketika session tidak tersedia.
- [ ] HTTP 403 dikembalikan ketika terautentikasi tetapi tidak memiliki izin/kepemilikan (sesuai baseline helper).
- [ ] HTTP 404 dapat digunakan untuk menyamarkan keberadaan resource milik pengguna lain.
- [ ] HTTP 500 tidak mengekspos stack trace atau detail internal dan menggunakan Error Envelope standar.
- [ ] Unit dan integration tests (colocated) mencakup skenario request ID (valid, invalid, absent) serta seluruh pemetaan status HTTP.

## 9. Review Gate
- Status dokumen: **Proposed**.
- Implementasi hanya boleh dimulai setelah status berubah menjadi **Planning Approved**.
- Persetujuan task plan tidak otomatis memberikan izin implementasi.

## 10. Referensi
- `AGENTS.md`
- `plan/ACTIVE-ROADMAP.md`
- `plan/API-CONTRACTS.md`
- `plan/SYSTEM-DESIGN.md`
- `plan/SECURITY-ARCHITECTURE-AND-THREAT-MODEL.md`
- `plan/DATA-FLOW-AND-DATA-LIFECYCLE.md`

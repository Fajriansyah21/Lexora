# Task Plan: Database and Backend Foundation (M2)

- **Tanggal:** 2026-11-19
- **Branch:** `stage-7/m2-database-backend`
- **Status:** Planning Approved
- **Milestone:** Stage 7, M2
- **Architecture:** Modular Monolith

## 1. Objective

Membangun fondasi database dan backend Lexora menggunakan Next.js, PostgreSQL, Drizzle ORM, dan Better Auth.

## 2. Architecture Decision

`apps/web` menjadi aplikasi Next.js yang menangani frontend dan Backend-for-Frontend (BFF).

Backend menggunakan pemisahan modular:
- Database infrastructure
- Authentication
- API routes
- Domain services
- Security middleware

Logika domain tidak ditempatkan langsung di route handlers.

## 3. Scope

### In Scope
1. Inisialisasi Next.js App Router pada `apps/web`.
2. Integrasi PostgreSQL 18 dengan Drizzle ORM.
3. Konfigurasi Drizzle Kit dan migration workflow.
4. Implementasi skema autentikasi Better Auth.
5. Login dan logout menggunakan email/password.
6. Session management.
7. Protected API dan authorization baseline.
8. Zod validation.
9. CORS, security headers, dan rate limiting baseline.
10. Automated tests dan dokumentasi.

### Out of Scope
- AI Detector dan Humanizer integration.
- Payment dan Midtrans.
- Credits dan transaction system.
- Redis dan BullMQ.
- AI provider integration.
- Production deployment.

## 4. Database Strategy

- PostgreSQL 18 sebagai database utama.
- Database development: `lexora_dev`.
- Application role: `lexora_app`.
- Drizzle ORM sebagai database access layer.
- Drizzle Kit sebagai migration manager.
- Database credentials disimpan melalui environment variables.
- Tidak menggunakan akun superuser PostgreSQL untuk koneksi aplikasi.
- Tidak memasukkan credentials ke Git.

Skema awal dibatasi pada kebutuhan autentikasi dan fondasi backend. Entitas produk lain ditambahkan pada milestone yang relevan.

## 5. Implementation Sequence

| ID | Workstream | Deliverable |
|---|---|---|
| M2.1 | Documentation | Task plan dan roadmap |
| M2.2 | Web foundation | Next.js App Router |
| M2.3 | Database | Drizzle connection dan schema |
| M2.4 | Migrations | Versioned SQL migrations |
| M2.5 | Authentication | Better Auth integration |
| M2.6 | API foundation | API routes dan domain services |
| M2.7 | Security | Authentication guard dan security baseline |
| M2.8 | Verification | Integration tests dan acceptance evidence |

## 6. Acceptance Criteria

- [ ] Next.js berjalan di dalam monorepo.
- [ ] Database connection berhasil.
- [ ] Drizzle schema tersedia.
- [ ] Migrations berhasil dijalankan pada database development.
- [ ] Login berhasil.
- [ ] Logout berhasil.
- [ ] Session dapat diverifikasi.
- [ ] Protected API mengembalikan HTTP 401 tanpa session.
- [ ] Protected API menolak akses yang tidak terotorisasi.
- [ ] Security baseline diterapkan dan diuji.
- [ ] Existing M1 checks tetap lulus.
- [ ] Dokumentasi dan bukti pengujian diperbarui.

## 7. Constraints and Risks

- Mempertahankan kompatibilitas dengan pnpm workspace dan Turborepo.
- Tidak menghapus atau menimpa perubahan lokal yang sudah ada.
- Tidak mengubah file desain yang tidak berkaitan dengan M2.
- Tidak menyimpan secrets dalam source control.
- Tidak mengklaim acceptance criteria selesai tanpa bukti pengujian.
- Memperhatikan keterbatasan RAM lingkungan pengembangan lokal.

## 8. Review Gate

M2 hanya dapat dinyatakan selesai setelah seluruh acceptance criteria diverifikasi dan pengguna menyetujui hasilnya.

M3 tidak boleh dimulai sebelum mandatory review gate M2 diselesaikan.
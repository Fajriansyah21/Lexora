# Database Setup (M2.3)

Lexora uses PostgreSQL 18 with Drizzle ORM inside `apps/web`.

## Prerequisites

- PostgreSQL 18 running on `127.0.0.1:5432`.
- Database `lexora_dev` created.
- Role `lexora_app` with least-privilege access to `lexora_dev`.
- The role password is provided locally and never committed.

## Local environment

1. Copy the template:

   ```bash
   cp apps/web/.env.example apps/web/.env.local
   ```

2. Edit `apps/web/.env.local` and replace `REPLACE_WITH_LOCAL_PASSWORD` with the real password for `lexora_app`.

3. `apps/web/.env.local` is ignored by Git. Do not commit it.

## Better Auth setup (M2.4)

1. Copy environment template above.
2. In `.env.local`, configure:
   - `BETTER_AUTH_SECRET`: string acak minimal 32 karakter.
   - `BETTER_AUTH_URL`: URL lokal, misal `http://localhost:3000`.
   - `BETTER_AUTH_TRUSTED_ORIGINS`: origin tepercaya, misal `http://localhost:3000`.
3. Production proxy requirement:
   - `BETTER_AUTH_TRUSTED_PROXIES` wajib diisi daftar IP/CIDR proxy spesifik bila berjalan di belakang reverse proxy.
   - Jangan memasukkan IP client atau rentang publik luas ke variabel tersebut.

## Connection check

From the repository root:

```bash
corepack pnpm --filter @lexora/web db:check
```

Expected output (no credentials):

```
current_database: lexora_dev
current_user:    lexora_app
server_version:  PostgreSQL 18
Connection check OK.
```

## Drizzle Kit

Configuration lives in `apps/web/drizzle.config.ts`. It loads environment variables through `@next/env` so Drizzle Kit sees the same files as Next.js.

Schema path: `apps/web/src/db/schema.ts` (empty in M2.3).
Migration output: `apps/web/src/db/migrations` (not generated in M2.3).

Available scripts:

```bash
corepack pnpm --filter @lexora/web db:generate
corepack pnpm --filter @lexora/web db:migrate
```

Do not run either script during M2.3. The first migration, containing Better Auth tables, is created in M2.4.

## Connection pool

Development uses one `globalThis` pool with `max: 5`; production uses one module-scoped pool per process with `max: 10`. No capacity benchmark or production connection budget exists yet, so these values are intentionally conservative. Pool limits multiply across processes: for example, four production processes can open up to 40 connections. Reassess limits only after PostgreSQL capacity, process count, and workload concurrency are measured.

## Troubleshooting

- **`DATABASE_URL is not set`**: confirm `apps/web/.env.local` exists and contains `DATABASE_URL`.
- **Connection refused**: confirm PostgreSQL 18 is running and listening on `127.0.0.1:5432`.
- **Authentication failed**: confirm the password in `apps/web/.env.local` matches the `lexora_app` role.
- **Wrong database or role**: the check script fails if `current_database()` is not `lexora_dev` or `current_user` is not `lexora_app`.

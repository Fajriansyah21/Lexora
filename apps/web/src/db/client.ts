import { drizzle } from 'drizzle-orm/node-postgres';
import { Pool } from 'pg';

import { databaseUrl } from './env';

function createPool(): Pool {
  const isProduction = process.env.NODE_ENV === 'production';

  return new Pool({
    connectionString: databaseUrl,
    // Capacity is not benchmarked yet. Keep each process conservative because
    // pools multiply across dev workers and production processes.
    max: isProduction ? 10 : 5,
    idleTimeoutMillis: 30_000,
    connectionTimeoutMillis: 5_000,
  });
}

// In development, Next.js hot reload re-evaluates modules and would create a new
// pool on every reload. Storing the pool on globalThis keeps a single pool per
// dev server process. In production the pool is module-scoped: one pool per process.
const globalForDb = globalThis as unknown as { pool: Pool | undefined };

export const pool: Pool = globalForDb.pool ?? createPool();

if (process.env.NODE_ENV !== 'production') {
  globalForDb.pool = pool;
}

export const db = drizzle(pool);

let poolClosed = false;

// Cleanup hook for test runners and scripted shutdown. It is intentionally
// idempotent so it can be called more than once without side effects.
export async function closePool(): Promise<void> {
  if (poolClosed) {
    return;
  }

  poolClosed = true;
  await pool.end();

  if (process.env.NODE_ENV !== 'production') {
    globalForDb.pool = undefined;
  }
}

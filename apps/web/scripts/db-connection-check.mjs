// Read-only connectivity check for the local PostgreSQL instance.
//
// Verifies that the connection succeeds, that it targets the expected database
// and application role, and that the server runs PostgreSQL 18. It never
// mutates data and never prints the connection string or credentials.

import { createRequire } from 'node:module';
const require = createRequire(import.meta.url);
const { loadEnvConfig } = require('@next/env');
import pg from 'pg';

const EXPECTED_DATABASE = 'lexora_dev';
const EXPECTED_ROLE = 'lexora_app';

function loadDatabaseUrl() {
  loadEnvConfig(process.cwd());

  const url = process.env.DATABASE_URL;

  if (!url || url.trim().length === 0) {
    throw new Error(
      'DATABASE_URL is not set. Copy apps/web/.env.example to apps/web/.env.local and fill in local credentials.'
    );
  }

  return url;
}

async function main() {
  const connectionString = loadDatabaseUrl();
  const pool = new pg.Pool({ connectionString, max: 1, connectionTimeoutMillis: 5000 });

  try {
    const result = await pool.query(
      'select current_database() as database, current_user as role, version() as server_version'
    );
    const row = result.rows[0];

    console.log(`current_database: ${row.database}`);
    console.log(`current_user:    ${row.role}`);
    console.log(`server_version:  ${String(row.server_version).split(' ').slice(0, 2).join(' ')}`);

    const problems = [];

    if (row.database !== EXPECTED_DATABASE) {
      problems.push(`expected database ${EXPECTED_DATABASE}, got ${row.database}`);
    }

    if (row.role !== EXPECTED_ROLE) {
      problems.push(`expected role ${EXPECTED_ROLE}, got ${row.role}`);
    }

    if (!String(row.server_version).startsWith('PostgreSQL 18')) {
      problems.push(
        `expected PostgreSQL 18, got ${String(row.server_version).split(' ').slice(0, 2).join(' ')}`
      );
    }

    if (problems.length > 0) {
      console.error(`Connection check FAILED:\n- ${problems.join('\n- ')}`);
      process.exitCode = 1;
      return;
    }

    console.log('Connection check OK.');
  } catch {
    // Do not expose driver messages: they may include connection details.
    console.error(
      'Connection check FAILED: unable to connect or run the read-only identity query. Verify PostgreSQL is running, DATABASE_URL is configured locally, and lexora_app can access lexora_dev.'
    );
    process.exitCode = 1;
  } finally {
    await pool.end();
  }
}

await main();

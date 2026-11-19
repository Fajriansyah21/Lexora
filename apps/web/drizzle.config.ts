import { createRequire } from 'node:module';
import { defineConfig } from 'drizzle-kit';

const require = createRequire(import.meta.url);
const { loadEnvConfig } = require('@next/env') as typeof import('@next/env');

// Drizzle Kit runs outside the Next.js runtime, so environment files are loaded
// explicitly with @next/env (same loader and precedence as Next.js).
loadEnvConfig(process.cwd());

const databaseUrl = process.env.DATABASE_URL;

if (!databaseUrl || databaseUrl.trim().length === 0) {
  throw new Error(
    'DATABASE_URL is not set. Copy apps/web/.env.example to apps/web/.env.local and fill in local credentials.'
  );
}

export default defineConfig({
  dialect: 'postgresql',
  schema: './src/db/schema.ts',
  out: './src/db/migrations',
  dbCredentials: {
    url: databaseUrl,
  },
});

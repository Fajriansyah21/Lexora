const POSTGRES_URL_PATTERN = /^postgres(ql)?:\/\//;

function readDatabaseUrl(): string {
  const url = process.env.DATABASE_URL;

  if (!url || url.trim().length === 0) {
    throw new Error(
      'DATABASE_URL is not set. Copy apps/web/.env.example to apps/web/.env.local and fill in local credentials.'
    );
  }

  if (!POSTGRES_URL_PATTERN.test(url)) {
    throw new Error('DATABASE_URL must be a postgres:// or postgresql:// connection string.');
  }

  return url;
}

export const databaseUrl = readDatabaseUrl();

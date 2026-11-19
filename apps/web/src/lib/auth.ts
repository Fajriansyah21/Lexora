import { betterAuth } from 'better-auth';
import { drizzleAdapter } from '@better-auth/drizzle-adapter';

import { db } from '../db/client';
import * as schema from '../db/schema';
import { parseTrustedOrigins, parseTrustedProxies } from './security-config';

const betterAuthSecret = process.env.BETTER_AUTH_SECRET;
const betterAuthUrl = process.env.BETTER_AUTH_URL;
const trustedOrigins = parseTrustedOrigins(process.env.BETTER_AUTH_TRUSTED_ORIGINS);

if (!betterAuthSecret || betterAuthSecret.length < 32) {
  throw new Error('BETTER_AUTH_SECRET must be set and contain at least 32 characters.');
}

if (!betterAuthUrl) {
  throw new Error('BETTER_AUTH_URL must be set.');
}

if (trustedOrigins.length === 0) {
  throw new Error('BETTER_AUTH_TRUSTED_ORIGINS must contain at least one origin.');
}

const isProduction = process.env.NODE_ENV === 'production';
const parsedAuthUrl = new URL(betterAuthUrl);
const trustedProxies = parseTrustedProxies(process.env.BETTER_AUTH_TRUSTED_PROXIES, isProduction);

if (isProduction && parsedAuthUrl.protocol !== 'https:') {
  throw new Error('BETTER_AUTH_URL must use HTTPS in production.');
}

if (isProduction && trustedProxies.length === 0) {
  throw new Error(
    'BETTER_AUTH_TRUSTED_PROXIES must list trusted proxy IPs or CIDRs in production.'
  );
}

export const auth = betterAuth({
  database: drizzleAdapter(db, {
    provider: 'pg',
    schema,
  }),
  secret: betterAuthSecret,
  baseURL: betterAuthUrl,
  trustedOrigins,
  emailAndPassword: {
    enabled: true,
  },
  defaultCookieAttributes: {
    httpOnly: true,
    sameSite: 'lax',
    secure: isProduction,
  },
  advanced: {
    useSecureCookies: isProduction,
    ipAddress: {
      ipAddressHeaders: isProduction ? ['x-forwarded-for'] : [],
      ...(isProduction ? { trustedProxies } : {}),
    },
  },
  rateLimit: {
    enabled: true,
    window: 10,
    max: 100,
    customRules: {
      '/sign-in/email': {
        window: 10,
        max: 3,
      },
      '/sign-up/email': {
        window: 60,
        max: 5,
      },
    },
  },
});

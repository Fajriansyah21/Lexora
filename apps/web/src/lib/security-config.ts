import { isIP } from 'node:net';

function parseEntries(value: string | undefined): string[] {
  return (
    value
      ?.split(',')
      .map((entry) => entry.trim())
      .filter(Boolean) ?? []
  );
}

function isValidOrigin(origin: string): boolean {
  if (origin.endsWith('/')) return false;

  try {
    const parsed = new URL(origin);
    return (
      (parsed.protocol === 'http:' || parsed.protocol === 'https:') &&
      parsed.hostname.length > 0 &&
      parsed.username === '' &&
      parsed.password === '' &&
      parsed.pathname === '/' &&
      parsed.search === '' &&
      parsed.hash === '' &&
      (parsed.port === '' || Number(parsed.port) >= 0)
    );
  } catch {
    return false;
  }
}

function isValidProxyAddress(address: string): boolean {
  const slashIndex = address.indexOf('/');
  if (slashIndex === -1) return isIP(address) !== 0;
  if (slashIndex !== address.lastIndexOf('/')) return false;

  const ip = address.slice(0, slashIndex);
  const prefix = address.slice(slashIndex + 1);
  const version = isIP(ip);
  if (version === 0 || !/^\d+$/.test(prefix)) return false;

  const bits = Number(prefix);
  return bits >= 0 && bits <= (version === 4 ? 32 : 128);
}

export function parseTrustedOrigins(value: string | undefined): string[] {
  const origins = parseEntries(value);
  if (origins.length === 0 || origins.some((origin) => !isValidOrigin(origin))) {
    throw new Error(
      'BETTER_AUTH_TRUSTED_ORIGINS must contain valid HTTP or HTTPS origins without paths or trailing slashes.'
    );
  }
  return origins;
}

export function parseTrustedProxies(value: string | undefined, production = false): string[] {
  const proxies = parseEntries(value);
  if (production && proxies.length === 0) {
    throw new Error(
      'BETTER_AUTH_TRUSTED_PROXIES must list trusted proxy IPs or CIDRs in production.'
    );
  }
  if (proxies.some((proxy) => !isValidProxyAddress(proxy))) {
    throw new Error(
      'BETTER_AUTH_TRUSTED_PROXIES must contain valid IPv4, IPv6, or CIDR addresses.'
    );
  }
  return proxies;
}

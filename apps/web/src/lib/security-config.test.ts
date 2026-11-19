import { describe, expect, it } from 'vitest';

import { parseTrustedOrigins, parseTrustedProxies } from './security-config';

describe('parseTrustedOrigins', () => {
  it('accepts HTTP and HTTPS origins with valid ports', () => {
    expect(parseTrustedOrigins('http://localhost:3000,https://lexora.example')).toEqual([
      'http://localhost:3000',
      'https://lexora.example',
    ]);
  });

  it('rejects origins with trailing slash or path', () => {
    expect(() => parseTrustedOrigins('https://lexora.example/')).toThrow();
    expect(() => parseTrustedOrigins('https://lexora.example/app')).toThrow();
  });

  it('rejects origins with invalid scheme, hostname, port, or syntax', () => {
    expect(() => parseTrustedOrigins('ftp://lexora.example')).toThrow();
    expect(() => parseTrustedOrigins('https://')).toThrow();
    expect(() => parseTrustedOrigins('https://lexora.example:99999')).toThrow();
    expect(() => parseTrustedOrigins('not-an-origin')).toThrow();
  });

  it('rejects empty configuration', () => {
    expect(() => parseTrustedOrigins('')).toThrow();
    expect(() => parseTrustedOrigins(undefined)).toThrow();
  });
});

describe('parseTrustedProxies', () => {
  it('accepts IPv4, IPv6, and CIDR entries', () => {
    expect(parseTrustedProxies('127.0.0.1,10.0.0.0/8,2001:db8::1,2001:db8::/32')).toEqual([
      '127.0.0.1',
      '10.0.0.0/8',
      '2001:db8::1',
      '2001:db8::/32',
    ]);
  });

  it('rejects invalid IP and CIDR entries', () => {
    expect(() => parseTrustedProxies('999.1.1.1')).toThrow();
    expect(() => parseTrustedProxies('10.0.0.0/33')).toThrow();
    expect(() => parseTrustedProxies('2001:db8::/129')).toThrow();
    expect(() => parseTrustedProxies('10.0.0.1/')).toThrow();
  });

  it('rejects empty production configuration', () => {
    expect(() => parseTrustedProxies('', true)).toThrow();
    expect(() => parseTrustedProxies(undefined, true)).toThrow();
  });

  it('allows empty development configuration', () => {
    expect(parseTrustedProxies(undefined)).toEqual([]);
  });
});

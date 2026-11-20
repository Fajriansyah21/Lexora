import { describe, expect, it } from 'vitest';

import { authClient } from './auth-client';

describe('authClient', () => {
  it('exposes email auth and session methods', () => {
    expect(typeof authClient.signUp.email).toBe('function');
    expect(typeof authClient.signIn.email).toBe('function');
    expect(typeof authClient.signOut).toBe('function');
    expect(typeof authClient.getSession).toBe('function');
  });
});

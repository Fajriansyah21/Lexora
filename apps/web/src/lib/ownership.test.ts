import { describe, expect, it } from 'vitest';

import { canAccessOwnedResource } from './ownership';

describe('canAccessOwnedResource', () => {
  it('allows user to access their own resource', () => {
    expect(canAccessOwnedResource('user-a', 'user-a')).toBe(true);
  });

  it('denies access to another user resource', () => {
    expect(canAccessOwnedResource('user-a', 'user-b')).toBe(false);
  });

  it.each([
    [null, 'user-a'],
    ['user-a', null],
    [undefined, 'user-a'],
    ['user-a', undefined],
    ['', 'user-a'],
    ['user-a', ''],
    ['   ', 'user-a'],
    ['user-a', '   '],
  ])('denies invalid IDs: %s and %s', (currentUserId, resourceOwnerId) => {
    expect(canAccessOwnedResource(currentUserId, resourceOwnerId)).toBe(false);
  });
});

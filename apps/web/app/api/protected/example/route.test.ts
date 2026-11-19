import { beforeEach, describe, expect, it, vi } from 'vitest';

const { getServerSession } = vi.hoisted(() => ({
  getServerSession: vi.fn(),
}));

vi.mock('../../../../src/lib/server-session', () => ({
  getServerSession,
}));

import { GET } from './route';

describe('GET /api/protected/example', () => {
  beforeEach(() => {
    getServerSession.mockReset();
  });

  it('returns 401 when request has no valid session', async () => {
    getServerSession.mockResolvedValue(null);

    const response = await GET();

    expect(response.status).toBe(401);
    await expect(response.json()).resolves.toEqual({ error: 'Unauthorized' });
  });

  it('returns authenticated user ID when session is valid', async () => {
    getServerSession.mockResolvedValue({
      user: { id: 'user-123' },
      session: { id: 'session-123' },
    });

    const response = await GET();

    expect(response.status).toBe(200);
    await expect(response.json()).resolves.toEqual({ ok: true, userId: 'user-123' });
  });
});

import { describe, expect, it, vi } from 'vitest';

const { handler } = vi.hoisted(() => ({
  handler: vi.fn(async () => new Response('auth-handler-response')),
}));

vi.mock('../../../../src/lib/auth', () => ({
  auth: { handler },
}));

import { GET, POST } from './route';

describe('GET/POST /api/auth/[...all]', () => {
  it('delegates GET requests to the Better Auth handler', async () => {
    const request = new Request('http://localhost:3000/api/auth/get-session');

    const response = await GET(request);

    expect(handler).toHaveBeenCalledWith(request);
    await expect(response.text()).resolves.toBe('auth-handler-response');
  });

  it('delegates POST requests to the Better Auth handler', async () => {
    const request = new Request('http://localhost:3000/api/auth/sign-in/email', {
      method: 'POST',
    });

    const response = await POST(request);

    expect(handler).toHaveBeenCalledWith(request);
    await expect(response.text()).resolves.toBe('auth-handler-response');
  });
});

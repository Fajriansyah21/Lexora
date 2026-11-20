import { toNextJsHandler } from 'better-auth/next-js';

export const { GET, POST } = toNextJsHandler({
  handler: async (req) => {
    const { auth } = await import('../../../../src/lib/auth');
    return auth.handler(req);
  },
});

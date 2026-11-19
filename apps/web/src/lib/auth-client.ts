import { createAuthClient } from 'better-auth/client';

// Client-side auth client. It intentionally contains no secret and no
// database credentials: only the browser-facing endpoints are used.
export const authClient = createAuthClient();

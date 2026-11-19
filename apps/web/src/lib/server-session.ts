import { headers } from 'next/headers';

export async function getServerSession() {
  const { auth } = await import('./auth');
  return auth.api.getSession({ headers: await headers() });
}

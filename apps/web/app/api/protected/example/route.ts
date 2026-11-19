import { getServerSession } from '../../../../src/lib/server-session';

export async function GET() {
  const session = await getServerSession();

  if (!session) {
    return Response.json({ error: 'Unauthorized' }, { status: 401 });
  }

  return Response.json({ ok: true, userId: session.user.id });
}

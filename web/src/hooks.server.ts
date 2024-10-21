import type { Handle } from '@sveltejs/kit';
import { redirect } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  const session = event.cookies.get('session');
  const isAuthenticated = Boolean(session);

  if (event.url.pathname.startsWith('/signin')) {
    return await resolve(event);
  }

  if (!isAuthenticated) {
    throw redirect(303, '/signin');
  }

  return await resolve(event);
};

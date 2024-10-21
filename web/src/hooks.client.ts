import { goto } from '$app/navigation';

export const handle = async ({ event, resolve }) => {
  const response = await resolve(event);

  if (response.status === 401) {
    await goto('/signin');
  }

  return response;
};

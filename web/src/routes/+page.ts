import type { PageLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: PageLoad = async ({ fetch }) => {
  redirect(302, '/albums');
};

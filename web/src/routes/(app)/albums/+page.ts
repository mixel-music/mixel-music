import { getAlbumList } from '$lib/requests';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, url }) => {
  const start = parseInt(url.searchParams.get('start') ?? '1', 10);
  const end = parseInt(url.searchParams.get('end') ?? '40', 10);

  try {
    const data = await getAlbumList(fetch, start, end);

    return {
      list: data.list,
      title: 'albums.title',
      start: start,
      end: end,
    };
  }
  catch (error) {
    console.error(error);
  }
};

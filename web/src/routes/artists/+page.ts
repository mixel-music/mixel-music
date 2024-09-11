import { getArtistList } from '$lib/requests';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, url }) => {
  const page = parseInt(url.searchParams.get('page') ?? '1', 10);
  const item = parseInt(url.searchParams.get('item') ?? '48', 10);

  try {
    const data = await getArtistList(fetch, page, item);

    return {
      list: data.list,
      title: 'Artists',
      page: page,
      item: item,
    };
  }
  catch (error) {
    console.error(error);
  }
};
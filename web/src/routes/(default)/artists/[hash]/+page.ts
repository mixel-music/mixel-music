import { getArtistItem } from '$lib/requests';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
  const hash: string = params.hash

  try {
    const data = await getArtistItem(fetch, hash);

    return {
      item: data.item!,
      title: data.item.artist,
    };
  }
  catch (error) {
    console.error(error);
  }
};

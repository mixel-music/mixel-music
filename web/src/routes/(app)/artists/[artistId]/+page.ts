import { getArtistItem } from '$lib/requests';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
  const artistId: string = params.artistId

  try {
    const data = await getArtistItem(fetch, artistId);

    return {
      item: data.item!,
      title: data.item.artist,
    };
  }
  catch (error) {
    console.error(error);
  }
};

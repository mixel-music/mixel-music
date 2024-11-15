import { getArtist } from '$lib/requests';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
  const artistId: string = params.artistId

  try {
    const data = await getArtist(fetch, artistId);

    return {
      item: data.response!,
      title: data.response.artist,
    };
  }
  catch (error) {
    console.error(error);
  }
};

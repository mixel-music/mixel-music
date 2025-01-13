import { getArtist } from '$lib/requests';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
  const playlistId: string = params.playlistId

  try {
    const data = await getArtist(fetch, playlistId);

    return {
      item: data.response!,
      title: data.response.artist,
    };
  }
  catch (error) {
    console.error(error);
  }
};

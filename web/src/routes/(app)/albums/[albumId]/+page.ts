import { getAlbum } from '$lib/requests';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
  const albumId: string = params.albumId

  try {
    const data = await getAlbum(fetch, albumId);

    return {
      album: data.response!,
      title: data.response.album,
    };
  }
  catch (error) {
    console.error(error);
  }
};

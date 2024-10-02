import { getAlbumItem } from '$lib/requests';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
  const albumId: string = params.albumId

  try {
    const data = await getAlbumItem(fetch, albumId);

    return {
      item: data.item!,
      title: data.item.album,
    };
  }
  catch (error) {
    console.error(error);
  }
};

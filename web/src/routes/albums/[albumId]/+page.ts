import { getAlbumItem, getArtistItem } from '$lib/requests';
import type { PageLoad } from './$types';

export const load: PageLoad = async ({ fetch, params }) => {
  const albumId: string = params.albumId

  try {
    const data = await getAlbumItem(fetch, albumId);
    const moreData = await getArtistItem(fetch, data.item.albumartist_id);

    return {
      item: data.item!,
      list: moreData.item.albums,
      title: data.item.album,
    };
  }
  catch (error) {
    console.error(error);
  }
};

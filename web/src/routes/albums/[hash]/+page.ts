import type { PageLoad } from './$types';
import type { Album } from '$lib/interface';

export const load: PageLoad = async ({ fetch, params }) => {
  const albumHash: string = params.hash;
  let albumItem: any = [];

  const getAlbum = await fetch(`http://localhost:2843/api/albums/${ albumHash }`);
  albumItem = await getAlbum.json();

  return {
    albumItem,
    title: albumItem.album,
  }
}
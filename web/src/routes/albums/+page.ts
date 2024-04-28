import type { PageLoad } from './$types';
import type { Album } from '$lib/interface';

export const load: PageLoad = async ({ fetch }) => {
  let albumListItem: Album[] = [];

  const getAlbumList = await fetch('http://localhost:2843/api/albums');
  albumListItem = await getAlbumList.json();

  return {
    albumListItem,
    title: 'Albums',
  };
};
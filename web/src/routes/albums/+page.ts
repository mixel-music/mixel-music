import type { PageLoad } from './$types';
import type { albumListModel } from '$lib/model';

export const load: PageLoad = async ({ fetch }) => {
  let albumListItem: albumListModel[] = [];

  const getAlbumList = await fetch('http://localhost:2843/api/albums');
  albumListItem = await getAlbumList.json();

  return {
    albumListItem,
    title: 'Albums',
  };
};
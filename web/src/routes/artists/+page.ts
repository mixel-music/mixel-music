import type { PageLoad } from './$types';
import type { artistListModel } from '$lib/model';

export const load: PageLoad = async ({ fetch }) => {
  let artistListItem: artistListModel[] = [];

  const getArtistList = await fetch('http://localhost:2843/api/artists');
  artistListItem = await getArtistList.json();

  return {
    artistListItem,
    title: 'Artists',
  };
};
import type { PageLoad } from './$types';
import type { artistList } from '$lib/interface';

export const load: PageLoad = async ({ fetch }) => {
  let artistListItem: artistList[] = [];

  const getArtistList = await fetch('http://localhost:2843/api/artists');
  artistListItem = await getArtistList.json();

  return {
    artistListItem,
    title: 'Artists',
  };
};
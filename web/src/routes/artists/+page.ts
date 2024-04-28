import type { PageLoad } from './$types';
import type { Artist } from '$lib/interface';

export const load: PageLoad = async ({ fetch }) => {
  let artistListItem: Artist[] = [];

  const getArtistList = await fetch('http://localhost:2843/api/artists');
  artistListItem = await getArtistList.json();

  return {
    artistListItem,
    title: 'Artists',
  };
};
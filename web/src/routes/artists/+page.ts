import type { PageLoad } from './$types';

export const load = (async () => {
  interface artistItemModel {
    artisthash: string;
    artist: string;
  }

  let artistItem: artistItemModel[] = [];

  const artistFetch = await fetch('http://localhost:2843/api/artists');
  const artist = await artistFetch.json();

  artistItem = artist.map((tag: any) => ({
    artisthash: tag.artisthash,
    artist: tag.artist,
  }));

  return {
    artistItem,
    title: 'Artists',
  };
}) satisfies PageLoad;
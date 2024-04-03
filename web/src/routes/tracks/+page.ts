import type { PageLoad } from './$types';

export const load = (async () => {
  interface trackItemModel {
    hash: string;
    title: string;
    album: string;
    artist: string;
    imagehash: string;
  }

  let trackItem: trackItemModel[] = [];

  const trackFetch = await fetch('http://localhost:2843/api/tracks');
  const track = await trackFetch.json();

  trackItem = track.map((tag: any) => ({
    hash: tag.hash,
    title: tag.title,
    album: tag.album,
    artist: tag.artist,
    imagehash: tag.imagehash,
  }));

  return {
    trackItem,
    title: 'Tracks',
  };
}) satisfies PageLoad;
import type { PageLoad } from './$types';

export const load = (async () => {
  interface albumItemModel {
    albumhash: string;
    album: string;
    albumartist: string;
    imagehash: string;
  }

  let albumItem: albumItemModel[] = [];

  const albumFetch = await fetch('http://localhost:2843/api/albums');
  const album = await albumFetch.json();

  albumItem = album.map((tag: any) => ({
    albumhash: tag.albumhash,
    album: tag.album,
    albumartist: tag.albumartist,
    imagehash: tag.imagehash,
  }));

  return {
    albumItem,
    title: 'Albums',
  };
}) satisfies PageLoad;
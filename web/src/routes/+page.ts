import type { PageLoad } from './$types';
import { redirect } from '@sveltejs/kit';

export const load: PageLoad = async ({ fetch }) => {
  redirect(302, '/albums');
  
  interface trackItemModel {
    hash: string;
    title: string;
    album: string;
    artist: string;
    imagehash: string;
  }

  let trackItem: trackItemModel[] = [];

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

  // 캡슐화해서 재사용 고려해야 함

  const trackFetch = await fetch('http://localhost:2843/api/tracks?num=8');
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
    title: 'For you', // title이 여러 개 나오는 경우 고려해야 함
  };
};
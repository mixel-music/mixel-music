import type { PageLoad } from './$types';
import type { Track } from '$lib/interface';

export const load: PageLoad = async ({ fetch }) => {
  let trackListItem: Track[] = [];

  const getTrackList = await fetch('http://localhost:2843/api/tracks');
  trackListItem = await getTrackList.json();

  return {
    trackListItem,
    title: 'Tracks',
  };
};
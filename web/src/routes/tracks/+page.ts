import type { PageLoad } from './$types';
import type { trackListModel } from '$lib/model';

export const load: PageLoad = async ({ fetch }) => {
  let trackListItem: trackListModel[] = [];

  const getTrackList = await fetch('http://localhost:2843/api/tracks');
  trackListItem = await getTrackList.json();

  return {
    trackListItem,
    title: 'Tracks',
  };
};
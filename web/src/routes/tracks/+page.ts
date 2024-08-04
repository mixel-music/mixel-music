import type { PageLoad } from './$types';
import type { Track } from '$lib/interface';

export const load: PageLoad = async ({ fetch, url }) => {
  let trackListItem: Track[] = [];

  const pageCount = parseInt(url.searchParams.get('page') ?? '1', 10);
  const itemCount = parseInt(url.searchParams.get('item') ?? '40', 10);

  try {
    const response = await fetch(`http://localhost:2843/api/tracks?page=${pageCount}&item=${itemCount}`);
    
    if (!response.ok) {
      throw new Error(`Please check your internet connection, ${response.statusText}`);
    }
    
    trackListItem = await response.json();
  } catch (error) {
    console.error('Failed to fetch track list:', error);
  }

  return {
    trackListItem,
    title: 'Tracks',
  };
};
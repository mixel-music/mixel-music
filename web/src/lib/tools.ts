export const getArtwork = (id: string, size: number): string => {
  return `http://localhost:2843/api/artworks/${id}?size=${size.toString()}`;
};


export const getAlbumLink = (albumId: string): string => {
  return `/albums/${albumId}`;
};


export const getArtistLink = (artistId: string): string => {
  return `/artists/${artistId}`;
};


import { getAlbumList, getArtistList, getTrackList } from "./requests";
import { replaceState } from "$app/navigation";

type pageDirection = 'next' | 'prev';
type pageDataTypes = 'album' | 'artist' | 'track';

export async function getPaginatedList(
  fetch: typeof window.fetch,
  direction: pageDirection,
  dataType: pageDataTypes,
  total: number,
  start: number,
  count: number,
) {

  let newStart, newEnd;
  let response;

  if (direction === 'next') {
    newStart = Math.min(start + count, total);
    newEnd = Math.min(newStart + count, total);

    if (newStart >= total - (total % count)) {
        newStart = total - (total % count) + 1;
        newEnd = total;
    }

    switch (dataType) {
      case 'album':
        response = await getAlbumList(fetch, newStart, newEnd);
        break;
      case 'artist':
        response = await getArtistList(fetch, newStart, newEnd);
        break;
      case 'track':
        response = await getTrackList(fetch, newStart, newEnd);
        break;
      default:
        throw new Error('Invalid data type');
    }
  } else {
      newStart = Math.max(start - 40, 1);
      newEnd = newStart + 40;

      if (newStart === 1) {
          newEnd = Math.min(40, total);
      }

      switch (dataType) {
        case 'album':
          response = await getAlbumList(fetch, newStart, newEnd);
          break;
        case 'artist':
          response = await getArtistList(fetch, newStart, newEnd);
          break;
        case 'track':
          response = await getTrackList(fetch, newStart, newEnd);
          break;
        default:
          throw new Error('Invalid data type');
      }
  } 

  return { newStart, newEnd, response };
};


export function removeLinkParams(params: Record<string, string>): void {
  const url = new URL(window.location.href);

  Object.keys(params).forEach((key) => {
    url.searchParams.set(key, params[key]);
  });

  replaceState('', url.pathname);
};


export function convertDateTime(time: number): string {
  const min = Math.floor(time / 60);
  const sec = Math.floor(time % 60);

  return `${ min }:${ sec < 10 ? '0' : '' }${ sec }`;
};


export function convertFileSize(size: number): string {
  const units = ['B', 'KB', 'MB', 'GB'];
  let index = 0;

  while (size >= 1024 && index < units.length - 1) {
    size /= 1024;
    index++;
  }

  return `${size.toFixed(2)} ${units[index]}`;
};

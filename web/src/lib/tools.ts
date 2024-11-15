export async function apiFetch(
  fetch: typeof window.fetch,
  url: string,
  options = {}
) {

  const response = await fetch(url, {
    ...options,
    credentials: 'include',
  });

  if (response.status === 401) {
    window.location.href = '/signin';
  }

  return response;
}


export function handleLogout(fetch: typeof window.fetch): void {
  postLogout(fetch);
};


export const getArtwork = (id: string, size: number): string => {
  return `http://localhost:2843/api/library/artworks/${id}?size=${size.toString()}`;
};


export const getAlbumLink = (albumId: string): string => {
  return `/albums/${albumId}`;
};


export const getArtistLink = (artistId: string): string => {
  return `/artists/${artistId}`;
};


import { replaceState } from "$app/navigation";
import { getAlbums, getArtists, getTracks, postLogout } from "./requests";

type PageDirection = 'next' | 'prev';
type PageDataTypes = 'album' | 'artist' | 'track';

export async function getPaginatedList(
  fetch: typeof window.fetch,
  direction: PageDirection,
  dataType: PageDataTypes,
  total: number,
  start: number,
  count: number,
) {
  const getList = (type: PageDataTypes) => {
    switch (type) {
      case 'album':
        return getAlbums;
      case 'artist':
        return getArtists;
      case 'track':
        return getTracks;
      default:
        throw new Error('Invalid data type');
    }
  };

  const fetchList = getList(dataType);
  let newStart: number;
  let newEnd: number;

  if (direction === 'next') {
    newStart = Math.min(start + count + 1, total);
    newEnd = Math.min(newStart + count, total);
  }
  else {
    newStart = Math.max(start - count - 1, 1);
    newEnd = Math.min(newStart + count, total);
  }

  const response = await fetchList(fetch, newStart, newEnd);
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

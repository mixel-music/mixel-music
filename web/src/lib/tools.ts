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
import type { AlbumListResponse, ArtistListResponse, TrackListResponse } from "./interface";
import { replaceState } from "$app/navigation";

type pageDirection = 'next' | 'prev';
type pageDataTypes = 'album' | 'artist' | 'track';

export async function getPaginatedList(
  fetch: typeof window.fetch,
  direction: pageDirection,
  dataType: pageDataTypes,
  currentPage: number,
  itemsPerPage: number,
  totalItems: number,
) {

  const totalPages = Math.ceil(totalItems / itemsPerPage);

  let newPage = direction === 'next'
    ? Math.min(currentPage + 1, totalPages)
    : Math.max(currentPage - 1, 1);
  let response;

  switch (dataType) {
    case 'album':
      response = await getAlbumList(fetch, newPage, itemsPerPage);
      break;
    case 'artist':
      response = await getArtistList(fetch, newPage, itemsPerPage);
      break;
    case 'track':
      response = await getTrackList(fetch, newPage, itemsPerPage);
      break;
      
    default:
      throw new Error('Invalid data type');
  }

  return { newPage, response };
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

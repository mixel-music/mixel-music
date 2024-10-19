import type {
  AlbumListResponse,
  TrackListResponse,
  ArtistListResponse,
  TrackItemResponse,
  AlbumItemResponse,
  ArtistItemResponse
} from "./interface";
import { apiFetch } from "./tools";


export async function postLogout(fetch: typeof window.fetch): Promise<void> {
  try {
    const postLogout = await fetch(
      `http://localhost:2843/api/auth/logout`,
      {
        method: 'POST',
        credentials: 'include',
      }
    );

    if (!postLogout.ok) {
      throw new Error(postLogout.statusText);
    }

    window.location.href = '/signin';

  }

  catch (error) {
    console.error('Logout failed:', error);
    throw new Error('Failed to log out');
  }
}


export async function getTrackList(
  fetch: typeof window.fetch,
  start: number,
  end: number,
): Promise<{list: TrackListResponse;}> {

  try {
    const getTrackList = await apiFetch(fetch,
      `http://localhost:2843/api/library/tracks?start=${start}&end=${end}`);

    if (!getTrackList.ok) {
      throw new Error(getTrackList.statusText);
    }

    const list: TrackListResponse = await getTrackList.json();

    return {
      list,
    };
  }
  
  catch (error) {
    return {
      list: null,
    }
  }
};


export async function getTrackItem(
  fetch: typeof window.fetch,
  trackId: string,
): Promise<{item: TrackItemResponse;}> {
  
  try {
    const getTrackItem = await apiFetch(fetch,
      `http://localhost:2843/api/library/tracks/${trackId}`);

    if (!getTrackItem.ok) {
      throw new Error(getTrackItem.statusText);
    }

    const item: TrackItemResponse = await getTrackItem.json();

    return {
      item,
    };
  }

  catch (error) {
    throw error;
  }
};


export async function getAlbumList(
  fetch: typeof window.fetch,
  start: number,
  end: number,
): Promise<{list: AlbumListResponse;}> {

  try {
    const getAlbumList = await apiFetch(fetch,
      `http://localhost:2843/api/library/albums?start=${start}&end=${end}`);

    if (!getAlbumList.ok) {
      throw new Error(getAlbumList.statusText);
    }

    const list: AlbumListResponse = await getAlbumList.json();

    return {
      list,
    };
  }

  catch (error) {
    return {
      list: null,
    }
  }
};


export async function getAlbumItem(
  fetch: typeof window.fetch,
  albumId: string,
): Promise<{item: AlbumItemResponse;}> {

  try {
    const getAlbumItem = await apiFetch(fetch,
      `http://localhost:2843/api/library/albums/${albumId}`);

    if (!getAlbumItem.ok) {
      throw new Error(getAlbumItem.statusText);
    }

    const item: AlbumItemResponse = await getAlbumItem.json();

    return {
      item,
    };
  }

  catch (error) {
    throw error;
  }
};


export async function getArtistList(
  fetch: typeof window.fetch,
  start: number,
  end: number,
): Promise<{list: ArtistListResponse;}> {

  try {
    const getArtistList = await apiFetch(fetch,
      `http://localhost:2843/api/library/artists?start=${start}&end=${end}`);

    if (!getArtistList.ok) {
      throw new Error(getArtistList.statusText);
    }

    const list: ArtistListResponse = await getArtistList.json();

    return {
      list,
    };
  }

  catch (error) {
    return {
      list: null,
    }
  }
};


export async function getArtistItem(
  fetch: typeof window.fetch,
  artistId: string,
): Promise<{item: ArtistItemResponse;}> {

  try {
    const getArtistItem = await apiFetch(fetch,
      `http://localhost:2843/api/library/artists/${artistId}`);

    if (!getArtistItem.ok) {
      throw new Error(getArtistItem.statusText);
    }

    const item: ArtistItemResponse = await getArtistItem.json();

    return {
      item,
    };
  }

  catch (error) {
    throw error;
  }
};

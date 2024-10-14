import type {
  AlbumListResponse,
  TrackListResponse,
  ArtistListResponse,
  TrackItemResponse,
  AlbumItemResponse,
  ArtistItemResponse
} from "./interface";


export async function getTrackList(
  fetch: typeof window.fetch,
  start: number,
  end: number,
): Promise<{list: TrackListResponse;}> {

  try {
    const getTrackList = await fetch(
      `http://localhost:2843/api/tracks?start=${start}&end=${end}`,
      { credentials: 'include' }
    );

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
    const getTrackItem = await fetch(
      `http://localhost:2843/api/tracks/${trackId}`,
      { credentials: 'include' }
    );

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
    const getAlbumList = await fetch(
      `http://localhost:2843/api/albums?start=${start}&end=${end}`,
      { credentials: 'include' }
    );

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
    const getAlbumItem = await fetch(
      `http://localhost:2843/api/albums/${albumId}`,
      { credentials: 'include' }
    );

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
    const getArtistList = await fetch(
      `http://localhost:2843/api/artists?start=${start}&end=${end}`,
      { credentials: 'include' }
    );

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
    const getArtistItem = await fetch(
      `http://localhost:2843/api/artists/${artistId}`,
      { credentials: 'include' }
    );

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

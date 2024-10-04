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
  page: number,
  item: number,
): Promise<{list: TrackListResponse;}> {

  try {
    const getTrackList = await fetch(`http://localhost:2843/api/tracks?page=${page}&item=${item}`);

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
    const getTrackItem = await fetch(`http://localhost:2843/api/tracks/${trackId}`);

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
  page: number,
  item: number,
): Promise<{list: AlbumListResponse;}> {

  try {
    const getAlbumList = await fetch(`http://localhost:2843/api/albums?page=${page}&item=${item}`);

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
    const getAlbumItem = await fetch(`http://localhost:2843/api/albums/${albumId}`);

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
  page: number,
  item: number,
): Promise<{list: ArtistListResponse;}> {

  try {
    const getArtistList = await fetch(`http://localhost:2843/api/artists?page=${page}&item=${item}`);

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
    const getArtistItem = await fetch(`http://localhost:2843/api/artists/${artistId}`);

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

export async function getTrackList(page: number, item: number) {
  try {
    const getTrackList = await fetch(`http://localhost:2843/api/tracks?page=${page}&item=${item}`);
    const getTotalCount = await fetch(`http://localhost:2843/api/count?type=0`);

    if (!getTrackList.ok) {
      throw new Error(getTrackList.statusText);
    }

    const list = await getTrackList.json();
    const total: number = await getTotalCount.json();

    return {
      list,
      total,
    };
  }
  catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getTrackItem(hash: string) {
  try {
    const getTrackItem = await fetch(`http://localhost:2843/api/tracks/${hash}`);

    if (!getTrackItem.ok) {
      throw new Error(getTrackItem.statusText);
    }

    const item = await getTrackItem.json();

    return {
      item,
    };
  }
  catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getAlbumList(page: number, item: number) {
  try {
    const getAlbumList = await fetch(`http://localhost:2843/api/albums?page=${page}&item=${item}`);
    const getTotalCount = await fetch(`http://localhost:2843/api/count?type=1`);

    if (!getAlbumList.ok) {
      throw new Error(getAlbumList.statusText);
    }

    const list = await getAlbumList.json();
    const total: number = await getTotalCount.json();

    return {
      list,
      total,
    };
  }
  catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getAlbumItem(hash: string) {
  try {
    const getAlbumItem = await fetch(`http://localhost:2843/api/albums/${hash}`);

    if (!getAlbumItem.ok) {
      throw new Error(getAlbumItem.statusText);
    }

    const item = await getAlbumItem.json();

    return {
      item,
    };
  }
  catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getArtistList(page: number, item: number) {
  try {
    const getArtistList = await fetch(`http://localhost:2843/api/artists?page=${page}&item=${item}`);
    const getTotalCount = await fetch(`http://localhost:2843/api/count?type=2`);

    if (!getArtistList.ok) {
      throw new Error(getArtistList.statusText);
    }

    const list = await getArtistList.json();
    const total: number = await getTotalCount.json();

    return {
      list,
      total,
    };
  }
  catch (error) {
    console.error(error);
    throw error;
  }
}

export async function getArtistItem(hash: string) {
  try {
    const getArtistItem = await fetch(`http://localhost:2843/api/artists/${hash}`);

    if (!getArtistItem.ok) {
      throw new Error(getArtistItem.statusText);
    }

    const item = await getArtistItem.json();

    return {
      item,
    };
  }
  catch (error) {
    console.error(error);
    throw error;
  }
}
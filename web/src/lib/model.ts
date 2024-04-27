interface trackListModel {
  hash: string;
  title: string;
  album: string;
  albumhash: string;
  artist: string;
  artisthash: string;
  imagehash: string;
}

interface albumListModel {
  albumhash: string;
  album: string;
  albumartist: string;
  imagehash: string;
  year: number;
}

interface artistListModel {
  artisthash: string;
  artist: string;
  imagehash: string;
}

interface trackModel {
  hash: string;
  title: string;
  album: string;
  albumhash: string;
  artist: string;
  artisthash: string;
  imagehash: string;
  date: string;
  year: number;
  musicbrainz_trackid: string;
}

interface albumModel {
  albumhash: string;
  album: string;
  albumartist: string;
  imagehash: string;
  year: number;
  tracktotals: number;
  disctotals: number;
}

export type { 
  trackListModel,
  albumListModel,
  artistListModel,
  trackModel,
  albumModel,
}
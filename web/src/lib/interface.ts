export interface trackList {
  title: string;
  album: string;
  artist: string;
  hash: string;
  albumhash: string;
}

export interface trackItem {
  hash: string;
  title: string;
  artist: string;
  artisthash: string;
  album: string;
  albumhash: string
  albumartist: string;
  bitdepth: number;
  bitrate: number;
  channels: number;
  comment: string;
  composer: string;
  disc: number;
  disctotal: number;
  duration: number;
  size: number;
  genre: string;
  samplerate: number;
  track: number;
  tracktotal: number;
  year: string;
  directory: string;
  mime: string;
  path: string;
  created_date: Date;
  updated_date: Date;
  lyrics: string;
  isrc: string;
}

export interface albumList {
  albumhash: string;
  album: string;
  albumartist: string;
  albumartisthash: string;
  year: string;
  durationtotals: number;
  tracktotals: number;
  disctotals: number;
  sizetotals: number;
}

export interface albumItem {
  albumhash: string;
  album: string;
  albumartist: string;
  albumartisthash: string;
  year: string;
  durationtotals: number;
  tracktotals: number;
  disctotals: number;
  sizetotals: number;
  tracks: albumTrackItem[];
}

export interface albumTrackItem {
  title: string;
  artist: string;
  duration: number;
  track: number;
  hash: string;
  comment: string;
}

export interface artistList {
  artisthash: string;
  artist: string;
}

export interface artistItem {

}
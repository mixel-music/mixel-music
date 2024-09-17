export interface TrackListResponse {
  list: TrackList[];
  total: number;
}

export interface TrackList {
  album: string;
  album_id: string;
  artist: string;
  artist_id?: string;
  duration?: number;
  title: string;
  track_id: string;

  artwork?: string;
  index?: number;
}

export interface TrackItem {
  album: string;
  album_id: string;
  albumartist: string;
  albumartist_id: string;
  artist: string;
  artist_id: string;
  artwork_id: string;
  bitdepth: number;
  bitrate: number;
  channels: number;
  compilation: boolean;
  comment: string;
  composer: string;
  content_type: string;
  created_at?: string;
  date: string;
  director: string;
  directory: string;
  duration: number;
  disc_number: number;
  disc_total: number;
  filepath: string;
  filesize: number;
  genre: string;
  isrc: string;
  label: string;
  lyrics: string;
  samplerate: number;
  title: string;
  track_id: string;
  track_number: number;
  track_total: number;
  updated_at?: string;
  year: number;
}

export interface AlbumListResponse {
  list: AlbumList[];
  total: number;
}

export interface AlbumList {
  album: string;
  album_id: string;
  albumartist: string;
  albumartist_id: string;
  year: number;
}

export interface AlbumItem {
  album: string;
  album_id: string;
  albumartist: string;
  albumartist_id: string;
  disc_total: number;
  duration_total: number;
  filesize_total: number;
  year: string;

  tracks: [
    artist: string,
    artist_id: string,
    comment: string,
    duration: number,
    title: string,
    track_id: string,
    track_number: number,
  ];
}

export interface ArtistListResponse {
  list: ArtistList[];
  total: number;
}

export interface ArtistList {
  artist_id: string;
  artist: string;
}

export interface ArtistItem {
  artist: string;
  artist_id: string;

  albums: AlbumItem[];
}

export interface PlayerState {
  index: number;
  lists: TrackList[];
  isLoaded: boolean;
  isPlaying: boolean;
  currentTime: number;
  volumeRange: number;
  duration: number;
  volume: number;
  mute: boolean;
  loop: number;
}

export interface PlayerStore extends PlayerState, TrackList {}
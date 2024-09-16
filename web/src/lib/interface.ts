export interface TrackListResponse {
  list: TrackList[];
  total: number;
}

export interface TrackList {
  track_id: string;
  album_id: string;
  artist_id: string;
  title: string;
  album: string;
  artist: string;
  duration?: number;
  artwork?: string;
  index?: number;
}

export interface TrackItem {
  track_id: string;
  album_id: string;
  artist_id: string;
  albumartist_id: string;
  title: string;
  album: string;
  albumartist: string;
  composer: string;
  artist: string;
  genre: string;
  total_track: number;
  total_disc: number;
  track: number
  disc: number;
  label: string;  
  lyrics: string;
  comment: string;
  copyright: string;
  filepath: string;
  filesize: number;
  duration: number;
  mime: string;
  date: Date;
  year: number;
  bitrate: number;
  bitdepth: number;
  channels: number;
  samplerate: number
  created_at: Date;
  updated_at: Date;
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
  total_filesize: number;
  total_duration: number;
  total_disc: number;
  year: number;
  tracks: TrackItem[];
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
  artist_id: string;
  artist: string;
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
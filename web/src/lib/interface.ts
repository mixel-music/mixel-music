export interface TrackList {
  album: string;
  album_id: string;
  artist: string;
  artist_id: string;
  duration: number;
  title: string;
  track_id: string;
};


export interface TrackListResponse {
  list: TrackList[];
  total: number;
};


export interface TrackItem {
  album: string;
  album_id: string;
  albumartist: string;
  albumartist_id: string;
  artist: string;
  artist_id: string;
  bitdepth: number;
  bitrate: number;
  channels: number;
  compilation: boolean;
  comment?: string;
  composer?: string;
  content_type: string;
  created_at?: string;
  date?: string;
  director?: string;
  directory: string;
  duration: number;
  disc_number: number;
  disc_total: number;
  filepath: string;
  filesize: number;
  genre?: string;
  isrc?: string;
  label?: string;
  lyrics?: string;
  samplerate: number;
  title: string;
  track_id: string;
  track_number: number;
  track_total: number;
  updated_at: string;
  year?: number;
};


export interface TrackItemResponse extends TrackItem {
  
};


export interface AlbumList {
  album: string;
  album_id: string;
  albumartist: string;
  albumartist_id: string;
  year?: number;
};


export interface AlbumListResponse {
  list: AlbumList[]
  total: number;
};


export interface AlbumItem {
  album: string;
  album_id: string;
  albumartist: string;
  albumartist_id: string;
  disc_total: number;
  duration_total: number;
  filesize_total: number;
  year?: number;
};


export interface AlbumTrack {
  artist: string;
  artist_id: string;
  comment?: string;
  duration: number;
  title: string;
  track_id: string;
  track_number: number;
};


export interface AlbumItemResponse extends AlbumItem {
  tracks: AlbumTrack[];
};


export interface ArtistList {
  artist: string;
  artist_id: string;
};


export interface ArtistListResponse {
  list: ArtistList[];
  total: number;
};


export interface ArtistItem {
  artist: string;
  artist_id: string;
};


export interface ArtistAlbum {
  album: string;
  album_id: string;
  albumartist_id: string;
  year?: number;
};


export interface ArtistItemResponse extends ArtistItem {
  albums: ArtistAlbum[];
};


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
};


export interface PlayerStore extends PlayerState, TrackList {
  artwork?: string;
}

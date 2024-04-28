interface Track {
  hash: string;
  title: string;
  album: string;
  albumhash?: string;
  artist?: string;
  artisthash?: string;
  imagehash?: string;
  date?: string;
  year?: number;
  musicbrainz_trackid?: string;
}

interface Album {
  albumhash: string;
  album: string;
  albumartist: string;
  imagehash?: string;
  year?: number;
  tracktotals: number;
  disctotals: number;
}

interface Artist {
  artisthash: string;
  artist: string;
  imagehash?: string;
}

export type {
  Track,
  Album,
  Artist,
}
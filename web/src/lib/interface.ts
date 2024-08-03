interface Track {
  hash: string;
  title: string;
  album: string;
  albumhash?: string;
  artist?: string;
  artisthash?: string;
  year?: number;
}

interface Album {
  albumhash: string;
  album: string;
  albumartist: string;
  year?: number;
  tracktotals: number;
  disctotals: number;
}

interface Artist {
  artisthash: string;
  artist: string;
}

export type {
  Track,
  Album,
  Artist,
}
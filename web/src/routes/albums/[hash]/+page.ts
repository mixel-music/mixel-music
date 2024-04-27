import type { PageLoad } from './$types';
import type { albumModel } from '$lib/model';

export const load: PageLoad = async ({ fetch, params }) => {
  const albumHash: string = params.hash;
  let albumItem: albumModel[] = [];

  const getAlbum = await fetch(`http://localhost:2843/api/albums/${ albumHash }`);
  albumItem = await getAlbum.json();

  return {
    albumItem,
  }
}

// export const load: PageLoad = async ({ fetch, params }) => {
//   const albumHash = params.hash

//   interface albumItemModel {
//     [key: string]: any;
//   }

//   let albumItem: albumItemModel[] = [];

//   const albumFetch = await fetch(`http://localhost:2843/api/albums/${ albumHash }`);
//   const album = await albumFetch.json();

//   return {
//     album: album,
//     title: 'Albums',
//   };
// };
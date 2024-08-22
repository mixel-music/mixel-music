import { writable } from 'svelte/store';

export const trackStore = writable({
  hash: '',
  title: '',
  album: '',
  artist: '',
  artwork: '',
  albumhash: '',
});
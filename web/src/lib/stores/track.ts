import { writable, type Writable } from 'svelte/store';

const trackHash: Writable<string | undefined> = writable();
const trackTitle: Writable<string | undefined> = writable();
const trackAlbum: Writable<string> = writable('Unknown Album');
const trackArtist: Writable<string> = writable('Unknown Artist');

export {
  trackHash,
  trackTitle,
  trackAlbum,
  trackArtist,
}
import { writable, type Writable } from 'svelte/store';

const hash: Writable<string | undefined> = writable(undefined)
const title: Writable<string | undefined> = writable(undefined);
const album: Writable<string | undefined> = writable(undefined);
const artist: Writable<string | undefined> = writable(undefined);
const imagehash: Writable<string | undefined> = writable(undefined);

export {
  hash,
  title,
  album,
  artist,
  imagehash,
}
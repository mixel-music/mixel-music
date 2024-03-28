import { writable } from 'svelte/store';

const hash = writable(null)
const title = writable(null);
const album = writable(null);
const artist = writable(null);
const imagehash = writable(null);

export { hash, title, album, artist, imagehash }
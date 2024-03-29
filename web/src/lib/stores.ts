import { writable, type Writable } from 'svelte/store';

const hash: Writable<string> = writable('')
const title: Writable<string> = writable('');
const album: Writable<string> = writable('');
const artist: Writable<string> = writable('');
const imagehash: Writable<string> = writable('');

export { hash, title, album, artist, imagehash }
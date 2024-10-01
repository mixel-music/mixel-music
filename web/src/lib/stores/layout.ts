import { writable, type Writable } from 'svelte/store';

export const isQueueOpen: Writable<boolean> = writable();

import { writable, type Writable } from 'svelte/store';

const isQueueOpen: Writable<boolean> = writable();

export {
  isQueueOpen,
}
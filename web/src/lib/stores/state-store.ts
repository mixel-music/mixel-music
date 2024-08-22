import { writable } from 'svelte/store';

export const stateStore = writable({
  isSeeking: false,
  isUpdated: false,
  isPlaying: false,
  currentTime: 0,
  duration: 0,
  volume: 1.0,
  mute: false,
  loop: 0,
});
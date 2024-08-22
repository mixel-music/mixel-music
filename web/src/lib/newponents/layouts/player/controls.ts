import { trackStore } from '$lib/stores/track-store';
import { stateStore } from "$lib/stores/state-store";

export function playTrack(): void {
  stateStore.update(state => ({
    ...state,
    isPlaying: !state.isPlaying,
  }));
}

export function prevTrack(): void {
  stateStore.update(state => ({
    ...state,
    isUpdated: true,
    currentTime: 0,
  }));
}

export function nextTrack(): void {
  stateStore.update(state => ({
    ...state,
    isUpdated: true,
    currentTime: state.duration,
  }));
}

export function seekTrack(time: number): void {
  stateStore.update(state => ({
    ...state,
    isUpdated: true,
    currentTime: time,
  }));
}

export function initTrack(
  hash: string,
  title: string,
  album: string,
  artist: string,
  albumhash: string,
): void {

  trackStore.update(track => ({
    ...track,
    hash: hash,
    title: title,
    album: album,
    artist: artist,
    albumhash: albumhash,
  }));
}

export function muteTrack(): void {
  let $volume;
  let $mute;

  stateStore.subscribe(value => {
    $volume = value.volume;
    $mute = value.mute;
  });

  if ($volume === 0) {
    stateStore.update(state => ({
      ...state,
      volume: 1.0,
      mute: false,
    }));
  }
  else if ($mute) {
    stateStore.update(state => ({
      ...state,
      mute: false,
    }));
  }
  else {
    stateStore.update(state => ({
      ...state,
      mute: true,
    }));
  }
}

  // export function loopMusic(): void {
  //   if ($trackStore.loop == 0) {
  //     $trackStore.loop = 1;
  //   }
  //   else if ($trackStore.loop == 1) {
  //     $trackStore.loop = 2;
  //     musicItem.loop = true;
  //   }
  //   else {
  //     $trackStore.loop = 0;
  //     musicItem.loop = false;
  //   }
  // }

export function loopTrack(): void {

}
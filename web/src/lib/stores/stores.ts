import { getArtwork } from "$lib/tools";
import { writable, get, derived } from "svelte/store";

interface AudioState {
  isReady: boolean;
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  volume: number;
  mute: boolean;
  loop: number;
}

interface Track {
  hash: string;
  title: string;
  album: string;
  artist: string;
  artwork?: string;
  albumhash: string;
}

interface StoreState extends AudioState, Track {}

function createAudioStore() {
  const initialState: StoreState = {
    hash: '',
    title: '',
    album: '',
    artist: '',
    artwork: '',
    albumhash: '',

    isReady: false,
    isPlaying: false,
    currentTime: 0,
    duration: 0,
    volume: 1.0,
    mute: false,
    loop: 0,
  };

  const { subscribe, update, set } = writable<StoreState>(initialState);
  const audio = new Audio();

  const updateState = () => {
    update(state => ({
      ...state,
      isReady: true,
      isPlaying: !audio.paused,
      currentTime: audio.currentTime,
      duration: audio.duration || 0,
      volume: audio.volume,
      mute: audio.muted,
    }));
  };

  const setTrackInfo = () => {
    if ('mediaSession' in navigator) {
      const { title, album, artist, artwork } = get({ subscribe });
      navigator.mediaSession.metadata = new MediaMetadata({
        title,
        album,
        artist,
        artwork: artwork ? [{ src: artwork }] : [],
      });

      navigator.mediaSession.setActionHandler('play', audioStore.toggle);
      navigator.mediaSession.setActionHandler('pause', audioStore.toggle);
      navigator.mediaSession.setActionHandler('seekbackward', () => { audio.currentTime -= 10; });
      navigator.mediaSession.setActionHandler('seekforward', () => { audio.currentTime += 10; });
      navigator.mediaSession.setActionHandler('previoustrack', audioStore.goPrev);
      navigator.mediaSession.setActionHandler('nexttrack', audioStore.goNext);
    }
  };

  return {
    subscribe,

    setTrack: ({ hash, title, album, artist, albumhash }: Track) => {
      update(state => ({
        ...state,
        hash,
        title,
        album,
        artist,
        albumhash,
        artwork: getArtwork(albumhash, 128),
        isReady: false,
      }));

      if (hash) {
        audio.src = `http://localhost:2843/api/stream/${hash}`;
        audio.load();

        audio.onloadedmetadata = () => {
          audio.play();
          updateState();
          setTrackInfo();
        };

        audio.ontimeupdate = updateState;

        audio.onerror = () => {
          console.error("Failed to load audio.");
          update(state => ({ ...state, isReady: false }));
        };
      }
    },

    toggle: () => {
      if (audio.paused) {
        audio.play();
      } else {
        audio.pause();
      }
      update(state => ({ ...state, isPlaying: !audio.paused }));
    },

    volume: (value: number) => {
      if (audio.muted) {
        audio.muted = false;
      }

      audio.volume = value / 100;
      update(state => ({ ...state, volume: value }));
    },

    seek: (time: number) => {
      audio.currentTime = time;
      update(state => ({ ...state, currentTime: time }));
    },

    mute: () => {
      audio.muted = !audio.muted;
      if (!audio.muted && audio.volume === 0) {
        audio.volume = 1.0;
      }
      update(state => ({ ...state, mute: audio.muted }));
    },

    loop: () => {
      update(state => {
        const newLoop = (state.loop + 1) % 3;
        audio.loop = newLoop === 2;
        return { ...state, loop: newLoop };
      });
    },

    getState: () => get({ subscribe }),
    getCurrentTime: () => get({ subscribe }).currentTime,
    goPrev: () => audio.currentTime = 0,
    goNext: () => audio.currentTime = get({ subscribe }).duration,
    getVolume: () => get({ subscribe }).volume * 100,
  };
}

const audioStore = createAudioStore();
export default audioStore;
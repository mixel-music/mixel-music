import { getArtwork } from "$lib/tools";
import { writable, get } from "svelte/store";
import type { TrackList, StoreState } from "$lib/interface";

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
    volumeRange: 100,
    mute: false,
    loop: 0,

    trackList: [],
    currentTrackIndex: -1,
  };

  const { subscribe, update } = writable<StoreState>(initialState);
  const audio = new Audio();

  const updateState = () => {
    update(state => ({
      ...state,
      isReady: true,
      isPlaying: !audio.paused,
      currentTime: audio.currentTime,
      duration: audio.duration || 0,
      volume: audio.volume,
      volumeRange: audio.volume * 100,
      mute: audio.muted,
    }));
  };

  const updateMetadata = (track: TrackList) => {
    update(state => ({
      ...state,
      hash: track.hash,
      title: track.title,
      album: track.album,
      artist: track.artist,
      albumhash: track.albumhash,
      artwork: track.album == 'Unknown Album' ? getArtwork(track.hash, 128) : getArtwork(track.albumhash, 128),
    }));
  };

  const setTrackInfo = (track: TrackList) => {
    if ('mediaSession' in navigator) {
      navigator.mediaSession.metadata = new MediaMetadata({
        title: track.title,
        album: track.album,
        artist: track.artist,
        artwork: track.artwork ? [{ src: track.artwork }] : [],
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

    addTrack: (track: TrackList, index?: number) => {
      update(state => {
        const updatedTrackList = [...state.trackList];

        if (typeof index === 'number' && index >= 0 && index <= updatedTrackList.length) {
          updatedTrackList.splice(index, 0, track);
        } else {
          updatedTrackList.push(track);
        }

        return { ...state, trackList: updatedTrackList };
      });
    },

    setTrack: (index: number) => {
      update(state => {
        const track = state.trackList[index];

        if (track) {
          audio.src = `http://localhost:2843/api/stream/${track.hash}`;
          audio.load();

          audio.onloadedmetadata = () => {
            audio.play();
            updateState();
            updateMetadata(track);
            setTrackInfo(track);
          };

          audio.ontimeupdate = updateState;

          audio.onerror = () => {
            console.error("Failed to load audio.");
            update(state => ({ ...state, isReady: false }));
          };

          return {
            ...state,
            currentTrackIndex: index,
            ...track,
            artwork: getArtwork(track.albumhash, 128),
          };
        }

        return state;
      });
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
      update(state => ({ ...state, volume: value, volumeRange: value }));
    },

    seek: (time: number) => {
      audio.currentTime = time;
      update(state => ({ ...state, currentTime: time }));
    },

    mute: () => {
      if (!audio.muted && audio.volume === 0) {
        audio.volume = 1.0;
        update(state => ({ ...state, volume: 1.0, volumeRange: 100 }));
      }
      else {
        audio.muted = !audio.muted;
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

    goPrev: () => {
      update(state => {
        const newIndex = state.currentTrackIndex > 0 ? state.currentTrackIndex - 1 : 0;
        audio.currentTime = 0;

        if (newIndex !== state.currentTrackIndex) {
          audioStore.setTrack(newIndex);
        }

        return state;
      });
    },

    goNext: () => {
      update(state => {
        const newIndex = state.currentTrackIndex < state.trackList.length - 1
          ? state.currentTrackIndex + 1
          : state.currentTrackIndex;

        if (newIndex !== state.currentTrackIndex && newIndex < state.trackList.length) {
          audioStore.setTrack(newIndex);
        }

        return state;
      });
    },

    getState: () => get({ subscribe }),
    getCurrentTime: () => get({ subscribe }).currentTime,
  };
}

const audioStore = createAudioStore();
export default audioStore;
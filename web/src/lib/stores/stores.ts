import { getArtwork } from "$lib/tools";
import { writable, get } from "svelte/store";
import type { PlayerStore, TrackList } from "$lib/interface";

function InitPlayerService() {
  const DefaultValues: PlayerStore = {
    track_id: '',
    title: '',
    album: '',
    artist: '',
    artwork: '',
    artist_id: '',
    album_id: '',
    isLoaded: false,
    isPlaying: false,
    volumeRange: 100,
    currentTime: 0,
    duration: 0,
    volume: 1.0,
    mute: false,
    loop: 0,
    lists: [],
    index: 0,
  }

  const { subscribe, update } = writable<PlayerStore>(DefaultValues);
  const audio: HTMLAudioElement = new Audio();

  const updateState = () => {
    update(state => ({
      ...state,
      isLoaded: true,
      isPlaying: !audio.paused,
      currentTime: audio.currentTime,
      duration: audio.duration || 0,
      volume: audio.volume,
      mute: audio.muted,
    }));

    if (audio.currentTime >= audio.duration) {
      let stats = PlayerService.getState();

      if (stats.lists[stats.index + 1]) {
        PlayerService.setTrack(stats.index + 1);
        console.log("stats.index found");
      }
      else if (stats.loop === 1) {
        PlayerService.setTrack(0);
        console.log("go to first");
      }
    }
  };

  const updateTrack = (track: TrackList) => {
    update(state => ({
      ...state,
      track_id: track.track_id,
      title: track.title,
      album: track.album,
      artist: track.artist,
      artist_id: track.artist_id,
      album_id: track.album_id,
      artwork: getArtwork(track.album_id, 128),
    }));
  };

  const SetMediaInfo = () => {
    if ('mediaSession' in navigator) {
      let track: PlayerStore = get({ subscribe });

      navigator.mediaSession.metadata = new MediaMetadata({
        title: track.title,
        album: track.album,
        artist: track.artist,
        artwork: [{ src: track.artwork ? track.artwork : '' }],
      });

      navigator.mediaSession.setActionHandler('play', PlayerService.toggle);
      navigator.mediaSession.setActionHandler('pause', PlayerService.toggle);
      navigator.mediaSession.setActionHandler('seekbackward', () => { audio.currentTime -= 10; });
      navigator.mediaSession.setActionHandler('seekforward', () => { audio.currentTime += 10; });
      navigator.mediaSession.setActionHandler('previoustrack', PlayerService.goPrev);
      navigator.mediaSession.setActionHandler('nexttrack', PlayerService.goNext);
    }
  };

  const addTrack = (track: TrackList, index?: number) => {
    update(state => {
      const newLists = [...state.lists];

      if (typeof index === 'number' && index >= 0 && index <= newLists.length) {
        newLists.splice(index, 0, track);
      }
      else {
        newLists.push(track);
      }

      console.debug(newLists);
      return { ...state, lists: newLists };
    });

    if (PlayerService.getState().lists.length === 1) {
      setTrack(0);
    }
  };

  const setTrack = (index: number) => {
    update(state => {
      const track = state.lists[index];
      console.debug(`setTrack called with ${index}`);

      if (track) {
        audio.src = `http://localhost:2843/api/streaming/${track.track_id}`;
        audio.load();

        audio.onloadedmetadata = (): void => {
          updateState();
          updateTrack(track);
          SetMediaInfo();
          audio.play();
        };

        audio.ontimeupdate = updateState;

        audio.onerror = (): void => {
          console.error("Failed to play track.");
          update(state => ({ ...state, isLoaded: false }));
        };

        return {
          ...state,
          ...track,
          index: index,
          artwork: getArtwork(track.album_id, 128),
        };
      }

      return state;
    });
  };

  return {
    subscribe,
    addTrack,
    setTrack,

    toggle: (): void => {
      if (audio.paused) {
        audio.play();
      }
      else {
        audio.pause();
      }

      update(state => ({ ...state, isPlaying: !audio.paused }));
    },

    volume: (value: number): void => {
      if (audio.muted) {
        audio.muted = false;
      }

      audio.volume = value / 100;
      update(state => ({ ...state, volume: value, volumeRange: value }));
    },
    
    seek: (time: number): void => {
      audio.currentTime = time;
      update(state => ({ ...state, currentTime: time }));
    },

    mute: (): void => {
      if (!audio.muted && audio.volume === 0) {
        audio.volume = 1.0
        update(state => ({ ...state, volume: 1.0, volumeRange: 100 }));
      }
      else {
        audio.muted = !audio.muted;
      }

      update(state => ({ ...state, mute: audio.muted }));
    },

    loop: (): void => {
      update(state => {
        const newLoop = (state.loop + 1) % 3;
        audio.loop = newLoop === 2;

        return {
          ...state,
          loop: newLoop,
        };
      });
    },

    goPrev: (): void => {
      update(state => {
        const newIndex = state.index > 0 ? state.index - 1 : 0;

        if (audio.currentTime < 3) {
          PlayerService.setTrack(newIndex);
        }
        else {
          audio.currentTime = 0;
        }
        
        // if (newIndex !== state.index) {
        //   PlayerService.setTrack(newIndex);
        // }

        return {
          ...state,
          index: newIndex,
        };
      });
    },

    goNext: (): void => {
      update(state => {
        let newIndex = state.index + 1;

        if (state.lists[newIndex]) {
          PlayerService.setTrack(newIndex);
        }
        else if (state.loop === 1) {
          PlayerService.setTrack(0);
          newIndex = 0;
        }

        return {
          ...state,
          index: newIndex,
        };
      });
    },

    getState: () => get({ subscribe }),
    getLists: () => get({ subscribe }).lists,

    destroy: (): void => {
      audio.src = '';
      updateState();
    },
  };
}

const PlayerService = InitPlayerService();
export default PlayerService;
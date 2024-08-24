<script lang="ts">
  import audioElement from "$lib/stores/stores";
  import PlayerButton from '$lib/newponents/layouts/player/player-button.svelte'
  import PlayerNow from '$lib/newponents/layouts/player/player-now.svelte';

  $: trk = $audioElement;
</script>

<div class="player">
  <div class="player-center">
    <div class="player-button">
      <PlayerButton
        alt="Previous"
        on:click={audioElement.goPrev}
        icon="iconoir:skip-prev-solid"
        ControlButton
      />

      <PlayerButton
        on:click={audioElement.toggle}
        alt={trk.isPlaying ? 'Pause' : 'Play'}
        icon={trk.isPlaying ? 'iconoir:pause-solid' : 'iconoir:play-solid'}
        ControlButton
        PrimaryButton
        disabled={!trk.isReady}
      />

      <PlayerButton
        alt="Next"
        on:click={() => console.log('Next track')}
        icon="iconoir:skip-next-solid"
        ControlButton
      />
    </div>

    <input
      type="range"
      min="0"
      max={trk.duration}
      value={trk.currentTime}
      on:input={(e) => audioElement.seek(parseFloat(e.target.value))}
      disabled={!trk.isReady}
    />
  </div>

  <div class="player-area">
    <PlayerNow />
    
    <div class="player-menu">
      <div class="player-volume">
        <!-- <Slider
          bind:value={trk.volume}
          name='volume'
          width='110px'
          max={1.0}
        /> -->
    
        <PlayerButton
          on:click={audioElement.mute}
          alt="Volume"
          icon={trk.volume === 0 || trk.mute
            ? 'iconoir:sound-off' : trk.volume * 100 < 50
            ? 'iconoir:sound-low' : 'iconoir:sound-high'
          }
          off={trk.volume === 0 || trk.mute}
        />
      </div>
    
      <PlayerButton
        on:click={audioElement.loop}
        alt={trk.loop === 2 ? 'Repeat one' : 'Repeat'}
        icon={trk.loop === 1
          ? 'iconoir:repeat' : trk.loop === 2
          ? 'iconoir:repeat-once' : 'iconoir:repeat'
        }
        off={!trk.loop}
      />
    
      <PlayerButton
        alt='Shuffle'
        icon='iconoir:shuffle'
        off
      />
    
      <PlayerButton
        alt='Playlist'
        icon='iconoir:playlist'
      />
    </div>
  </div>
</div>

<style>
  .player {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: fixed;
    bottom: 0;
    z-index: 2;
    width: 100%;
    height: 96px;
    background-color: var(--color-dark-bg-trk);
    box-shadow: 0 0 0 1px var(--color-dark-border) inset;
    backdrop-filter: blur(64px);
  }

  .player-area {
    width: 100%;
    display: flex;
    padding: 0 21px;
    justify-content: space-between;
  }

  .player-center {
    position: fixed;
    left: 50%;
    transform: translate(-50%, 0);
  }

  .player-button {
    display: flex;
    justify-content: center;
    /* padding-top: 3px;
    padding-bottom: 2px; */
    gap: 24px;
    /* margin-bottom: -1px; */
    margin-left: 2px;
  }

  .player-menu {
    display: flex;
    align-items: center;
  }

  .player-volume {
    display: flex;
    align-items: center;
    gap: 4px;
  }
</style>

<!-- <script lang="ts">
  import { onDestroy } from 'svelte';
  import { trackStore, stateStore } from '$lib/stores/stores';
  import Slider from '$lib/newponents/elements/slider.svelte';
  import PlayerButton from './player-button.svelte';
  import PlayerNow from './player-now.svelte';

  let trackElement: HTMLAudioElement = new Audio();
  let value: number = 0;

  $: $trackStore.hash, initTrack();
  $: value = $stateStore.currentTime;

  function initTrack(): void {
    if (trackElement.src) {
      trackElement.removeEventListener('loadedmetadata', handleDataLoaded);
      trackElement.removeEventListener('timeupdate', handleTimeUpdate);
    }

    trackElement.src = `http://localhost:2843/api/stream/${$trackStore.hash}`
    trackElement.addEventListener('loadedmetadata', handleDataLoaded);
    trackElement.addEventListener('timeupdate', handleTimeUpdate);
    setTrackInfo();
  };

  function handleDataLoaded(): void {
    trackElement.play();
    stateStore.update(state => ({...state,
      duration: trackElement.duration,
      isPlaying: true,
    }));
  };

  function handleTimeUpdate(): void {
    stateStore.update(state => ({...state,
      currentTime: trackElement.currentTime,
    }));

    if (trackElement.currentTime >= $stateStore.duration) {
      trackElement.pause();
      stateStore.update(state => ({...state,
        isPlaying: false,
      }));
    }
  };

  function toggleTrack(): void {
    if (trackElement.src) {
      if (trackElement.paused) {
        trackElement.play();
        stateStore.update(state => ({...state,
          isPlaying: true,
        }));
      }
      else {
        trackElement.pause();
        stateStore.update(state => ({...state,
          isPlaying: false,
        }));
      }
    }
  };

  function prevTrack(): void {

  };

  function nextTrack(): void {

  };

  function setTrackInfo(): void {
    if ('mediaSession' in navigator) {
      navigator.mediaSession.metadata = new MediaMetadata({
        title: $trackStore.title,
        album: $trackStore.album,
        artist: $trackStore.artist,
        artwork: [{src: ''}],
      });

      navigator.mediaSession.setActionHandler('play', toggleTrack);
      navigator.mediaSession.setActionHandler('pause', toggleTrack);
      navigator.mediaSession.setActionHandler('seekbackward', () => { trackElement.currentTime -= 10; });
      navigator.mediaSession.setActionHandler('seekforward', () => { trackElement.currentTime += 10; });
      navigator.mediaSession.setActionHandler('previoustrack', prevTrack);
      navigator.mediaSession.setActionHandler('nexttrack', nextTrack);
    }
  }

  onDestroy(() => {
    if (trackElement) {
      trackElement.removeEventListener('loadedmetadata', handleDataLoaded);
      trackElement.removeEventListener('timeupdate', handleTimeUpdate);
      trackElement.src = '';
    }
  });
</script>

<div class="player">
  <div class="player-center">
    <div class="player-button">
      <PlayerButton
        alt="Previous"
        on:click={prevTrack}
        icon="iconoir:skip-prev-solid"
        ControlButton
      />

      <PlayerButton
        on:click={toggleTrack}
        alt={$stateStore.isPlaying ? 'Pause' : 'Play'}
        icon={$stateStore.isPlaying ? 'iconoir:pause-solid' : 'iconoir:play-solid'}
        ControlButton
        PrimaryButton
      />

      <PlayerButton
        alt="Next"
        on:click={nextTrack}
        icon="iconoir:skip-next-solid"
        ControlButton
      />
    </div>

    <Slider
      bind:value={value}
      name="length"
      width="550px"
      max={$stateStore.duration}
    />
  </div>

  <div class="player-area">
    <PlayerNow />
    
    <div class="player-menu">
      <div class="player-volume">
        <Slider
          bind:value={$stateStore.volume}
          name='volume'
          width='110px'
          max={1.0}
        />
    
        <PlayerButton
          on:click
          alt="Volume"
          icon={$stateStore.volume === 0 || $stateStore.mute
            ? 'iconoir:sound-off' : $stateStore.volume * 100 < 50
            ? 'iconoir:sound-low' : 'iconoir:sound-high'
          }
          off={$stateStore.volume === 0 || $stateStore.mute}
        />
      </div>
    
      <PlayerButton
        on:click
        alt={$stateStore.loop === 2 ? 'Repeat one' : 'Repeat'}
        icon={$stateStore.loop === 1
          ? 'iconoir:repeat' : $stateStore.loop === 2
          ? 'iconoir:repeat-once' : 'iconoir:repeat'
        }
        off={!$stateStore.loop}
      />
    
      <PlayerButton
        alt='Shuffle'
        icon='iconoir:shuffle'
        off
      />
    
      <PlayerButton
        alt='Playlist'
        icon='iconoir:playlist'
      />
    </div>
  </div>
</div>

<style>
  .player {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: fixed;
    bottom: 0;
    z-index: 2;
    width: 100%;
    height: 96px;
    background-color: var(--color-dark-bg-trk);
    box-shadow: 0 0 0 1px var(--color-dark-border) inset;
    backdrop-filter: blur(64px);
  }

  .player-area {
    width: 100%;
    display: flex;
    padding: 0 21px;
    justify-content: space-between;
  }

  .player-area-1 {
    display: flex;
    align-items: center;
    gap: var(--app-padding-s);
  }

  .player-area-2 {
    display: flex;
    align-items: center;
  }

  .player-track {
    display: flex;
    flex-direction: column;
    justify-content: space-evenly;
    line-height: 115%;
  }

  .player-center {
    position: fixed;
    left: 50%;
    transform: translate(-50%, 0);
  }

  .player-button {
    display: flex;
    justify-content: center;
    padding: 0 6px;
    padding-top: 3px;
    padding-bottom: 2px;
    gap: 24px;
  }

  .player-menu {
    display: flex;
    align-items: center;
  }

  .player-volume {
    display: flex;
    align-items: center;
    gap: 4px;
  }
</style> -->
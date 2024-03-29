<script lang="ts">
  import {
    onMount,
    onDestroy,
  }
  from "svelte";
  import { hash, title, album, artist, imagehash } from '$lib/stores';

  import IconamoonPlayerPauseFill from '~icons/iconamoon/player-pause-fill';
  import IconamoonPlayerPlayFill from '~icons/iconamoon/player-play-fill';
  import IconamoonPlayerStartFill from '~icons/iconamoon/player-start-fill';
  import IconamoonPlayerEndFill from '~icons/iconamoon/player-end-fill';

  import IconamoonVolumeUp from '~icons/iconamoon/volume-up';
  import IconamoonVolumeDown from '~icons/iconamoon/volume-down';
  import IconamoonVolumeOff from '~icons/iconamoon/volume-off';

  import IconamoonPlaylistRepeatList from '~icons/iconamoon/playlist-repeat-list';
  import IconamoonPlaylistRepeatSong from '~icons/iconamoon/playlist-repeat-song';
  import IconamoonPlaylistShuffle from '~icons/iconamoon/playlist-shuffle';
  import IconamoonPlaylist from '~icons/iconamoon/playlist';

  
  /* slider */

  let isDragging: boolean = false;
  let isDraggingLength: boolean = false;
  let isDraggingVolume: boolean = false;

  function handleSeek(
      event: MouseEvent,
      range: string,
      callback: (value: number) => void
    ): void
  {
    const ctl: HTMLElement = document.querySelector(range);
    const ctlWidth: number = ctl.clientWidth;
    const newValue: number = event.clientX - ctl.getBoundingClientRect().left;
    callback(newValue / ctlWidth);
  }

  function lengthSeek(event: MouseEvent): void {
    handleSeek(event, '.player-length-ctl', (value: number) => {
      console.log("test");
    });
  }

  function volumeSeek(event: MouseEvent): void {
    handleSeek(event, '.player-volume-ctl', (value: number) => {
      console.log("volume");
    });
  }

  function seekEvent(event: MouseEvent, type: 'length' | 'volume'): void {
    isDragging = true;
    isDraggingLength = type === 'length';
    isDraggingVolume = type === 'volume';
    const handleMove: (event: MouseEvent) => void = type === 'length' ? lengthSeek : volumeSeek;
    document.addEventListener('mousemove', handleMove);
    document.addEventListener('mouseup', seekEventStop)
  }

  function seekEventStop(): void {
    isDragging = false;
    isDraggingLength = false;
    isDraggingVolume = false;
    document.removeEventListener('mousemove', lengthSeek);
    document.removeEventListener('mousemove', volumeSeek);
    document.removeEventListener('mouseup', seekEventStop);
  }


  /* player */

  let handlePlay: HTMLAudioElement = new Audio();
  let isPlaying: boolean = false;
  let imagepath: string = '';

  let duration: string | number = '';
  let length : string | number = ''
  let lengthWidth: number = 0;
  let volumeWidth: number = 0;

  function toggleTrack(): void {
    if (isPlaying) {
      isPlaying = false;
    }
    else if (!isPlaying && duration) {
      isPlaying = true;
    }
  }

  $: if (handlePlay) {
    handlePlay.src = `http://localhost:2843/api/stream/${$hash}`;
    imagepath = `http://localhost:2843/api/images/${$imagehash}`;

    handlePlay.addEventListener('loadedmetadata', () => {
      duration = formatTime(handlePlay.duration);
      isPlaying = true;
    });
  }

  $: if (isPlaying) {
    handlePlay.play();
  } else {
    handlePlay.pause();
  }

  /* tools */

  function formatTime(time: number): string {
    const min = Math.floor(time / 60);
    const sec = Math.floor(time % 60);

    return `${min}:${sec < 10 ? '0' : ''}${sec}`;
  }

  handlePlay.addEventListener('timeupdate', () => {
    length = formatTime(handlePlay.currentTime);
    lengthWidth = (handlePlay.currentTime / handlePlay.duration) * 100;
    volumeWidth = Math.floor(handlePlay.volume * 100);
  });

  onMount(() => {
    return () => {
      handlePlay.removeEventListener('loadedmetadata', () => {
        duration = handlePlay.duration;
      });
    };
  });

  onDestroy(() => {
    return () => {
      handlePlay.removeEventListener('timeupdate', updateLength);
    }
  })

  function updateLength() {
    length = formatTime(handlePlay.currentTime);
  }
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<div class="player">
  <div
    class="player-length"
    on:mousedown="{
      event => seekEvent(event, 'length')
    }"
  >
    <div class="player-length-ctl">
      <div
        class="player-length-ctl__now"
        style="width: {lengthWidth}%;"
      >
      </div>
    </div>
  </div>
  <div class="player-area">
    <div class="player-area-1">
      <img
        src="{imagepath}"
        class="player-area-1-img"
        alt="Front Cover">
      <div class="player-area-1-trk">
        <span class="text-title">{$title ? $title : ''}</span>
        <span class="text-description">{$artist ? $artist : ''}</span>
        <span class="text-description">{length} / {duration}</span>
      </div>
    </div>
    <div class="player-area-2">
      <button class="player-area-btn" title="Previous">
        <IconamoonPlayerStartFill />
      </button>
      <button
        class="player-area-btn btn-primary"
        on:click="{toggleTrack}"
      >
        {#if isPlaying}
          <IconamoonPlayerPauseFill />
        {:else}
          <IconamoonPlayerPlayFill />
        {/if}
      </button>
      <button class="player-area-btn" title="Next">
        <IconamoonPlayerEndFill />
      </button>
    </div>
    <div class="player-area-3">
      <div
        class="player-volume"
        on:mousedown="{
          event => seekEvent(event, 'volume')
        }"
      >
        <div class="player-volume-ctl">
          <div
            class="player-volume-ctl__now"
            style="width: {volumeWidth}%;"
          >
          </div>
        </div>
        <button class="player-side-btn" title="Volume">
          <IconamoonVolumeUp />
        </button>
      </div>
      <button class="player-side-btn" title="Repeat">
        <IconamoonPlaylistRepeatList />
      </button>
      <button class="player-side-btn" title="Shuffle">
        <IconamoonPlaylistShuffle />
      </button>
      <button class="player-side-btn" title="Playlist">
        <IconamoonPlaylist />
      </button>
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
  width: -webkit-fill-available;
  height: 96px;
  padding: 0 16px;
  background-color: var(--color-dark-trk);
  backdrop-filter: blur(32px);
}

.player-area {
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.player-area-1 {
  display: flex;
  align-items: center;
  height: -webkit-fill-available;
}

.player-area-1-img {
  width: 58px;
  height: 58px;
  object-fit: scale-down;
  margin-right: var(--app-padding-s);
  background-color: var(--color-dark-bg-2);
  box-shadow: 0 0 0 1px var(--color-dark-border) inset;
  border-radius: var(--app-radius);
  cursor: pointer;
}

.player-area-1-trk {
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  line-height: 120%;
}

.player-area-2 {
  display: flex;
  position: fixed;
  left: 50%;
  transform: translate(-50%, 0);
  height: 58px;
}

.player-area-btn {
  display: flex;
  padding: 12px;
  border: none;
  background-color: transparent;
  color: var(--color-dark-text-1);
  font-size: 20px;
  cursor: pointer;
  transition: 0.2s ease;
  align-items: center;
  justify-content: center;
}

.player-area-btn:focus {
  outline: none;
}

.player-area-btn:hover {
  color: var(--color-dark-focus);
  transition: all 0.1s ease;
}

.btn-primary {
  font-size: 28px;
  margin: 0 10px;
}

.player-area-3 {
  display: flex;
  align-items: center;
}

.player-side-btn {
  display: flex;
  padding: 12px;
  border: none;
  background-color: transparent;
  color: var(--color-dark-text-1);
  font-size: 18px;
  cursor: pointer;
  transition: 0.2s ease;
  align-items: center;
  justify-content: center;
}

.player-length {
  height: 3px;
  background-color: var(--color-dark-trk-len);
  border-radius: var(--app-radius);
  position: fixed;
  left: 0;
  bottom: 93px;
  width: 100%;
}

.player-length-ctl {
  padding-bottom: 12px;
  cursor: pointer;
}

.player-length-ctl__now {
  width: 0;
  height: 3px;
  background-color: var(--color-dark-trk-now);
  border-radius: var(--app-radius);
}

.player-volume {
  display: flex;
  align-items: center;
}

.player-volume-ctl {
  width: 100px;
  height: 3px;
  cursor: pointer;
  padding: 12px;
  background-color: var(--color-dark-trk-len);
  border-radius: var(--app-radius);
  background-clip: content-box;
}

.player-volume-ctl__now {
  width: 30px;
  height: 3px;
  background-color: var(--color-dark-trk-now);
  border-radius: var(--app-radius);
}
</style>
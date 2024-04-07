<script lang="ts">
  import { onDestroy } from "svelte";
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
  import Page from "../../routes/+page.svelte";

  let audioItem: HTMLAudioElement = new Audio();
  let imagepath: string = "";

  let durationTime: number = 0;
  let currentTime: number = 0;
  let durationString: string = formatTime(0);
  let currentString: string = formatTime(0);
  let currentBar: number = 0;
  let volumeBar: number = 100;

  let isPlaying: boolean = false;
  let isDraggingLength: boolean = false;
  let isDraggingVolume: boolean = false;
  let isRepeatTrack: number = 0;

  $: $hash, loadAudio();

  function handlePlay(): void {
    if (audioItem.paused) {
      audioItem.play();
      isPlaying = true;
    }
    else {
      audioItem.pause();
      isPlaying = false;
    }
  }

  function previousPlay(): void {
    audioItem.currentTime = 0;
  }

  function loadAudio() {
    audioItem.src = (`http://localhost:2843/api/stream/${$hash}`);
    imagepath = `http://localhost:2843/api/images/${$imagehash}`;
    audioItem.volume = volumeBar / 100;

    audioItem.addEventListener("loadedmetadata", () => {
      durationTime = audioItem.duration;
      durationString = formatTime(audioItem.duration);
      currentString = formatTime(audioItem.currentTime);

      audioItem.play();
      isPlaying = true;
      setMediaControls();
    });

    audioItem.addEventListener("timeupdate", () => {
      if (!isDraggingLength) {
        currentTime = audioItem.currentTime;
        currentString = formatTime(currentTime);
        currentBar = (currentTime / durationTime) * 100;
      }

      if (audioItem.currentTime === audioItem.duration) {
        isPlaying = false;
        audioItem.pause();
        setMediaControls();
      }
    });

    // audioItem.addEventListener("error", () => {
    //   console.error("Failed to load track");
    // });
  }

  function setMediaControls(): void {
    if ('mediaSession' in navigator) {
      navigator.mediaSession.metadata = new MediaMetadata({
        title: $title,
        album: $album,
        artist: $artist,
        artwork: [
          {
            src: imagepath + "?size=300",
          }  
        ],
      });

      navigator.mediaSession.setActionHandler("play", () => { handlePlay(); });
      navigator.mediaSession.setActionHandler("pause", () => { handlePlay(); });
      navigator.mediaSession.setActionHandler("seekbackward", () => { audioItem.currentTime -= 10; });
      navigator.mediaSession.setActionHandler("seekforward", () => { audioItem.currentTime += 10; });
      navigator.mediaSession.setActionHandler("previoustrack", () => { previousPlay(); });
      navigator.mediaSession.setActionHandler("nexttrack", () => { console.log("test") });
    }
  }

  function handleSeek(event: MouseEvent, eventClass: string, callback: (value: number) => void): void {
    event.preventDefault();

    const ctl = document.querySelector(eventClass);
    if (ctl) {
      const ctlWidth = ctl.clientWidth;
      const ctlRect = ctl.getBoundingClientRect();
      const newValue = Math.max(0, Math.min(event.clientX - ctlRect.left, ctlWidth));
      const newValueCalc = newValue / ctlWidth;
      callback(newValueCalc);
    }
  }

  function lengthSeek(event: MouseEvent): void {
    handleSeek(event, '.player-length-ctl', (value) => {
      if (audioItem) {
        currentTime = value * durationTime;
        currentString = formatTime(currentTime);
        currentBar = value * 100;
        if (!isDraggingLength) {
          audioItem.currentTime = currentTime;
        }
      }
    });
  }

  function volumeSeek(event: MouseEvent): void {
    handleSeek(event, '.player-volume-ctl', (value) => {
      volumeBar = value * 100;
      if (audioItem) {
        audioItem.volume = value;
      }
    });
  }

  function handleDragStart(event: MouseEvent, type: "length" | "volume"): void {
    event.preventDefault();
    if (type === "length") {
      isDraggingLength = true;
    } else {
      isDraggingVolume = true;
    }
    const handleMove = type === "length" ? lengthSeek : volumeSeek;
    const handleEnd = () => {
      if (type === "length") {
        isDraggingLength = false;
        if (audioItem) {
          audioItem.currentTime = currentTime;
        }
      } else {
        isDraggingVolume = false;
      }
      document.removeEventListener("mousemove", handleMove);
      document.removeEventListener("mouseup", handleEnd);
    };
    document.addEventListener("mousemove", handleMove);
    document.addEventListener("mouseup", handleEnd);
    handleMove(event);
  }

  function formatTime(time: number): string {
    const min = Math.floor(time / 60);
    const sec = Math.floor(time % 60);
    return `${min}:${sec < 10 ? "0" : ""}${sec}`;
  }

  function muteVolume(): void {
    if (audioItem.volume === 0) {
      audioItem.volume = 1;
      audioItem.muted = false;
      volumeBar = 100;
    }
    else if (!audioItem.muted) {
      audioItem.muted = true;
    }
    else {
      audioItem.muted = false;
    }
  }

  function repeatTrack(): void {
    if (isRepeatTrack === 0) {
      isRepeatTrack = 1;
      audioItem.loop = true;
    }
    else if (isRepeatTrack === 1) {
      isRepeatTrack = 2;
      audioItem.loop = true;
    }
    else {
      isRepeatTrack = 0;
      audioItem.loop = false;
    }
  }

  onDestroy(() => {
    if (audioItem) {
      audioItem.src = '';
    }
  });
</script>

<!-- svelte-ignore a11y-click-events-have-key-events -->
<div class="player">

  <div class="player-center">
    <div class="player-center-ctl">
      <button
        class="player-center-btn"
        on:click={previousPlay}
        title="Previous"
      >
        <IconamoonPlayerStartFill />
      </button>
      {#if $hash}
        <button
          class="player-center-btn btn__primary"
          on:click={handlePlay}
        >
          {#if isPlaying}
            <IconamoonPlayerPauseFill />
          {:else}
            <IconamoonPlayerPlayFill />
          {/if}
        </button>
      {:else}
        <button class="player-center-btn btn__primary">
          <IconamoonPlayerPlayFill />
        </button>
      {/if}
      <button class="player-center-btn" title="Next">
        <IconamoonPlayerEndFill />
      </button>
    </div>
    <div
      tabindex=0
      role="slider"
      class="player-length"
      on:click={(event) => lengthSeek(event)}
      on:mousedown={(event) => handleDragStart(event, "length")}
    >
      <div class="player-length-ctl">
        <div
          class="player-length-ctl__now"
          style="width: {currentBar}%;"
        />
      </div>
    </div>

  </div>

  <div class="player-area">
    <div class="player-area-1">
      {#if $hash}
        <img
          src="{imagepath}?size=128"
          class="player-area-1-img"
          alt="Front Cover"
        />
        <div class="player-area-1-trk">
          <span class="text-title">
            {$title ? $title : ""}
          </span>
          <span class="text-description">
            {$artist ? $artist : ""} - {$album ? $album : ""}
          </span>
          <span class="text-description">
            {currentString} / {durationString}
          </span>
        </div>
      {/if}
    </div>

    <div class="player-area-2">
      <div class="player-volume">
        {#key muteVolume}
          <div
            tabindex=0
            role="slider"
            class="player-volume-ctl"
            on:click={(event) => volumeSeek(event)}
            on:mousedown={(event) => handleDragStart(event, "volume")}  
          >
            <div
              class="player-volume-ctl__now"
              style="width: {audioItem.muted ? 0 : volumeBar}%;"
            />
          </div>
          <button
            class="player-side-btn"
            title="Volume"
            on:click={muteVolume}
          >
            {#if volumeBar === 0 || audioItem.muted}
              <IconamoonVolumeOff />
            {:else if volumeBar < 50}
              <IconamoonVolumeDown />
            {:else}
              <IconamoonVolumeUp />
            {/if}
          </button>
        {/key}
      </div>
      <button
        class="player-side-btn { isRepeatTrack == 0 ? 'btn__disabled' : ''}"
        title={isRepeatTrack == 2 ? 'Repeat one' : 'Repeat'}
        on:click={repeatTrack}
      >
        {#if isRepeatTrack === 1}
          <IconamoonPlaylistRepeatList />
        {:else if isRepeatTrack === 2}
          <IconamoonPlaylistRepeatSong />
        {:else}
          <IconamoonPlaylistRepeatList />
        {/if}
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
  z-index: 2;
  width: 100%;
  height: 96px;
  background-color: var(--color-dark-trk);
  backdrop-filter: blur(64px);
  user-select: none;
  border-top: 1px solid var(--color-dark-border);
  box-shadow: 0 0 0 1px var(--color-dark-border) inset;
}

.player-center {
  display: flex;
  position: fixed;
  left: 50%;
  transform: translate(-50%, 0);
  justify-content: center;
  flex-direction: column;
  height: 96px;
}

.player-center-ctl {
  display: flex;
  justify-content: center;
}

.player-center-btn {
  display: flex;
  padding: 0 12px;
  border: none;
  background-color: transparent;
  color: var(--color-dark-text-1);
  font-size: 20px;
  cursor: pointer;
  transition: 0.2s ease;
  align-items: center;
  justify-content: center;
}

.player-center-btn:focus {
  outline: none;
}

.player-center-btn:hover {
  color: var(--color-dark-focus);
  transition: all 0.1s ease;
}

.player-area {
  width: 100%;
  display: flex;
  padding: 0 16px;
  justify-content: space-between;
}

.player-area-1 {
  display: flex;
  align-items: center;
  gap: var(--app-padding-s);
}

.player-area-1-img {
  width: 56px;
  height: 56px;
  object-fit: scale-down;
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
  width: 100%;
  height: 3px;
  cursor: pointer;
  padding: 12px;
  border-radius: var(--app-radius);
}

.player-length-ctl {
  width: 600px;
  background-color: var(--color-dark-trk-len);
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
  border-radius: var(--app-radius);
}

.player-volume-ctl {
  width: 128px;
  cursor: pointer;
  padding: 6px;
  background-color: var(--color-dark-trk-len);
  border-radius: var(--app-radius);
  background-clip: content-box;
}

.player-volume-ctl__now {
  height: 3px;
  background-color: var(--color-dark-trk-now);
  border-radius: var(--app-radius);
}

.btn__primary {
  font-size: 28px;
  margin: 0 10px;
}

.btn__disabled {
  color: var(--color-dark-disabled);
}
</style>
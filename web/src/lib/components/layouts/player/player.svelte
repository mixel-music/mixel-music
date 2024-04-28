<script lang="ts">
  import { onDestroy } from "svelte";
  import { hash, title, album, artist, imagehash } from '$lib/stores';

  import ContentHead from '$lib/components/elements/content-head.svelte';
  import ContentBody from '$lib/components/elements/content-body.svelte';
  import PlayerButton from './player-button.svelte';
  import PlayerSlider from './player-slider.svelte';

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

  $: $title, loadAudio();

  function handlePlay(): void {
    if ($hash !== undefined) {
      if (audioItem.paused) {
        audioItem.play();
        isPlaying = true;
      }
      else {
        audioItem.pause();
        isPlaying = false;
      }
    }
  }

  function previousPlay(): void {
    audioItem.currentTime = 0;
  }

  function loadAudio() {
    if ($hash !== undefined) {
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
    }

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
    handleSeek(event, '.length-ctl', (value) => {
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
    handleSeek(event, '.volume-ctl', (value) => {
      volumeBar = value * 100;
      if (audioItem) {
        audioItem.volume = value;
      }
    });
  }

  function handleDragStart(event: MouseEvent, type: 'length' | 'volume'): void {
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

<div class="player">
  <div class="player-center">
    <div class="player-center-ctl">

      <PlayerButton
        title='Previous'
        on:click={previousPlay}
        icon='iconoir:skip-prev-solid'
        control_button
      />

      <PlayerButton
        title={isPlaying ? 'Pause' : 'Play'}
        on:click={handlePlay}
        icon={isPlaying ? 'iconoir:pause-solid' : 'iconoir:play-solid'}
        control_button
        primary_button
      />

      <PlayerButton
        title='Next'
        on:click={undefined}
        icon='iconoir:skip-next-solid'
        control_button
      />

    </div>

    <PlayerSlider
      width='550px'
      value={currentBar}
      unique='length-ctl'
      on:click={(event) => lengthSeek(event)}
      on:mousedown={(event => handleDragStart(event, 'length'))}  
    />

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
          <ContentHead head='{$title ? $title : ""}' />
          <ContentBody body='{$artist ? $artist : ""} - {$album ? $album : ""}' />
          <ContentBody body='{ currentString } / { durationString }' />
        </div>
      {/if}

    </div>

    <div class="player-area-2">
      <div class="player-volume">

        {#key muteVolume}
          <PlayerSlider
            width='110px'
            unique='volume-ctl'
            value={audioItem.muted ? 0 : volumeBar}
            on:click={(event) => volumeSeek(event)}
            on:mousedown={(event) => handleDragStart(event, "volume")}  
          />

          <PlayerButton
            title="Volume"
            on:click={muteVolume}
            turn_off={volumeBar === 0 || audioItem.muted ? true : false}
            icon={
              volumeBar === 0 || audioItem.muted ? 'iconoir:sound-off' :
                volumeBar < 50 ? 'iconoir:sound-low' : 'iconoir-sound-high'
            }
          />
        {/key}

      </div>

      <PlayerButton
        title={
          isRepeatTrack == 2 ? 'Repeat one' : 'Repeat'
        }
        icon={
          isRepeatTrack === 1 ? 'iconoir:repeat' :
            isRepeatTrack === 2 ? 'iconoir-repeat-once' : 'iconoir-repeat'
        }
        turn_off={isRepeatTrack !== 0 ? false : true}
        on:click={repeatTrack}
      />

      <PlayerButton
        title='Shuffle'
        icon='iconoir:shuffle'
        turn_off
      />

      <PlayerButton
        title='Playlist'
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
    backdrop-filter: blur(64px);
    user-select: none;
    border-top: 1px solid var(--color-dark-border);
    box-shadow: 0 0 0 1px var(--color-dark-border) inset;
  }

  .player-center {
    position: fixed;
    left: 50%;
    transform: translate(-50%, 0);
  }

  .player-center-ctl {
    display: flex;
    justify-content: center;
    padding: 4px 8px;
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

  .player-volume {
    display: flex;
    align-items: center;
  }
</style>
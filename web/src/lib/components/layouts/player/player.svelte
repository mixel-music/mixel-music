<script lang="ts">
  import { onDestroy } from "svelte";

  import {
    getCoverUrl,
    getFormattedTime,
  } from "$lib/tools";

  import {
    trackHash,
    trackTitle,
    trackAlbum,
    trackArtist
  } from '$lib/stores/track';

  import ContentHead from '$lib/components/elements/content-head.svelte';
  import ContentBody from '$lib/components/elements/content-body.svelte';
  import PlayerButton from './player-button.svelte';
  import PlayerSlider from './player-slider.svelte';

  let musicItem: HTMLAudioElement = new Audio();
  let coverPath: string = getCoverUrl('');
  let current: number = 0;
  let length: number = 0;

  let lengthBar: number = 0;
  let volumeBar: number = 100;
  let isPlay: boolean = false;
  let isDrag: boolean = false;
  let isLoop: number = 0;

  $: $trackHash, StreamMusic(), SetMusicInfo();
  $: musicItem.volume, volumeBar = musicItem.volume * 100;

  function StreamMusic(): void {
    if ($trackHash !== undefined) {
      musicItem.src = (`http://localhost:2843/api/stream/${ $trackHash }`);
      coverPath = getCoverUrl($trackHash);
      
      musicItem.addEventListener("loadedmetadata", () => {
        length = musicItem.duration;
        musicItem.play();
        isPlay = true;
      });

      musicItem.addEventListener("timeupdate", () => {
        current = musicItem.currentTime;
        if (!isDrag) lengthBar = (current / length) * 100;

        if (musicItem.currentTime == musicItem.duration) {
          musicItem.pause();
          isPlay = false;
        }
      });
    }
  }

  function ToggleMusic(): void {
    if ($trackHash) {
      if (musicItem.paused) {
        musicItem.play();
        isPlay = true;
      } else {
        musicItem.pause();
        isPlay = false;
      }
    }
  }

  function PlayPrev(): void {
    musicItem.currentTime = 0;
  }

  function PlayNext(): void {
    console.debug("PlayNext Called");
  }

  function SetMusicInfo(): void {
    if ('mediaSession' in navigator) {
      navigator.mediaSession.metadata = new MediaMetadata({
        title: $trackTitle,
        album: $trackAlbum,
        artist: $trackArtist,
        artwork: [
          {
            src: getCoverUrl($trackHash, 128),
          }
        ],
      });

      navigator.mediaSession.setActionHandler("play", () => { ToggleMusic(); });
      navigator.mediaSession.setActionHandler("pause", () => { ToggleMusic(); });
      navigator.mediaSession.setActionHandler("seekbackward", () => { musicItem.currentTime -= 10; });
      navigator.mediaSession.setActionHandler("seekforward", () => { musicItem.currentTime += 10; });
      navigator.mediaSession.setActionHandler("previoustrack", () => { PlayPrev(); });
      navigator.mediaSession.setActionHandler("nexttrack", () => { PlayNext(); });
    }
  }

  function SeekHandler(
    event: MouseEvent,
    type: string,
    callback: (value: number) => void
  ): void {

    event.preventDefault();
    const ctl = document.querySelector(type);
    
    if (ctl) {
      const ctlWidth = ctl.clientWidth;
      const ctlBound = ctl.getBoundingClientRect();
      const newValue = Math.max(0, Math.min(event.clientX - ctlBound.left, ctlWidth));

      callback(newValue / ctlWidth);
    }
  }

  function DragHandler(
    event: MouseEvent,
    type: 'length' | 'volume'
  ): void {
    
    isDrag = true;
    event.preventDefault();
    
    const MoveHandler = type === 'length' ? SeekLength : SeekVolume;
    const PostHandler = () => {
      document.removeEventListener("mousemove", MoveHandler);
      document.removeEventListener("mouseup", PostHandler);

      if (type === 'length' && musicItem) {
        musicItem.currentTime = current;
      }

      isDrag = false;
    };

    document.addEventListener("mousemove", MoveHandler);
    document.addEventListener("mouseup", PostHandler);
    MoveHandler(event);
  }

  function SeekLength(event: MouseEvent): void {
    SeekHandler(event, '.length-ctl', (value) => {
      if (musicItem && $trackHash) {
        current = value * length;
        lengthBar = value * 100;

        if (!isDrag) {
          musicItem.currentTime = current;
        }
      }
    });
  }

  function SeekVolume(event: MouseEvent): void {
    SeekHandler(event, '.volume-ctl', (value) => {
      if (musicItem) {
        musicItem.muted = false;
        musicItem.volume = value;
      }
    });
  }

  function MuteMusic(): void {
    if (musicItem.volume === 0) {
      musicItem.volume = 1;
      musicItem.muted = false;
    }
    else if (!musicItem.muted) {
      musicItem.muted = true;
    }
    else {
      musicItem.muted = false;
    }
  }

  function LoopMusic(): void {
    if (isLoop === 0) {
      isLoop = 1;
      musicItem.loop = true;
    }
    else if (isLoop === 1) {
      isLoop = 2;
      musicItem.loop = true;
    }
    else {
      isLoop = 0;
      musicItem.loop = false;
    }
  }

  onDestroy(() => {
    if (musicItem) {
      musicItem.src = '';
    }
  });
</script>

<div class="player">
  <div class="player-center">
    <div class="player-button">

      {#key isPlay}
        <PlayerButton
          title='Previous'
          on:click={ PlayPrev }
          icon='iconoir:skip-prev-solid'
          ControlButton
        />

        <PlayerButton
          title={ isPlay ? 'Pause' : 'Play' }
          on:click={ ToggleMusic }
          icon={ isPlay ? 'iconoir:pause-solid' : 'iconoir:play-solid' }
          ControlButton
          PrimaryButton
        />

        <PlayerButton
          title='Next'
          on:click={ PlayNext }
          icon='iconoir:skip-next-solid'
          ControlButton
        />
      {/key}

    </div>

    <PlayerSlider
      width='550px'
      value={ lengthBar }
      unique='length-ctl'
      on:click={(event) => SeekLength(event)}
      on:mousedown={(event => DragHandler(event, 'length'))}
    />

  </div>

  <div class="player-area">
    <div class="player-area-1">

      {#if $trackHash}
        <img
          src="{ coverPath }?size=128"
          class="player-cover"
          alt="Front Cover"
        />

        <div class="player-track">
          <ContentHead head='{ $trackTitle ? $trackTitle : "" }' />
          <ContentBody body='{ $trackArtist } - { $trackAlbum }' />
          <ContentBody body='{ getFormattedTime(current) } / { getFormattedTime(length) }' />
        </div>
      {/if}

    </div>

    <div class="player-area-2">
      <div class="player-volume">

        {#key MuteMusic}
          <PlayerSlider
            width='110px'
            unique='volume-ctl'
            value={ musicItem.muted ? 0 : volumeBar }
            on:click={(event) => SeekVolume(event)}
            on:mousedown={(event) => DragHandler(event, "volume")}  
          />

          <PlayerButton
            title="Volume"
            on:click={ MuteMusic }
            TurnOff={ volumeBar === 0 || musicItem.muted ? true : false }
            icon={
              volumeBar === 0 || musicItem.muted ? 'iconoir:sound-off' :
                volumeBar < 50 ? 'iconoir:sound-low' : 'iconoir-sound-high'
            }
          />
        {/key}

      </div>

      <PlayerButton
        title={
          isLoop == 2 ? 'Repeat one' : 'Repeat'
        }
        icon={
          isLoop === 1 ? 'iconoir:repeat' :
            isLoop === 2 ? 'iconoir-repeat-once' : 'iconoir-repeat'
        }
        TurnOff={ !isLoop }
        on:click={ LoopMusic }
      />

      <PlayerButton
        title='Shuffle'
        icon='iconoir:shuffle'
        TurnOff
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
    border-top: 1px solid var(--color-dark-border);
    box-shadow: 0 0 0 1px var(--color-dark-border) inset;
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

  .player-cover {
    width: 56px;
    height: 56px;
    object-fit: scale-down;
    background-color: var(--color-dark-bg-2);
    box-shadow: 0 0 0 1px var(--color-dark-border) inset;
    border-radius: var(--app-radius);
    cursor: pointer;
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

  .player-volume {
    display: flex;
    align-items: center;
    gap: 4px;
  }
</style>
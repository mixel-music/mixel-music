<script lang="ts">
  import { onMount, onDestroy } from "svelte";

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

  let MusicHandler: HTMLAudioElement = new Audio();
  let IsPlaying: boolean = false;
  let IsRepeat: boolean = false; 
  let TrackInfo: string = '';
  let TrackLength: number = 0;
  let TrackCurrent: number = 0;
  let VolumeValue: number = 0;

  function SelectTrack(title: string, album: string, artist: string, path: string) {
    let TrackTitle: string = title;
    let TrackAlbum: string = album;
    let TrackArtist: string = artist;
    let TrackPath: string = path;
    MusicHandler.src = path;

    if (MusicHandler.paused) {
      MusicHandler.play();
      IsPlaying = true;
      document.title = title + ' - mixel-music';
    }
  }
</script>

<div class="player">
  <div class="player-seek">
    <div class="player-seek-ctl">
      <div class="player-seek-ctl__now"></div>
    </div>
  </div>
  <div class="player-area">
    <div class="player-area-1">
      <img
        src="http://localhost:2843/api/images/a2211d43e8149d87a7642dd48c36eb7426d4a9fb?size=128"
        class="player-area-1-img"
        alt="Front Cover">
      <div class="player-area-1-trk">
        <span class="text-title">Test</span>
        <span class="text-description">Description</span>
        <span class="text-description">Length</span>
      </div>
    </div>
    <div class="player-area-2">
      <button class="player-area-btn" title="Previous">
        <IconamoonPlayerStartFill />
      </button>
      <button class="player-area-btn btn-primary">
        {#if IsPlaying}
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
      <div class="player-volume">
        <div class="player-volume-ctl">
          <div class="player-volume-ctl__now"></div>
        </div>
        <button class="player-area-btn" title="Previous">
          <IconamoonVolumeUp />
        </button>
      </div>
      <button class="player-area-btn" title="Previous">
        <IconamoonPlaylistRepeatList />
      </button>
      <button class="player-area-btn" title="Previous">
        <IconamoonPlaylistShuffle />
      </button>
      <button class="player-area-btn" title="Previous">
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

.player-seek {
  height: 3px;
  background-color: var(--color-dark-trk-len);
  border-radius: var(--app-radius);
  position: fixed;
  left: 0;
  bottom: 93px;
  width: 100%;
}

.player-seek-ctl {
  padding-bottom: 12px;
  cursor: pointer;
}

.player-seek-ctl__now {
  width: 500px;
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
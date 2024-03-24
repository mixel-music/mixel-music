<script lang="ts">
  import { onMount, onDestroy } from "svelte";

  let MusicHandler: HTMLAudioElement = new Audio();
  let IsPlaying: boolean = false;
  let IsRepeat: boolean = false; 
  let TrackInfo: JSON = {};
  let TrackLength: number = 0;
  let TrackCurrent: number = 0;
  let VolumeValue: nummer = 0;

  function SelectTrack(title: string, album: string, artist: string, path: string) {
    let TrackTitle: string = title;
    let TrackAlbum: string = album;
    let TrackArtist: string = artist;
    let TrackPath: str = path;
    MusicHandler.src = path;

    if (MusicHandler.paused) {
      MusicHandler.play();
      IsPlaying = true;
      document.title = Title + ' - mixel-music';
    }
  }
</script>

<div class="player">
  <div class="player-seek">
    <div class="player-time"></div>
  </div>
</div>

<div class="player-area">
  <div class="player-area-info">
    <img src=".">
    <div clas="player-area-info-text">
      <span class="text-title">Test</span>
      <span class="text-description">Description</span>
      <span class="text-description">Length</span>
    </div>
  </div>
  <div class="player-area-menu">
    <button class="player-button" title="Previous">Previous</button>
    <button class="player-button">{IsPlaying ? 'Pause' : 'Play'}</button>
    <button class="player-button" title="Next">Next</button>
  </div>
  <div class="player-area-side">

  </div>
</div>

<style>

</style>
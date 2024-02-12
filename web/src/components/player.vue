<template>
  <div class="player">
    <div class="player-left">
      <p class="text-title">{{ MusicTitle }}</p>
      <p class="text-description">{{ MusicArtist }} - {{ MusicAlbum }}</p>
      <p class="text-description">{{ MusicCurrentFormat }} / {{ MusicDurationFormat }}</p>
    </div>
    <div class="player-center">
      <button class="player-button">
        <IconamoonPlayerStartFill />
      </button>
      <button class="player-button player-button-primary" @click="toggle">
        <IconamoonPlayerPauseFill v-if="IsPlay" />
        <IconamoonPlayerPlayFill v-else="IsPlay" />
      </button>
      <button class="player-button">
        <IconamoonPlayerEndFill />
      </button>
      <div class="player-range" @click="seek($event)" @mousedown="drag_start">
        <div class="player-range-length">
          <div class="player-range-now" :style="{ 'width': MusicSlider + '%' }"></div>
        </div>
      </div>
    </div>
    <div class="player-right">

    </div>
  </div>
</template>

<script>
import IconamoonPlayerPauseFill from '~icons/iconamoon/player-pause-fill';
import IconamoonPlayerPlayFill from '~icons/iconamoon/player-play-fill';
import IconamoonPlayerStartFill from '~icons/iconamoon/player-start-fill';
import IconamoonPlayerEndFill from '~icons/iconamoon/player-end-fill';

import IconamoonHeart from '~icons/iconamoon/heart';
import IconamoonHeartFill from '~icons/iconamoon/heart-fill';
import IconamoonMenuKebabHorizontal from '~icons/iconamoon/menu-kebab-horizontal';
import IconamoonPlaylistRepeatList from '~icons/iconamoon/playlist-repeat-list';
import IconamoonPlaylistRepeatSong from '~icons/iconamoon/playlist-repeat-song';
import IconamoonPlaylistShuffle from '~icons/iconamoon/playlist-shuffle';
import IconamoonRestart from '~icons/iconamoon/restart';
import IconamoonPlaylist from '~icons/iconamoon/playlist';
import IconamoonVolumeDown from '~icons/iconamoon/volume-down';
import IconamoonVolumeOff from '~icons/iconamoon/volume-off';
import IconamoonVolumeUp from '~icons/iconamoon/volume-up';
import IconamoonSearch from '~icons/iconamoon/search';

export default {
  components: {
    IconamoonPlayerPauseFill,
    IconamoonPlayerPlayFill,
    IconamoonPlayerStartFill,
    IconamoonPlayerEndFill
  },
  data() {
    return {
      MusicTitle: null,
      MusicAlbum: null,
      MusicArtist: null,
      MusicCurrent: 0,
      MusicDuration: 0,
      MusicSlider: 0,
      MusicAudio: new Audio(),
      IsDrag: false,
      IsPlay: false,
    };
  },
  created() {
    this.MusicAudio.addEventListener('timeupdate', this.updateTime);
    this.MusicAudio.addEventListener('loadedmetadata', () => {
      this.MusicDuration = this.MusicAudio.duration;
    });
  },
  beforeUnmount() {
    this.MusicAudio.removeEventListener('timeupdate', this.updateTime);
    this.MusicAudio.removeEventListener('loadedmetadata', () => {
      this.MusicDuration = this.MusicAudio.duration;
    });
    this.MusicAudio.pause();
  },
  computed: {
    MusicCurrentFormat() {
      return this.formatTime(this.MusicCurrent);
    },
    MusicDurationFormat() {
      return this.formatTime(this.MusicDuration);
    },
  },
  methods: {
    SetMediaControls: function () {
      if ('mediaSession' in navigator) {
        navigator.mediaSession.metadata = new MediaMetadata({
          title: this.MusicTitle,
          artist: this.MusicArtist,
          album: this.MusicAlbum,
          artwork: [
          ]
        });
        navigator.mediaSession.setActionHandler("play", () => { this.toggle(); });
        navigator.mediaSession.setActionHandler("pause", () => { this.toggle(); });
        navigator.mediaSession.setActionHandler("stop", () => { this.toggle(); });

        navigator.mediaSession.setActionHandler("seekbackward", () => { this.toggle(); });
        navigator.mediaSession.setActionHandler("seekforward", () => { this.toggle(); });
        navigator.mediaSession.setActionHandler("seekto", () => { this.toggle(); });
        navigator.mediaSession.setActionHandler("previoustrack", () => { this.toggle(); });
        navigator.mediaSession.setActionHandler("nexttrack", () => { this.toggle(); });
      }
    },
    SelectTrack(title, album, artist, relpath) {
      this.MusicTitle = title;
      this.MusicArtist = artist;
      this.MusicAlbum = album;
      this.MusicAudio.src = `http://localhost:8000/api/stream/${relpath}`;
      if (this.MusicAudio.paused) {
        this.MusicAudio.play();
        this.IsPlay = true;
        this.SetMediaControls();
      }
    },
    toggle() {
      if (!this.IsDrag && this.MusicAudio.paused && this.MusicCurrent >= this.MusicDuration && this.MusicCurrent != 0) {
        this.MusicCurrent = 0;
        this.MusicAudio.play();
        this.IsPlay = true;
        this.SetMediaControls();
      }
      else if (this.MusicAudio.paused) {
        if (this.MusicAudio.src) {
          this.MusicAudio.play();
          this.IsPlay = true;
          this.SetMediaControls();
        } else {
          console.error("Music is not selected");
        }
      } else {
        this.MusicAudio.pause();
        this.IsPlay = false;
        this.SetMediaControls();
      }
    },
    updateTime() {
      if (!this.IsDrag) this.MusicCurrent = this.MusicAudio.currentTime;
      this.MusicSlider = (this.MusicCurrent / this.MusicDuration) * 100;
      if (!this.IsDrag && this.MusicCurrent >= this.MusicDuration) {
        this.resetPlayer();
      }
    },
    resetPlayer() {
      this.IsPlay = false;
      this.MusicAudio.pause();
    },
    seek(event) {
      const slider_width = this.$el.querySelector('.slider_rail').clientWidth;
      const click_location = event.offsetX;
      const new_current_time = (click_location / slider_width) * this.MusicDuration;
      this.MusicAudio.currentTime = new_current_time;
    },
    drag_start() {
      this.IsDrag = true;
      document.addEventListener('mousemove', this.drag);
      document.addEventListener('mouseup', this.drag_stop);
    },
    drag_stop() {
      this.IsDrag = false;
      document.removeEventListener('mousemove', this.drag);
      document.removeEventListener('mouseup', this.drag_stop);
    },
    drag(event) {
      if (this.IsDrag) {
        const slider = this.$el.querySelector('.slider_rail');
        const slider_width = slider.clientWidth;
        const drag_location = event.clientX - slider.getBoundingClientRect().left;
        const new_current_time = (drag_location / slider_width) * this.MusicDuration;
        this.MusicAudio.currentTime = new_current_time;
      }
    },
    formatTime(time) {
      const minutes = Math.floor(time / 60);
      const seconds = Math.floor(time % 60);
      return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    },
  }
}
</script>
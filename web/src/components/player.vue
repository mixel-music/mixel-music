<template>
  <div class="app_player_container">
    <div class="player_left">
      <p class="player_title">{{ currentTrack }}</p>
      <p class="player_artist">{{ currentArtist }}</p>
      <p class="player_length">{{ currentTimeFormat }} / {{ durationFormat }}</p>
    </div>
    <div class="player_center">
      <button class="player_pause" @click="toggle"><component :is="buttonComponent" /></button>
      <div class="slider_container" @click="seek($event)" @mousedown="drag_start">
        <div class="slider_rail">
          <div class="slider_step" :style="{ 'width': progress + '%' }"></div>
        </div>
      </div>
    </div>
    <div class="player_right">

    </div>
  </div>
</template>

<script>
import { PauseSolid } from '@iconoir/vue';
import { PlaySolid } from '@iconoir/vue';

export default {
  components: {
    PauseSolid,
    PlaySolid
  },
  data() {
    return {
      currentTrack: null,
      currentArtist: null,
      audio: new Audio(),
      currentTime: 0,
      duration: 0,
      progress: 0,
      is_dragging: false,
      buttonComponent: PlaySolid
    };
  },
  created() {
    this.audio.addEventListener('timeupdate', this.updateTime);
    this.audio.addEventListener('loadedmetadata', () => {
      this.duration = this.audio.duration;
    });
  },
  beforeUnmount() {
    this.audio.removeEventListener('timeupdate', this.updateTime);
    this.audio.removeEventListener('loadedmetadata', () => {
      this.duration = this.audio.duration;
    });
    this.audio.pause();
  },
  computed: {
    currentTimeFormat() {
      return this.formatTime(this.currentTime);
    },
    durationFormat() {
      return this.formatTime(this.duration);
    },
  },
  methods: {
    selectTrack(title, artist, relpath) {
      this.currentTrack = title;
      this.currentArtist = artist;
      this.audio.src = `http://localhost:8000/api/stream/${relpath}`;
      if (this.audio.paused) {
        this.audio.play();
        this.buttonComponent = PauseSolid;
      }
    },
    toggle() {
      if (this.audio.paused) {
        if (this.audio.src) {
          this.audio.play();
          this.buttonComponent = PauseSolid;
        } else {
          console.error("No track selected");
        }
      } else {
        this.audio.pause();
        this.buttonComponent = PlaySolid;
      }
    },
    updateTime() {
      if (!this.is_dragging) this.currentTime = this.audio.currentTime;
      this.progress = (this.currentTime / this.duration) * 100;
      if (!this.is_dragging && this.currentTime >= this.duration) {
        this.resetPlayer();
      }
    },
    resetPlayer() {
      this.buttonComponent = PlaySolid;
      this.currentTrack = null;
      this.currentArtist = null;
      this.currentTime = 0;
      this.progress = 0;
      this.audio.currentTime = 0; // Reset audio currentTime
      this.audio.pause();
    },
    seek(event) {
      const slider_width = this.$el.querySelector('.slider_rail').clientWidth;
      const click_location = event.offsetX;
      const new_current_time = (click_location / slider_width) * this.duration;
      this.audio.currentTime = new_current_time;
    },
    drag_start() {
      this.is_dragging = true;
      document.addEventListener('mousemove', this.drag);
      document.addEventListener('mouseup', this.drag_stop);
    },
    drag_stop() {
      this.is_dragging = false;
      document.removeEventListener('mousemove', this.drag);
      document.removeEventListener('mouseup', this.drag_stop);
    },
    drag(event) {
      if (this.is_dragging) {
        const slider = this.$el.querySelector('.slider_rail');
        const slider_width = slider.clientWidth;
        const drag_location = event.clientX - slider.getBoundingClientRect().left;
        const new_current_time = (drag_location / slider_width) * this.duration;
        this.audio.currentTime = new_current_time;
      }
    },
    formatTime(time) {
      const minutes = Math.floor(time / 60);
      const seconds = Math.floor(time % 60);
      return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    }
  }
}
</script>
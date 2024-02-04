<template>
  <div class="app_player_container">
    <button @click="toggle()">{{ buttonStatus }} {{ currentTimeFormat }} / {{ durationFormat }}</button>
    <p>{{ currentTrack }}</p>
  </div>
</template>

<script>
export default {
  data() {
    return {
      currentTrack: null,
      audio: new Audio(),
      currentTime: 0,
      duration: 0,
      buttonStatus: "Play"
    };
  },

  created() {
    this.audio.addEventListener('timeupdate', this.updateTime);
  },
  beforeUnmount() {
    this.audio.removeEventListener('timeupdate', this.updateTime);
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
    selectTrack(track) {
      this.currentTrack = track;
      this.audio.src = `http://localhost:8000/api/stream/${track}`;
      this.audio.addEventListener('loadedmetadata', () => {
        this.duration = this.audio.duration;
      });

      if (this.audio.paused) {
        this.audio.play();
        this.buttonStatus = "Pause";
      }
    },

    toggle() {
      if (this.audio.paused) {
        if (this.audio.src) {
          this.audio.play();
          this.buttonStatus = "Pause";
        } else {
          console.error("No track selected");
        }
      } else {
        this.audio.pause();
        this.buttonStatus = "Play";
      }
    },

    updateTime() {
      this.currentTime = this.audio.currentTime;
      if (this.duration == this.currentTime && this.currentTime != 0) {
        this.buttonStatus = "Play";
        this.currentTrack = null;
        this.currentTime = 0;
        this.duration = 0;
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
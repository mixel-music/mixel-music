<template>
  <div class="app_player_container">
    <div class="player_title">
      <p class="music_title">{{ currentTrack }}</p>
      <p class="music_artist">{{ currentArtist }}</p>
      <p class="music_duration">{{ currentTimeFormat }} / {{ durationFormat }}</p>
    </div>
    <button @click="toggle()">{{ buttonStatus }}</button>
  </div>
</template>

<script>
let currentTrack = null;
let currentArtist = null;

export default {
  data() {
    return {
      currentTrack: null,
      currentArtist: null,
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
    selectTrack(title, artist, relpath) {
      currentTrack = title;
      currentArtist = artist;
      this.audio.src = `http://localhost:8000/api/stream/${relpath}`;
      this.audio.addEventListener('loadedmetadata', () => {
        this.duration = this.audio.duration;
      });

      if (this.audio.paused) {
        this.audio.play();
        this.currentTrack = currentTrack;
        this.currentArtist = currentArtist;
        document.title = currentTrack + ' - Tamaya'
        this.buttonStatus = "Pause";
      }
    },

    toggle() {
      if (this.audio.paused) {
        if (this.audio.src) {
          this.audio.play();
          this.currentTrack = currentTrack;
          this.currentArtist = currentArtist;
          document.title = currentTrack + ' - Tamaya'
          this.buttonStatus = "Pause";
        } else {
          console.error("No track selected");
        }
      } else {
        this.audio.pause();
        document.title = 'Tamaya'
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
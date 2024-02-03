<template>
  <div>
    <a v-for="track in tracks" :key="track" @click="selectTrack(track)" style="display: block;">
      {{ track }}
    </a>
    <br>
    <div v-if="currentTrack">
      <button @click="toggle">{{ buttonStatus }}</button>
      <br>
      <br>
      Now Playing: {{ currentTrack }}
      <br>
      <br>
      <div>Current Time: {{ currentTimeFormatted }}</div>
      <div>Duration: {{ durationFormatted }}</div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tracks: [],
      currentTrack: null,
      audio: new Audio(),
      currentTime: 0,
      duration: 0,
      buttonStatus: "Pause"
    };
  },
  created() {
    this.fetchMusicList();
    this.audio.addEventListener('timeupdate', this.updateTime);
  },
  beforeDestroy() {
    this.audio.removeEventListener('timeupdate', this.updateTime);
    this.audio.pause();
  },
  computed: {
    currentTimeFormatted() {
      return this.formatTime(this.currentTime);
    },
    durationFormatted() {
      return this.formatTime(this.duration);
    },
  },
  methods: {
    fetchMusicList() {
      axios.get('http://localhost:8000/api/list')
        .then(response => {
          this.tracks = response.data.music_files;
        })
        .catch(error => {
          console.error("There was an error fetching the music files:", error);
        });
    },
    selectTrack(track) {
      this.currentTrack = track;
      this.audio.src = `http://localhost:8000/api/stream/${track}`;
      this.audio.addEventListener('loadedmetadata', () => {
        this.duration = this.audio.duration;
      });
      this.audio.play();
      this.buttonStatus = "Pause";
    },
    toggle() {
      if (this.audio.paused) {
        this.audio.play();
        this.buttonStatus = "Pause";
      } else {
        this.audio.pause();
        this.buttonStatus = "Play";
      }
    },
    updateTime() {
      this.currentTime = this.audio.currentTime;
    },
    formatTime(time) {
      const minutes = Math.floor(time / 60);
      const seconds = Math.floor(time % 60);
      return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    },
  },
};
</script>
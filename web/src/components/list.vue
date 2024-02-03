<template>
  <div class="player_body">
    <a v-for="track in tracks" :key="track" @click="selectTrack(track)" style="display: block">
      {{ track }}
    </a>
    <br>
    <button @click="toggle">{{ buttonStatus }} {{ currentTimeFormatted }} / {{ durationFormatted }}</button>
    <br>
    <!--<p>{{ currentTrack }}</p>-->
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tracks: [],
      //currentTrack: "Empty",
      audio: new Audio(),
      currentTime: 0,
      duration: 0,
      buttonStatus: "Play"
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
      document.title = track + " - Tamaya";
      this.buttonStatus = "Pause";
    },
    toggle() {
      if (this.audio.paused) {
        if (this.audio.src) {
          this.audio.play();
          this.buttonStatus = "Pause";
        } else {
          console.error("not selected");
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
          document.title = "Tamaya";
          this.currentTrack = '';
          this.currentTime = 0;
          this.duration = 0;
          this.fetchMusicList();
      }
    },
    formatTime(time) {
      const minutes = Math.floor(time / 60);
      const seconds = Math.floor(time % 60);
      return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
    },
  },
};
</script>
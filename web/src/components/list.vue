<template>
  <div class="music_list">
      <a :style="music_link" v-for="file in musicFiles" :key="file" @click="playMusic(file)">
        {{ file }}
      </a>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      musicFiles: [],
      music_link: { display: 'block' }
    };
  },

  created() {
    this.fetchMusic();
  },

  methods: {
    fetchMusic() {
      axios.get('http://localhost:8000/api/list')
        .then(response => {
          this.musicFiles = response.data.music_files;
        })
        .catch(error => {
          console.error("There was an error fetching the music files:", error);
        });
    },
    playMusic(file) {
      const audio = new Audio(`http://localhost:8000/api/stream/${file}`);
      audio.play();
      console.log(audio.play());
    }
  }

};
</script>
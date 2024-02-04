<template>
  <div class="app_container_tracks">
    <a class="tracks_title" v-for="track in tracks" :key="track" @click="this.$emit('select-track', track);">
      {{ track }}
    </a>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      tracks: []
    };
  },

  created() {
    this.fetchMusicList();
  },

  methods: {
    fetchMusicList() {
      axios.get('http://localhost:8000/api/tracks')
        .then(response => {
          this.tracks = response.data.music_files;
        })
        .catch(error => {
          console.error("Failed to fetch:", error);
        });
    },
  }
}
</script>
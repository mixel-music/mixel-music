<template>
  <div class="app_container_tracks">
    <a class="tracks_title" v-for="(track, index) in tracks" :key="index" @click="this.$emit('select-track', track[0], track[1]);">
      {{ track[0] }}
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
          this.tracks = response.data;
        })
        .catch(error => {
          console.error("Failed to fetch:", error);
        });
    },
  }
}
</script>
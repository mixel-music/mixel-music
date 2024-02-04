<template>
  <div class="app_container_tracks">
    <div v-for="(song, index) in metadata" :key="index">
      <a class="track_title" @click="this.$emit('select-track', song[0], song[4]);">
        {{ song[1] }} - {{ song[0] }} ({{ song[2] }})
      </a>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      metadata: null
    };
  },

  created() {
    this.fetchMusicList();
  },

  methods: {
    fetchMusicList() {
      axios.get('http://localhost:8000/api/tracks')
        .then(response => {
          this.metadata = response.data;
        })
        .catch(error => {
          console.error("Failed to fetch:", error);
        });
    },
  }
}
</script>
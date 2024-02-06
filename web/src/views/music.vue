<template>
  <div class="list_container">
    <div class="list_card" v-for="(song, index) in metadata" :key="index">
      <a class="music_title" @click="$emit('select-track', song[0], song[2], song[4]);">
        {{ song[0] }}
      </a>
      <a class="music_artist">
        {{ song[2] }}
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
      axios.get('http://localhost:8000/api/list?type=music')
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
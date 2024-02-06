<template>
  <div class="tracks_cards_container">
    <div class="tracks_card" v-for="(song, index) in metadata" :key="index">
      <a class="track_title" @click="$emit('select-track', song[0], song[2], song[4]);">
        {{ song[2] }} - {{ song[0] }}
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
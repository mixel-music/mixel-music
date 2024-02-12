<template>
  <div class="card-grid">
    <div class="card" v-for="(song, index) in metadata" :key="index">
      <a class="text-title" @click="this.$emit('SelectTrack', song[0], song[1], song[2], song[3]);">
        {{ song[0] }}
      </a>
      <a class="text-description">
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
      this.FetchMusicList();
    },

    methods: {
      FetchMusicList() {
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
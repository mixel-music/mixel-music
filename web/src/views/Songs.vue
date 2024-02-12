<template>
  <div class="card-grid">
    <div class="card" v-for="(track, index) in list" :key="index">
      <a class="text-title" @click="this.$emit('SelectTrack', track[0], track[1], track[2], track[3]);">
        {{ track[0] }}
      </a>
      <a class="text-description">
        {{ track[2] }}
      </a>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      list: null,
    };
  },

  created() {
    this.FetchMusicList();
  },

  methods: {
    FetchMusicList() {
      axios.get('http://localhost:8000/api/list?type=music')
        .then(response => {
          this.list = response.data;
        })
        .catch(error => {
          console.error("Failed to fetch:", error);
        });
    },
  }
}
</script>
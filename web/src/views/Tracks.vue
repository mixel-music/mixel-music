<template>
  <div class="card-grid">
    <div class="card" v-for="(track, index) in list" :key="index" @click="this.$emit('SelectTrack', track['title'], track['album'], track['artist'], track['id']);">
      <div class="card-image">
        
      </div>
      <div class="card-content">
        <a class="text-title">
          {{ track['title'] }}
        </a>
        <a class="text-description">
          {{ track['artist'] }}
        </a>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import IconamoonPlayCircle from '~icons/iconamoon/play-circle';

export default {
  components: {
    IconamoonPlayCircle,
  },

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
      axios.get('http://localhost:8000/api/tracks')
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
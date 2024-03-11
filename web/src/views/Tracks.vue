<template>
  <div class="card-grid">
    <div v-for="(track, index) in fullCardList" :key="track.hash" class="card">
      <div v-if="track.title">
        <div class="card-image-content">
          <img v-lazy="`http://localhost:2843/api/images/${ track.hash }?size=300`" class="card-image" :alt="track.album" @click="this.$emit('SelectTrack', track.title, track.album, track.artist, track.hash);">
        </div>
        <div class="card-content">
          <span class="text-title">{{ track.title }}</span>
          <span class="text-description">{{ track.artist }}</span>
        </div>
      </div>
      <div v-else class="card-placeholder">

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
      info: [],
    };
  },

  created() {
    this.FetchMusicList();
  },

  methods: {
    FetchMusicList() {
      axios.get('http://localhost:2843/api/tracks')
        .then(response => {
          this.info = response.data;
        })
        .catch(error => {
          console.error("Failed to fetch:", error);
        });
    },
  },

  computed: {
    fullCardList() {
      const totalItems = 7;
      const emptyItemsToAdd = totalItems - this.info.length;
      const emptyItems = Array.from({ length: emptyItemsToAdd }, () => ({}));
      return [...this.info, ...emptyItems];
    },
  },
}
</script>
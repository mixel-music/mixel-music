<template>
  <div class="card-grid">
    <div v-for="(album, index) in fullCardList" :key="album.albumhash" class="card">
      <div v-if="album.album">
        <img :src="`http://localhost:2843/api/images/${ album.imagehash }?size=300`" class="card-image">
        <div class="card-content">
          <span class="text-title">{{ album.album }}</span>
          <span class="text-description">{{ album.albumartist }}</span>
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
      axios.get('http://localhost:2843/api/albums')
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
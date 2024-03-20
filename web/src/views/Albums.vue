<template>
  <Title />
  <div class="card-grid">
    <div v-for="(album, index) in fullCardList" :key="album.albumhash" class="card">
      <div v-if="album.album">
        <div class="card-image-content">
          <router-link :to="`/albums/${ album.albumhash }`">
            <img v-lazy="`http://localhost:2843/api/v1/images/${ album.imagehash }?size=300`" class="card-image">
          </router-link>
        </div>
        <div class="card-content">
          <router-link :to="`/albums/${ album.albumhash }`">
            <span class="text-title">{{ album.album }}</span>
          </router-link>
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
import Title from '../components/Title.vue';
import IconamoonPlayCircle from '~icons/iconamoon/play-circle';

export default {
  components: {
    Title,
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
      axios.get('http://localhost:2843/api/v1/albums')
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
      const totalItems = 6;
      const emptyItemsToAdd = totalItems - this.info.length;
      const emptyItems = Array.from({ length: emptyItemsToAdd }, () => ({}));
      return [...this.info, ...emptyItems];
    },
  },
}
</script>
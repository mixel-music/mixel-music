<template>
  <div class="list_container">
    <div class="list_card" v-for="(album, index) in metadata" :key="index">
      <a class="list_title">
        {{ album }}
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
      axios.get('http://localhost:8000/api/list?type=album')
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
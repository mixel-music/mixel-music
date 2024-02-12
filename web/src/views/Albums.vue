<template>
  <div class="card-grid">
    <div class="card" v-for="(album, index) in list" :key="index">
      <a class="text-title">
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
      list: null,
    };
  },
    
  created() {
    this.FetchAlbumList();
  },
    
  methods: {
    FetchAlbumList() {
      axios.get('http://localhost:8000/api/list?type=album')
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
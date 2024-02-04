<template>
    <div class="tracks_cards_container">
      <div class="tracks_card" v-for="(album, index) in metadata" :key="index">
        <a class="album_title">
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
        axios.get('http://localhost:8000/api/albums')
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
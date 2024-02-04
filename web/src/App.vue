<template>
  <div class="app_main">
    <div class="app_navbar">

    </div>
    <div class="app_sidebar">

    </div>
    <div class="app_container">
      <!--<albums />-->
      <tracks @select-track="handleSelectTrack"/>
    </div>
    <div class="app_player">
      <player ref="player"/>
    </div>
  </div>
</template>

<script>
import tracks from './components/tracks.vue'
import player from './components/player.vue'
import albums from './components/albums.vue'

export default {
  name: 'App',
  components: {
    tracks,
    player,
    albums,
  },

  methods: {
    handleSelectTrack(title, artist, relpath) {
      this.$refs.player.selectTrack(title, artist, relpath);
    }
  }
}
</script>
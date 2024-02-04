<template>
  <div class="app_sidebar">

  </div>
  <div class="app_container">
    <tracks @select-track="handleSelectTrack"/>
  </div>
  <div class="app_player">
    <player ref="player"/>
  </div>
</template>

<script>
import tracks from './components/tracks.vue'
import player from './components/player.vue'

export default {
  name: 'App',
  components: {
    tracks,
    player
  },

  methods: {
    handleSelectTrack(track) {
      this.$refs.player.selectTrack(track);
    }
  }
}
</script>
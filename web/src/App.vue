<template>
  <div class="app_main">
    <div class="app_sidebar">
      <div class="app_sidebar_container">
        <RouterLink to="/album">Album</RouterLink>
      </div>
    </div>
    <div class="app_container">
      <div class="app_navbar">
      </div>
      <RouterView v-slot="{ Component }">
        <component :is="Component" @select-track="handleSelectTrack" />
      </RouterView>
    </div>
    <div class="app_player">
      <player ref="player" />
    </div>
  </div>
</template>

<script>
import player from './components/player.vue'

export default {
  name: 'App',
  components: {
    player
  },

  methods: {
    handleSelectTrack(title, artist, relpath) {
      this.$refs.player.selectTrack(title, artist, relpath);
    }
  }
}
</script>
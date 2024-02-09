<template>
  <div class="app_main">
    <div class="app_sidebar">
      <div class="app_sidebar_container">
        <div class="sidebar_menu">
          <RouterLink to="/" class="sidebar_link">Music</RouterLink>
        </div>
        <div class="sidebar_menu">
          <RouterLink to="/album" class="sidebar_link">Album</RouterLink>
        </div>
      </div>
    </div>
    <div class="app_container">
      <div class="app_navbar">
        <navbar />
      </div>
      <RouterView v-slot="{ Component }">
        <component :is="Component" @SelectTrack="HandleSelectTrack" />
      </RouterView>
    </div>
    <div class="app_player">
      <player ref="player" />
    </div>
  </div>
</template>

<script>
import navbar from './components/navbar.vue'
import player from './components/player.vue'

export default {
  name: 'App',
  components: {
    navbar,
    player,
  },
  methods: {
    HandleSelectTrack(music_title, music_album, music_artist, music_path) {
      this.$refs.player.SelectTrack(music_title, music_album, music_artist, music_path);
    },
  }
}
</script>
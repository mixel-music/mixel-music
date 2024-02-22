<template>
  <Navbar />
  <section class="content">
    <div class="content-header">
      <span class="content-title">
        {{ $route.name }}
      </span>
    </div>
    <RouterView v-slot="{ Component }">
      <component :is="Component" @SelectTrack="HandleSelectTrack" />
    </RouterView>
  </section>
  <Player ref="player" />
</template>

<script>
import Sidebar from './components/Sidebar.vue'
import Navbar from './components/Navbar.vue'
import Player from './components/Player.vue'

export default {
  name: 'App',
  components: {
    Sidebar,
    Navbar,
    Player,
  },
  
  methods: {
    HandleSelectTrack(music_title, music_album, music_artist, music_path) {
      this.$refs.player.SelectTrack(music_title, music_album, music_artist, music_path);
    },
  },
}
</script>
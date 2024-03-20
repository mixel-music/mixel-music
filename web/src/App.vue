<template>
  <Navbar />
  <section class="content">
    <RouterView v-slot="{ Component }">
      <component :is="Component" @SelectTrack="HandleSelectTrack" />
    </RouterView>
  </section>
  <Player ref="player" />
</template>

<script>
import Navbar from './components/Navbar.vue'
import Player from './components/Player.vue'

export default {
  name: 'App',
  components: {
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
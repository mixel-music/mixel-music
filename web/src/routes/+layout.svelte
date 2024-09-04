<script lang="ts">
  import './style.css';
  import { onDestroy } from 'svelte';
  import Sidebar from '$lib/components/layouts/sidebar/sidebar.svelte';
  import Navbar from '$lib/components/layouts/navbar/navbar.svelte';
  import Player from '$lib/components/layouts/player/player.svelte';
  import PlayerQueue from '$lib/components/layouts/player/player-queue.svelte';
  import PlayerService from '$lib/stores/stores';

  onDestroy(() => {
    PlayerService.destroy();
  })
</script>

<div id="app">
  <Sidebar />

  <div class="app-body">
    <div class="app-main">
      <Navbar />
      <slot />
    </div>
  </div>

  <PlayerQueue />
  <Player />
</div>

<style>
  #app {
    width: 100%;
    display: flex;
    height: 100dvh;
    flex-direction: row;
    box-sizing: border-box;
  }

  .app-body {
    width: 100%;
    margin-bottom: 96px;
    overflow-y: scroll;
    user-select: none;
    display: flex;
    flex-direction: column;
    align-content: center;
    flex-wrap: wrap;
  }

  .app-body:focus {
    outline: none;
  }

  .app-main {
    display: flex;
    flex-direction: column;
    width: 100%;
    /* width: min(1600px, 100%); */
    padding-left: 64px;
    padding-right: 64px;
    margin-bottom: 24px;
  }
</style>
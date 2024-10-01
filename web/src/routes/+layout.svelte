<script lang="ts">
  import './style.css';
  import { onDestroy } from 'svelte';
  import { afterNavigate } from '$app/navigation';
  import { page } from '$app/stores';

  import Sidebar from "$lib/components/layouts/sidebar/Sidebar.svelte";
  import PlayerQueue from "$lib/components/layouts/player/PlayerQueue.svelte";
  import Player from "$lib/components/layouts/player/Player.svelte";
  import PlayerService from '$lib/stores/stores';

  let previousPathname: string | null = null;

  afterNavigate(() => {
    const currentPathname = $page.url.pathname;

    if (previousPathname == null || currentPathname !== previousPathname) {
      document.getElementById("contents")?.scrollIntoView({
        behavior: "smooth",
        block: "start",
        inline: "nearest"
      });
    }

    previousPathname = currentPathname;
  });

  onDestroy(() => {
    PlayerService.destroy();
  })
</script>

<div id="app">
  <Sidebar />

  <div>
    <slot />
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

  #app > div {
    width: 100%;
    margin-bottom: 96px;
    position: relative;
    overflow-y: scroll;
    user-select: none;
    display: flex;
    flex-direction: column;
    align-content: center;
    flex-wrap: wrap;
  }

  #app > div:hover {
    outline: none;
  }
</style>

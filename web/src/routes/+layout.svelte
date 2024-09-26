<script lang="ts">
  import './style.css';
  import { onDestroy } from 'svelte';
  import { afterNavigate } from '$app/navigation';
  import { page } from '$app/stores';

  import Sidebar from '$lib/components/layouts/sidebar/Sidebar.svelte';
  import Navbar from '$lib/components/layouts/navbar/Navbar.svelte';
  import Player from '$lib/components/layouts/player/Player.svelte';
  import PlayerQueue from '$lib/components/layouts/player/PlayerQueue.svelte';
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

<svelte:window />

<div id="app">
  <Sidebar />

  <div>
    <div id="contents">
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

  #app > div {
    width: 100%;
    margin-bottom: 96px;
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

  #app > div > div {
    display: flex;
    flex-direction: column;
    width: 100%;
    /* width: min(1600px, 100%); */
    padding: var(--space-m) var(--space-xl);
    padding-top: 0
  }

  @media screen and (max-width: 1960px) {
    #app > div > div {
      padding: 0 min(64px, 3%);
    }
  }
</style>
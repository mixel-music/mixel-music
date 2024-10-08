<script lang="ts">
  import './style.css';
  import { onDestroy } from 'svelte';
  import { page } from '$app/stores';
  import { afterNavigate } from '$app/navigation';
  import AlbumWrap from '$lib/components/AlbumWrap.svelte';
  import Sidebar from "$lib/components/layouts/sidebar/Sidebar.svelte";
  import Navbar from '$lib/components/layouts/navbar/Navbar.svelte';
  import Player from "$lib/components/layouts/player/Player.svelte";
  import PlayerQueue from "$lib/components/layouts/player/PlayerQueue.svelte";
  import PlayerService from '$lib/stores/stores';

  $: albumId = $page.params.albumId;
  let previousPathname: string | null = null;

  afterNavigate(() => {
    const currentPathname = $page.url.pathname;
    
    if (previousPathname == null || currentPathname !== previousPathname) {
      document.getElementById("contents")?.scrollIntoView({
        block: "start",
        inline: "nearest",
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

  <div id="wrap">
    {#if albumId}
      <AlbumWrap {albumId} />
    {/if}

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

  #contents {
    width: 100%;
    display: flex;
    flex-direction: column;
    /* width: min(1600px, 100%); */
    backdrop-filter: blur(12px);
    padding: var(--space-m) var(--space-xl);
    padding-top: 0;
  }

  @media screen and (max-width: 1960px) {
    #contents {
      padding: 0 min(64px, 3%);
    }
  }
</style>

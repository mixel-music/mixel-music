<script lang="ts">
  import '../style.css';
  import { page } from '$app/stores';
  import AlbumWrap from '$lib/components/AlbumWrap.svelte';
  import Sidebar from "$lib/components/layouts/sidebar/Sidebar.svelte";
  import Navbar from '$lib/components/layouts/navbar/Navbar.svelte';
  import Player from "$lib/components/layouts/player/Player.svelte";
  import PlayerQueue from "$lib/components/layouts/player/PlayerQueue.svelte";

  $: albumId = $page.params.albumId;
</script>

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

<style>
  #wrap {
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

  #wrap:hover {
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

<script lang="ts">
  import { onMount } from 'svelte';
  import Header from '$lib/components/Header.svelte'

  interface artistItemModel {
    artisthash: string;
    artist: string;
  }

  let artistItem: artistItemModel[] = [];

  onMount(async () => {
    const artistFetch = await fetch('http://localhost:2843/api/artists');
    const artist = await artistFetch.json();

    artistItem = artist.map((tag: any) => ({
      artisthash: tag.artisthash,
      artist: tag.artist,
    }));
  });
</script>

<svelte:head>
  <title>Artists • mixel-music</title>
</svelte:head>

<Header title="Artists" />

{#if artistItem.length > 0}
  <div class="card-grid">
    {#each artistItem as tag (tag.artisthash)}
      <div class="card">
        <div
          role="button"
          tabindex=0
          class="card-image-content"
        >
        </div>
        <div class="card-content">
          <span class="text-title">{tag.artist}</span>
        </div>
      </div>
    {/each}
  </div>
{:else}
  <div class="card-placeholder">

  </div>
{/if}

<style>

</style>

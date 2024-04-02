<script lang="ts">
  import { onMount } from 'svelte';
  import Header from '$lib/components/Header.svelte'

  interface albumItemModel {
    albumhash: string;
    album: string;
    albumartist: string;
    imagehash: string;
  }

  let albumItem: albumItemModel[] = [];

  onMount(async () => {
    const albumFetch = await fetch('http://localhost:2843/api/albums');
    const album = await albumFetch.json();

    albumItem = album.map((tag: any) => ({
      albumhash: tag.albumhash,
      album: tag.album,
      albumartist: tag.albumartist,
      imagehash: tag.imagehash,
    }));
  });
</script>

<svelte:head>
  <title>Albums • mixel-music</title>
</svelte:head>

<Header title="Albums" />

{#if albumItem.length > 0}
  <div class="card-grid">
    {#each albumItem as tag (tag.albumhash)}
      <div class="card">
        <div
          role="button"
          tabindex=0
          class="card-image-content"
        >
          <img
            loading="lazy"
            src={`http://localhost:2843/api/images/${tag.imagehash}?size=300`}
            alt="{tag.album}"
            class="card-image"
          >
          </div>
        <div class="card-content">
          <span class="text-title">{tag.album}</span>
          <span class="text-description">{tag.albumartist}</span>
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

<script lang="ts">
  import { onMount } from 'svelte';

  interface TrackItemsModel {
    hash: string;
    title: string;
    album: string;
    artist: string;
    imagehash: string;
  }

  let TrackItems: TrackItemsModel[] = [];

  onMount(async () => {
    const TracksFetch = await fetch('http://localhost:2843/api/tracks');
    const Tracks = await TracksFetch.json();

    TrackItems = Tracks.map((item: any) => ({
      hash: item.hash,
      title: item.title,
      album: item.album,
      artist: item.artist,
      imagehash: item.imagehash,
    }));
  });
</script>

<svelte:head>
  <title>Tracks • mixel-music</title>
</svelte:head>

{#if TrackItems.length > 0}
  <div class="card-grid">
    {#each TrackItems as item (item.hash)}
      <div class="card">
        <div class="card-image-content">
          <img
            loading="lazy"
            src={`http://localhost:2843/api/images/${item.imagehash}?size=300`}
            alt="{item.title}"
            class="card-image"
          />
        </div>
        <div class="card-content">
          <span class="text-title">{ item.title }</span>
          <span class="text-description">{ item.artist }</span>
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

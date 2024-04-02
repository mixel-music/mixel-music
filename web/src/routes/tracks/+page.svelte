<script lang="ts">
  import { onMount } from 'svelte';
  import { hash, title, album, artist, imagehash } from '$lib/stores';
  import Header from '$lib/components/Header.svelte'

  interface trackItemModel {
    hash: string;
    title: string;
    album: string;
    artist: string;
    imagehash: string;
  }

  let trackItem: trackItemModel[] = [];

  onMount(async () => {
    const trackFetch = await fetch('http://localhost:2843/api/tracks');
    const track = await trackFetch.json();

    trackItem = track.map((tag: any) => ({
      hash: tag.hash,
      title: tag.title,
      album: tag.album,
      artist: tag.artist,
      imagehash: tag.imagehash,
    }));
  });
</script>

<svelte:head>
  <title>Tracks • mixel-music</title>
</svelte:head>

<Header title="Tracks" />

{#if trackItem.length > 0}
  <div class="card-grid">
    {#each trackItem as tag (tag.hash)}
      <div class="card">
        <div
          role="button"
          tabindex=0

          class="card-image-content"
          on:click={() => (
            hash.set(tag.hash),
            title.set(tag.title),
            album.set(tag.album),
            artist.set(tag.artist), 
            imagehash.set(tag.imagehash)
          )}
        >
          <img
            loading="lazy"
            src={`http://localhost:2843/api/images/${tag.imagehash}?size=300`}
            alt="{tag.title}"
            class="card-image"
          >
          </div>
        <div class="card-content">
          <span class="text-title">{ tag.title }</span>
          <span class="text-description">{ tag.artist }</span>
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

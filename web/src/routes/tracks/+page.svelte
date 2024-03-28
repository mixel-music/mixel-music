<script lang="ts">
  import { onMount } from 'svelte';
  import { hash, title, album, artist, imagehash } from '$lib/stores';

  function selectTrack(
    tHash: string,
    tTitle: string,
    tAlbum: string,
    tArtist: string,
    tImageHash: string,
  ): void {
    hash.set(tHash);
    title.set(tTitle);
    album.set(tAlbum);
    artist.set(tArtist);
    imagehash.set(tImageHash);
  }

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

<!-- svelte-ignore a11y-no-static-element-interactions -->
<!-- svelte-ignore a11y-click-events-have-key-events -->
{#if trackItem.length > 0}
  <div class="card-grid">
    {#each trackItem as tag (tag.hash)}
      <div class="card">
        <div
          class="card-image-content"
          on:click={() => selectTrack(
            tag.hash,
            tag.title,
            tag.album,
            tag.artist, 
            tag.imagehash
          )}
        >
          <img
            loading="lazy"
            src={`http://localhost:2843/api/images/${tag.imagehash}?size=300`}
            alt="{tag.title}"
            class="card-image"
          />
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

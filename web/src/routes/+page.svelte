<script lang="ts">
  import { hash, title, album, artist, imagehash } from '$lib/stores';
  import Header from '$lib/components/layouts/title.svelte'
  import type { PageData } from './$types';

  export let data: PageData;
</script>

<svelte:head>
  <title>Home • mixel-music</title>
</svelte:head>

<Header title={data.title} />

{#if data.trackItem.length > 0}
  <div class="card-grid">
    {#each data.trackItem as tag, index (tag.hash)}
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
    {#if data.trackItem.length < 8}
      {#each Array(8 - data.trackItem.length) as _, index}
        <div class="card-placeholder">
          <!-- Placeholder content -->
        </div>
      {/each}
    {/if}
  </div>
{:else}
  <div class="card-placeholder">
    <!-- Placeholder content -->
  </div>
{/if}
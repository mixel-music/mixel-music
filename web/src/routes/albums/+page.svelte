<script lang="ts">
  import Header from '$lib/components/layouts/title.svelte'
  import type { PageData } from './$types';

  export let data: PageData;
</script>

<svelte:head>
  <title>Albums • mixel-music</title>
</svelte:head>

<Header title={data.title} />

{#if data.albumItem.length > 0}
  <div class="card-grid">
    {#each data.albumItem as tag (tag.albumhash)}
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

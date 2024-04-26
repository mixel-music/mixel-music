<script lang="ts">
  import Header from '$lib/components/elements/tab-header.svelte'
  import type { PageData } from './$types';

  export let data: PageData;
</script>

<svelte:head>
  <title>Artists • mixel-music</title>
</svelte:head>

<Header title={data.title} />

{#if data.artistItem.length > 0}
  <div class="card-grid">
    {#each data.artistItem as tag (tag.artisthash)}
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

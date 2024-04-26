<script lang="ts">
  import type { PageData } from './$types';
  import { hash, title, album, artist, imagehash } from '$lib/stores';
  import CardGridGroup from '$lib/components/elements/card-grid-group.svelte';
  import CardGrid from '$lib/components/elements/card-grid.svelte';
  import ContentTitle from '$lib/components/elements/content-title.svelte';
  import ContentText from '$lib/components/elements/content-text.svelte';

  export let data: PageData;

  function SetTrack(tag: any): void {
    hash.set(tag.hash),
    title.set(tag.title),
    album.set(tag.album),
    artist.set(tag.artist), 
    imagehash.set(tag.imagehash)
  }
</script>

<svelte:head>
  <title>Tracks • mixel-music</title>
</svelte:head>

{#if data.trackItem.length > 0}
  <CardGridGroup title={ data.title }>

    {#each data.trackItem as tag (tag.hash)}
      <CardGrid
        on:click={() => SetTrack(tag) }
        src={ `http://localhost:2843/api/images/${tag.imagehash}?size=300` }
        alt={ tag.title }
      >

        <div class="card-content">
          <ContentTitle title="{ tag.title }" />
          <ContentText text="{ tag.artist }" />
        </div>

      </CardGrid>
    {/each}

  </CardGridGroup>
{/if}
<script lang="ts">
  import type { PageData } from './$types';
  import CardGridGroup from '$lib/components/elements/card-grid-group.svelte';
  import CardGrid from '$lib/components/elements/card-grid.svelte';
  import ContentTitle from '$lib/components/elements/content-title.svelte';
  import ContentText from '$lib/components/elements/content-text.svelte';

  export let data: PageData;
</script>

<svelte:head>
  <title>Albums • mixel-music</title>
</svelte:head>

{#if data.albumItem.length > 0}
  <CardGridGroup title={data.title}>

    {#each data.albumItem as tag (tag.albumhash)}
      <CardGrid
        link="/albums/{tag.albumhash}"
        src={`http://localhost:2843/api/images/${tag.imagehash}?size=300`}
        alt="{tag.album}"
      >

        <div class="card-content">
          <ContentTitle title={ tag.album } />
          <ContentText text={ tag.albumartist } />
        </div>

      </CardGrid>
    {/each}

  </CardGridGroup>
{/if}
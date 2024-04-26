<script lang="ts">
  import type { PageData } from './$types';
  import CardGridGroup from '$lib/components/elements/card-grid-group.svelte';
  import CardGrid from '$lib/components/elements/card-grid.svelte';
  import ContentTitle from '$lib/components/elements/content-title.svelte';

  export let data: PageData;
</script>

<svelte:head>
  <title>Artists • mixel-music</title>
</svelte:head>

{#if data.artistItem.length > 0}
  <CardGridGroup title={ data.title }>

    {#each data.artistItem as tag (tag.artisthash)}
      <CardGrid>

        <div class="card-content">
          <ContentTitle title={ tag.artist } />
        </div>

      </CardGrid>
    {/each}

  </CardGridGroup>
{/if}
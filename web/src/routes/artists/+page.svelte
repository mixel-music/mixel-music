<script lang="ts">
  import type { PageData } from './$types';

  import CardItemGroup from '$lib/components/elements/card-item-group.svelte';
  import CardItem from '$lib/components/elements/card-item.svelte';
  import ContentHead from '$lib/components/elements/content-head.svelte';

  export let data: PageData;
</script>

<svelte:head>
  <title>{ data.title } • mixel-music</title>
</svelte:head>

{#if data.artistListItem.length > 0}
  <CardItemGroup title={ data.title }>

    {#each data.artistListItem as artist (artist.artisthash)}
      <CardItem>

        <div>
          <ContentHead head={ artist.artist } />
        </div>

      </CardItem>
    {/each}

  </CardItemGroup>
{/if}

<style>
  div {
    padding-top: var(--app-padding-s);
  }
</style>
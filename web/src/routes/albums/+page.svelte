<script lang="ts">
  import type { PageData } from './$types';

  import CardItemGroup from '$lib/components/elements/card-item-group.svelte';
  import CardItem from '$lib/components/elements/card-item.svelte';
  import ContentHead from '$lib/components/elements/content-head.svelte';
  import ContentBody from '$lib/components/elements/content-body.svelte';

  export let data: PageData;
</script>

<svelte:head>
  <title>{ data.title } • mixel-music</title>
</svelte:head>

{#if data.albumListItem.length > 0}
  <CardItemGroup title={ data.title }>

    {#each data.albumListItem as album (album.albumhash)}
      <CardItem
        href="/albums/{ album.albumhash }"
        src={`http://localhost:2843/api/artwork/${ album.albumhash }?size=300`}
        alt="{ album.album }"
        lazyload
      >

        <div>
          <ContentHead head={ album.album } />
          <ContentBody body={ album.albumartist } />
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
<script lang="ts">
  import type { PageData } from './$types';
  import { hash, title, album, artist, imagehash } from '$lib/stores';

  import CardItemGroup from '$lib/components/elements/card-item-group.svelte';
  import CardItem from '$lib/components/elements/card-item.svelte';
  import ContentHead from '$lib/components/elements/content-head.svelte';
  import ContentBody from '$lib/components/elements/content-body.svelte';

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
  <title>{ data.title } • mixel-music</title>
</svelte:head>

{#if data.trackListItem.length > 0}
  <CardItemGroup title={ data.title }>

    {#each data.trackListItem as track (track.hash)}
      <CardItem
        on:click={() => SetTrack(track) }
        src={ `http://localhost:2843/api/images/${ track.imagehash }?size=300` }
        alt={ track.title }
      >
        <div>
          <ContentHead head="{ track.title }" />
          <ContentBody body="{ track.artist }" />
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
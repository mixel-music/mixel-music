<script lang="ts">
  import type { PageData } from './$types';

  import {
    trackHash,
    trackTitle,
    trackAlbum,
    trackArtist,
    albumHash
  } from '$lib/stores/track';

  import CardItemGroup from '$lib/components/elements/card-item-group.svelte';
  import CardItem from '$lib/components/elements/card-item.svelte';
  import ContentHead from '$lib/components/elements/content-head.svelte';
  import ContentBody from '$lib/components/elements/content-body.svelte';

  export let data: PageData;

  function SetTrack(tag: any): void {
    trackHash.set(tag.hash),
    trackTitle.set(tag.title),
    trackAlbum.set(tag.album),
    trackArtist.set(tag.artist),
    albumHash.set(tag.albumhash)
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
        src={ `http://localhost:2843/api/artwork/${ track.albumhash }?size=300` }
        alt={ track.title }
        lazyload
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
<script lang="ts">
  import type { PageData } from './$types';
  import { handleClick, getArtwork, getArtistLink, getAlbumLink } from '$lib/tools';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import CardItem from '$lib/components/elements/CardItem.svelte';
  import CardItemGrid from '$lib/components/elements/CardItemGrid.svelte';

  export let data: PageData;

  let emptySlots = 0;
  if (data.item?.albums && data.item.albums.length < 8) {
    emptySlots = 8 - data.item.albums.length;
  }
</script>

<svelte:head>
  <title>{data.item.artist} • mixel-music</title>
</svelte:head>

{#if data.item}
  <PageTitle title={data.item.artist} />

  <CardItemGrid>
    {#each data.item.albums as album}
      <CardItem
        href='/albums/{ album.albumhash }'
        src={getArtwork(album.albumhash, 300)}
        alt={album.album}
        lazyload
      >
        <div class="info-card">
          <a href='{getAlbumLink(album.albumhash)}'>
            <span class="text">{album.album}</span>
          </a>
          <span class="text-sub">{album.year}</span>
        </div>
      </CardItem>
    {/each}

    {#if emptySlots > 0}
      {#each Array(emptySlots) as _}
        <CardItem Empty />
      {/each}
    {/if}
  </CardItemGrid>
{/if}

<style>

</style>
<script lang="ts">
  import type { PageData } from './$types';
  import { getAlbumLink } from '$lib/tools';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import GridWrap from '$lib/components/elements/GridWrap.svelte';
  import GridItem from '$lib/components/elements/GridItem.svelte';

  export let data: PageData;

  let emptySlots = 0;
  $: { 
    if (data.item?.albums && data.item.albums.length < 8) {
      emptySlots = 8 - data.item.albums.length;
    }
  }
</script>

<svelte:head>
  <title>{data.item.artist} • mixel-music</title>
</svelte:head>

<PageTitle title={data.item.artist} />

{#if data.item}
  <GridWrap>
    {#each data.item.albums as album}
      <GridItem
        href={getAlbumLink(album.albumhash)}
        src={album.albumhash}
        alt={album.album}
        lazyload
      >
        <div class="info-card">
          <a href='{getAlbumLink(album.albumhash)}'>
            <span class="text">{album.album}</span>
          </a>
          <span class="text-sub">{parseInt(album.year.substring(0, 4)) ? `${album.year.substring(0, 4)}` : 'Unknown Year'}</span>
        </div>
      </GridItem>
    {/each}

    {#if emptySlots > 0}
      {#each Array(emptySlots) as _}
        <GridItem Empty />
      {/each}
    {/if}
  </GridWrap>
{/if}
<script lang="ts">
  import type { PageData } from './$types';
  import { handleClick, getArtwork, convertDateTime, getArtistLink, getAlbumLink } from '$lib/tools';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import CardItem from '$lib/components/elements/CardItem.svelte';
  import CardItemGrid from '$lib/components/elements/CardItemGrid.svelte';

  export let data: PageData;
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
          <a href='{getArtistLink(album.albumartisthash)}'>
            <span class="text-sub">{album.year}</span>
          </a>
        </div>
      </CardItem>
    {/each}
  </CardItemGrid>
{/if}

<style>

</style>
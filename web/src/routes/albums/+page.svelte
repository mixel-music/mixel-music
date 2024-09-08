<script lang="ts">
  import Icon from '@iconify/svelte';
  import type { PageData } from './$types';
  import { getAlbumLink, getArtistLink, getNextPage, getPrevPage, getArtwork } from '$lib/tools';

  import ButtonRound from '$lib/components/elements/ButtonRound.svelte';
  import CardItemGrid from '$lib/components/elements/CardItemGrid.svelte';
  import CardItem from '$lib/components/elements/CardItem.svelte';

  export let data: PageData;
</script>

<svelte:head>
  <title>{data.title} • mixel-music</title>
</svelte:head>

{#if data.list}
  <CardItemGrid title={data.title}>
    {#each data.list.list as album (album.albumhash)}
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
            <span class="text-sub">{album.albumartist}</span>
          </a>
        </div>
      </CardItem>
    {/each}
  </CardItemGrid>

  {#if data.list.total > data.item}
    <div class='bottom-ctl'>
      <ButtonRound href={getPrevPage(data.page, data.item)}>
        <Icon icon='iconoir:nav-arrow-left' />
      </ButtonRound>
      <ButtonRound href={
        getNextPage(
          data.page,
          data.item,
          data.list.total
        )
      }>
        <Icon icon='iconoir:nav-arrow-right' />
      </ButtonRound>
    </div>
  {/if}
{/if}

<style>

</style>
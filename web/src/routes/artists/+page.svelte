<script lang="ts">
  import Icon from '@iconify/svelte';
  import type { PageData } from './$types';
  import { getArtistLink, getNextPage, getPrevPage } from '$lib/tools';
  import CardItem from '$lib/components/elements/CardItem.svelte';
  import CardItemGrid from '$lib/components/elements/CardItemGrid.svelte';
  import ButtonRound from '$lib/components/elements/ButtonRound.svelte';

  export let data: PageData;
</script>

<svelte:head>
  <title>{ data.title } • mixel-music</title>
</svelte:head>

{#if data.list}
  <CardItemGrid title={data.title}>
    {#each data.list.list as artist}
      <CardItem
        href='{getArtistLink(artist.artisthash)}'
        src=''
        alt={artist.artist}
        lazyload
        round
      >
        <div class="info-card">
          <a href='{getArtistLink(artist.artisthash)}'>
            <span class="text">{artist.artist}</span>
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
  div {
    text-align: center;
  }
</style>
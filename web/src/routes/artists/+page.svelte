<script lang="ts">
  import Icon from '@iconify/svelte';
  import type { PageData } from './$types';
  import { getArtistLink, getNextPage, getPrevPage } from '$lib/tools';
  import GridWrap from '$lib/components/elements/GridWrap.svelte';
  import GridItem from '$lib/components/elements/GridItem.svelte';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import RoundButton from '$lib/components/elements/RoundButton.svelte';

  export let data: PageData;

  let emptySlots = 0;
  if (data.list?.list && data.list.list.length < 8) {
    emptySlots = 8 - data.list.list.length;
  }
</script>

<svelte:head>
  <title>{ data.title } • mixel-music</title>
</svelte:head>

<PageTitle title={data.title} />

{#if data.list}
  <GridWrap>
    {#each data.list.list as artist}
      <GridItem
        href='{getArtistLink(artist.artist_id)}'
        src=''
        alt={artist.artist}
        lazyload
        round
      >
        <div class="info-card">
          <a href='{getArtistLink(artist.artist_id)}'>
            <span class="text">{artist.artist}</span>
          </a>
        </div>
      </GridItem>
    {/each}

    {#if emptySlots > 0}
      {#each Array(emptySlots) as _}
        <GridItem Empty />
      {/each}
    {/if}
  </GridWrap>

  {#if data.list.total > data.item}
    <div class='bottom-ctl'>
      <RoundButton preload="hover" href={getPrevPage(data.page, data.item)}>
        <Icon icon='iconoir:nav-arrow-left' />
      </RoundButton>
      <RoundButton preload="hover" href={
        getNextPage(
          data.page,
          data.item,
          data.list.total
        )
      }>
        <Icon icon='iconoir:nav-arrow-right' />
      </RoundButton>
    </div>
  {/if}
{/if}

<style>
  div {
    text-align: center;
  }
</style>
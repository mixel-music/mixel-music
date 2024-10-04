<script lang="ts">
  import type { PageData } from './$types';
  import type { ArtistListResponse } from '$lib/interface';
  import {
    removeLinkParams,
    getPaginatedList,
    getArtistLink,
  } from '$lib/tools';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import GridWrap from '$lib/components/elements/GridWrap.svelte';
  import GridItem from '$lib/components/elements/GridItem.svelte';
  import Button from '$lib/components/elements/Button.svelte';
  import { _ } from 'svelte-i18n';

  export let data: PageData;
  let artistList: ArtistListResponse = data.list;
  let currentPage = data.page;
  
  $: emptySlots = artistList?.list.length < 8 ? 8 - artistList.list.length : 0;

  async function changePage(direction: 'next' | 'prev') {
    const itemsPerPage = 48;

    const { newPage, response } = await getPaginatedList(
      fetch,
      direction,
      'artist',
      currentPage,
      itemsPerPage,
      data.list.total,
    );

    currentPage = newPage;
    if (response && response.list) {
      artistList = response.list;
    }

    removeLinkParams(
      { page: currentPage.toString(), item: itemsPerPage.toString() }
    );
  }
</script>

<svelte:head>
  <title>{$_(data.title)} • mixel-music</title>
</svelte:head>

<PageTitle title={$_(data.title)} />

{#if artistList.list}
  <GridWrap>
    {#each artistList.list as artist}
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
      <Button
        button='round'
        preload='hover'
        iconName='iconoir:nav-arrow-left'
        on:click={() => changePage('prev')}
      />
      
      <Button
        button='round'
        preload='hover'
        iconName='iconoir:nav-arrow-right'
        on:click={() => changePage('next')}
      />
    </div>
  {/if}
{/if}

<style>
  .info-card {
    text-align: center;
  }

  a {
    display: unset;
  }
</style>

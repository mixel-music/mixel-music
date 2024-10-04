<script lang="ts">
  import type { PageData } from './$types';
  import type { AlbumListResponse } from '$lib/interface';
  import {
    removeLinkParams,
    getPaginatedList,
    getAlbumLink,
    getArtistLink,
  } from '$lib/tools';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import GridWrap from '$lib/components/elements/GridWrap.svelte';
  import GridItem from '$lib/components/elements/GridItem.svelte';
  import Button from '$lib/components/elements/Button.svelte';
  import { _ } from 'svelte-i18n';

  export let data: PageData;
  let albumList: AlbumListResponse = data.list;
  let currentPage = data.page;
  
  $: emptySlots = albumList?.list.length < 8 ? 8 - albumList.list.length : 0;

  async function changePage(direction: 'next' | 'prev') {
    const itemsPerPage = 48;

    const { newPage, response } = await getPaginatedList(
      fetch,
      direction,
      'album',
      currentPage,
      itemsPerPage,
      data.list.total,
    );

    currentPage = newPage;
    if (response && response.list) {
      albumList = response.list;
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

{#if albumList.list}
  <GridWrap>
    {#each albumList.list as album (album.album_id)}
      <GridItem
        href={getAlbumLink(album.album_id)}
        src={album.album_id}
        alt={album.album ? album.album : $_('unknown_album')}
        lazyload
      >
        <div class="info-card">
          <a href='{getAlbumLink(album.album_id)}'>
            <span class="text">{album.album ? album.album : $_('unknown_album')}</span>
          </a>
          <a href='{getArtistLink(album.albumartist_id)}'>
            <span class="text-sub">{album.albumartist}</span>
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

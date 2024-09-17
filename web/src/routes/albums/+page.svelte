<script lang="ts">
  import Icon from '@iconify/svelte';
  import type { PageData } from './$types';
  import {
    getAlbumLink,
    getArtistLink,
    getNextPage,
    getPrevPage,
  } from '$lib/tools';
  import RoundButton from '$lib/components/elements/RoundButton.svelte';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import GridWrap from '$lib/components/elements/GridWrap.svelte';
  import GridItem from '$lib/components/elements/GridItem.svelte';
  import { _ } from 'svelte-i18n'

  export let data: PageData;

  let emptySlots = 0;
  if (data.list?.list && data.list.list.length < 8) {
    emptySlots = 8 - data.list.list.length;
  }
</script>

<svelte:head>
  <title>{$_(data.title)} • mixel-music</title>
</svelte:head>

<PageTitle title={$_(data.title)} />

{#if data.list}
  <GridWrap>
    {#each data.list.list as album (album.album_id)}
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
      <RoundButton href={getPrevPage(data.page, data.item)} preload="hover">
        <Icon icon='iconoir:nav-arrow-left' />
      </RoundButton>
      
      <RoundButton
        href={getNextPage(
          data.page,
          data.item,
          data.list.total
        )}
        preload="hover"
      >
        <Icon icon='iconoir:nav-arrow-right' />
      </RoundButton>
    </div>
  {/if}
{/if}
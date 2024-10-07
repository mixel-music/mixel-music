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
  let startNumber: number = data.start;
  let endNumber: number = data.end

  async function changePage(direction: 'next' | 'prev') {
    const { newStart, newEnd, response } = await getPaginatedList(
      fetch,
      direction,
      'album',
      data.list.total,
      startNumber,
      40,
    );

    startNumber = newStart;
    endNumber = newEnd;
    console.debug(startNumber, endNumber);

    if (response) {
      albumList = { list: [...response.list.list], total: response.list.total };
      console.debug(albumList);
    }

    removeLinkParams(
      { start: startNumber.toString(), end: (endNumber).toString() }
    );
  }
</script>

<svelte:head>
  <title>{$_(data.title)} • mixel-music</title>
</svelte:head>

<PageTitle title={$_(data.title)} />

<GridWrap
  items={albumList.list}
  bind:startNumber={startNumber}
  bind:endNumber={endNumber}
>
  <GridItem
    let:item
    slot="GridItem"
    href={getAlbumLink(item.album_id)}
    src={item.album_id}
    alt={item.album ? item.album : $_('unknown_album')}
    lazyload
  >
    <div class="info-card">
      <a href={getAlbumLink(item.album_id)}>
        <span class="text">{item.album ? item.album : $_('unknown_album')}</span>
      </a>
      <a href={getArtistLink(item.albumartist_id)}>
        <span class="text-sub">{item.albumartist}</span>
      </a>
    </div>
  </GridItem>
</GridWrap>

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
    disabled={data.end + (data.end - data.start) >= data.list.total}
    on:click={() => changePage('next')}
  />
</div>

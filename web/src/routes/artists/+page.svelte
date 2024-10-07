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
  let startNumber: number = data.start;
  let endNumber: number = data.end
  
  async function changePage(direction: 'next' | 'prev') {
    const { newStart, newEnd, response } = await getPaginatedList(
      fetch,
      direction,
      'artist',
      data.list.total,
      startNumber,
      40,
    );

    startNumber = newStart;
    endNumber = newEnd;
    console.debug(startNumber, endNumber);

    if (response) {
      artistList = { list: [...response.list.list], total: response.list.total };
      console.debug(artistList);
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
  items={artistList.list}
  bind:startNumber={startNumber}
  bind:endNumber={endNumber}
>
  <GridItem
    let:item
    slot="GridItem"
    href={getArtistLink(item.artist_id)}
    alt={item.artist}
    lazyload
    round
  >
    <div class="info-card">
      <a href='{getArtistLink(item.artist_id)}'>
        <span class="text">{item.artist}</span>
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

<style>
  .info-card {
    display: flex;
    justify-content: center;
  }

  a {
    display: unset;
  }
</style>

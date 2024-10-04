<script lang="ts">
  import type { PageData } from './$types';
  import type { TrackListResponse } from '$lib/interface';
  import {
    removeLinkParams,
    getPaginatedList,
  } from '$lib/tools';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import ControlsBar from '$lib/components/ControlsBar.svelte';
  import TrackTable from '$lib/components/TrackTable.svelte';
  import Button from '$lib/components/elements/Button.svelte';
  import { _ } from 'svelte-i18n';

  export let data: PageData;
  let trackList: TrackListResponse = data.list;
  let currentPage = data.page;

  async function changePage(direction: 'next' | 'prev') {
    const itemsPerPage = 48;
    const { newPage, response } = await getPaginatedList(
      fetch,
      direction,
      'track',
      currentPage,
      itemsPerPage,
      data.list.total,
    );

    currentPage = newPage;
    if (response && response.list) {
      trackList = response.list;
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

{#if data.list}
  <ControlsBar tracks={trackList.list} />
  <TrackTable list={trackList.list} />

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

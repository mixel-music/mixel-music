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
  let startNumber: number = data.start;
  let endNumber: number = data.end

  async function changePage(direction: 'next' | 'prev') {
    const { newStart, newEnd, response } = await getPaginatedList(
      fetch,
      direction,
      'track',
      data.list.total,
      startNumber,
      40,
    );

    startNumber = newStart;
    endNumber = newEnd;
    console.debug(startNumber, endNumber);

    if (response) {
      trackList = { list: [...response.list.list], total: response.list.total };
      console.debug(trackList);
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

{#if data.list}
  <div style="margin-bottom: var(--space-s);">
    <ControlsBar trackItems={trackList.list} />
  </div>

  <TrackTable list={trackList.list} />

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
{/if}

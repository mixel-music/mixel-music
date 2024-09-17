<script lang="ts">
  import Icon from '@iconify/svelte';
  import type { PageData } from './$types';
  import { getNextPage, getPrevPage } from '$lib/tools';
  import RoundButton from '$lib/components/elements/RoundButton.svelte';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import TrackTables from '$lib/components/TrackTables.svelte';
  import ControlsBar from '$lib/components/ControlsBar.svelte';
  import { _ } from 'svelte-i18n'

  export let data: PageData;
</script>

<svelte:head>
  <title>{$_(data.title)} • mixel-music</title>
</svelte:head>

<PageTitle title={$_(data.title)} />

{#if data.list}
  <ControlsBar />
  <TrackTables list={data.list.list} />

  {#if data.list.total > data.item}
    <div class='bottom-ctl'>
      <RoundButton href={getPrevPage(data.page, data.item)} preload="hover">
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
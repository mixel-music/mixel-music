<script lang="ts">
  import type { PageData } from './$types';
  import { getNextPage, getPrevPage } from '$lib/tools';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import ControlsBar from '$lib/components/ControlsBar.svelte';
  import TrackTable from '$lib/components/TrackTable.svelte';
  import Button from '$lib/components/elements/Button.svelte';
  import { _ } from 'svelte-i18n'

  export let data: PageData;
</script>

<svelte:head>
  <title>{$_(data.title)} • mixel-music</title>
</svelte:head>

<PageTitle title={$_(data.title)} />

{#if data.list}
  <ControlsBar tracks={data.list.list} />
  <TrackTable list={data.list.list} />

  {#if data.list.total > data.item}
    <div class='bottom-ctl'>
      <Button
        button='round'
        preload='hover'
        iconName='iconoir:nav-arrow-left'
        href={getPrevPage(data.page, data.item)}
      />
      
      <Button
        button='round'
        preload='hover'
        iconName='iconoir:nav-arrow-right'
        href={getNextPage(
          data.page,
          data.item,
          data.list.total
        )}
      />
    </div>
  {/if}
{/if}

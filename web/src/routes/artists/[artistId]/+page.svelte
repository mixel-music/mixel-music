<script lang="ts">
  import type { PageData } from './$types';
  import { getAlbumLink } from '$lib/tools';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import GridWrap from '$lib/components/elements/GridWrap.svelte';
  import GridItem from '$lib/components/elements/GridItem.svelte';
  import { _ } from 'svelte-i18n'

  export let data: PageData;
  let startNumber: number = 1;
  let endNumber: number = 2;
</script>

<svelte:head>
  <title>{data.item.artist} • mixel-music</title>
</svelte:head>

<PageTitle title={data.item.artist} />

{#if data.item}
  <GridWrap
    items={data.item.albums}
    bind:startNumber={startNumber}
    bind:endNumber={endNumber}
  >
    <GridItem
      let:item
      slot="GridItem"
      href={getAlbumLink(item.album_id)}
      src={item.album_id}
      alt={item.album}
      lazyload
    >
      <div class="info-card">
        <a href='{getAlbumLink(item.album_id)}'>
          <span class="text">{item.album ? item.album : $_('unknown_album')}</span>
        </a>
        <span class="text-sub">
          {item.year != 0 ? $_('info.year',{values: {year: item.year}}) : $_('unknown_year')}
        </span>
      </div>
    </GridItem>
  </GridWrap>
{/if}

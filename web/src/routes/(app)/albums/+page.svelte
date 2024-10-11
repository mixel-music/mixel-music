<script lang="ts">
  import type { PageData } from './$types';
  import type { AlbumListResponse } from '$lib/interface';
  import { getPaginatedList, getAlbumLink, getArtistLink } from '$lib/tools';
  import InfiniteScroll from '$lib/components/interactions/InfiniteScroll.svelte';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import GridWrap from '$lib/components/elements/GridWrap.svelte';
  import GridItem from '$lib/components/elements/GridItem.svelte';
  import { _ } from 'svelte-i18n';

  export let data: PageData;
  let albumList: AlbumListResponse = data.list;
  let startNumber = data.start;
  let loading = false;

  async function loadMoreAlbums() {
    if (loading || (startNumber + 39) >= albumList.total) return;
    loading = true;

    const { newStart, response } = await getPaginatedList(
      fetch, 'next', 'album', albumList.total, startNumber, 39,
    );

    startNumber = newStart;
    if (response) {
      albumList = {
        list: [...albumList.list, ...response.list.list],
        total: response.list.total,
      };
    }

    loading = false;
  }
</script>

<svelte:head>
  <title>{$_(data.title)} • mixel-music</title>
</svelte:head>

<PageTitle title={$_(data.title)} />

<InfiniteScroll threshold={100} on:loadMore={loadMoreAlbums}>
  <GridWrap items={albumList.list}>
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
</InfiniteScroll>

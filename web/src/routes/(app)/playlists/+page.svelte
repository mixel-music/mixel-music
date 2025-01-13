<script lang="ts">
  import type { PageData } from './$types';
  import type { PlaylistsResponse } from '$lib/interface';
  import { getPaginatedList, getAlbumLink, getArtistLink } from '$lib/tools';
  import InfiniteScroll from '$lib/components/interactions/InfiniteScroll.svelte';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import GridWrap from '$lib/components/elements/GridWrap.svelte';
  import GridItem from '$lib/components/elements/GridItem.svelte';
  import GridItemDetail from '$lib/components/elements/GridItemDetail.svelte';
  import { _ } from 'svelte-i18n';

  export let data: PageData;
  let playlists: PlaylistsResponse = data.playlists;
  let startNumber = data.start;
  let loading = false;

  async function loadMoreAlbums() {
    if (loading || (startNumber + 39) >= playlists.total) return;
    loading = true;

    const { newStart, response } = await getPaginatedList(
      fetch, 'next', 'playlist', playlists.total, startNumber, 39,
    );

    startNumber = newStart;
    if (response) {
      playlists = {
        playlists: [...playlists.playlists, ...response.response.playlists],
        total: response.response.total,
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
  <GridWrap items={playlists.playlists}>
    <GridItem
      let:item
      slot="GridItem"
      href={getAlbumLink(item.playlist_id)}
      src={item.playlist_id}
      alt={item.playlist_name ? item.playlist_name : $_('unknown_album')}
    >
      <GridItemDetail
        title={item.playlist_name ? item.playlist_name : $_('unknown_album')}
        titleHref={getAlbumLink(item.playlist_id)}
        sub={item.playlist_id}
        subHref={getArtistLink(item.playlist_id)}
      />
    </GridItem>
  </GridWrap>
</InfiniteScroll>

<script lang="ts">
  import type { PageData } from './$types';
  import type { ArtistsResponse } from '$lib/interface';
  import { getPaginatedList, getArtistLink } from '$lib/tools';
  import InfiniteScroll from '$lib/components/interactions/InfiniteScroll.svelte';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import GridWrap from '$lib/components/elements/GridWrap.svelte';
  import GridItem from '$lib/components/elements/GridItem.svelte';
  import GridItemDetail from '$lib/components/elements/GridItemDetail.svelte';
  import { _ } from 'svelte-i18n';

  export let data: PageData;
  let artists: ArtistsResponse = data.artists;
  let startNumber = data.start;
  let loading = false;
  
  async function loadMoreArtists() {
    if (loading || (startNumber + 39) >= artists.total) return;
    loading = true;

    const { newStart, response } = await getPaginatedList(
      fetch, 'next', 'artist', artists.total, startNumber, 39,
    );

    startNumber = newStart;
    if (response) {
      artists = {
        artists: [...artists.artists, ...response.response.artists],
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

<InfiniteScroll threshold={100} on:loadMore={loadMoreArtists}>
  <GridWrap items={artists.artists}>
    <GridItem
      let:item
      slot="GridItem"
      href={getArtistLink(item.artist_id)}
      alt={item.artist}
      lazyload
      round
    >
      <GridItemDetail
        center
        title={item.artist}
        titleHref={getArtistLink(item.artist_id)}
        sub={item.albumartist}
        subHref={getArtistLink(item.albumartist_id)}
      />
    </GridItem>
  </GridWrap>
</InfiniteScroll>

<script lang="ts">
  import type { PageData } from './$types';
  import type { ArtistListResponse } from '$lib/interface';
  import { getPaginatedList, getAlbumLink, getArtistLink } from '$lib/tools';
  import InfiniteScroll from '$lib/components/interactions/InfiniteScroll.svelte';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';
  import GridWrap from '$lib/components/elements/GridWrap.svelte';
  import GridItem from '$lib/components/elements/GridItem.svelte';
  import { _ } from 'svelte-i18n';

  export let data: PageData;
  let artistList: ArtistListResponse = data.list;
  let startNumber = data.start;
  let loading = false;
  
  async function loadMoreArtists() {
    if (loading || (startNumber + 39) >= artistList.total) return;
    loading = true;

    const { newStart, response } = await getPaginatedList(
      fetch, 'next', 'artist', artistList.total, startNumber, 39,
    );

    startNumber = newStart;
    if (response) {
      artistList = {
        list: [...artistList.list, ...response.list.list],
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

<InfiniteScroll threshold={100} on:loadMore={loadMoreArtists}>
  <GridWrap items={artistList.list}>
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
</InfiniteScroll>

<style>
  a {
    display: unset;
    text-align: center;
  }
</style>

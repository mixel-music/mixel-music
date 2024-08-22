<script lang="ts">
  import type { PageData } from './$types';
  import { getArtwork, getNextPage, getPrevPage } from '$lib/tools';
  import { trackStore } from '$lib/stores/track-store';
  import { initTrack } from '$lib/newponents/layouts/player/controls';

  import CardItemGroup from '$lib/components/elements/card-item-group.svelte';
  import CardItem from '$lib/components/elements/card-item.svelte';
  import ContentHead from '$lib/components/elements/text-title.svelte';
  import ContentBody from '$lib/components/elements/text-sub.svelte';
  import RdButton from '$lib/newponents/elements/rd-button.svelte';
  import Icon from '@iconify/svelte';

  export let data: PageData;
</script>

<svelte:head>
  <title>{data.title} • mixel-music</title>
</svelte:head>

{#if data.list}
  <CardItemGroup title={data.title}>
    {#each data.list.list as track (track.hash)}
      <CardItem
        on:click={() => initTrack(
          track.hash,
          track.title,
          track.album,
          track.artist,
          track.albumhash,
        )}
        src={getArtwork(track.albumhash, 300)}
        alt={track.title}
        lazyload
      >
        <div>
          <ContentHead head={track.title} />
          <ContentBody body={track.artist} />
        </div>
      </CardItem>
    {/each}
  </CardItemGroup>

  {#if data.list.total > data.item}
    <div class='bottom-ctl'>
      <RdButton href={getPrevPage(data.page, data.item)}>
        <Icon icon='iconoir:nav-arrow-left' />
      </RdButton>
      <RdButton href={
        getNextPage(
          data.page,
          data.item,
          data.list.total
        )
      }>
        <Icon icon='iconoir:nav-arrow-right' />
      </RdButton>
    </div>
  {/if}
{/if}

<style>
  div {
    padding-top: var(--app-padding-s);
  }

  .bottom-ctl {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
  }
</style>
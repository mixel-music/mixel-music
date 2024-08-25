<script lang="ts">
  import Icon from '@iconify/svelte';
  import type { PageData } from './$types';
  import { getArtwork, getNextPage, getPrevPage } from '$lib/tools';
  import audioElement from '$lib/stores/stores';

  import ButtonRd from '$lib/newponents/elements/button-rd.svelte';
  import CardItemGroup from '$lib/components/elements/card-item-group.svelte';
  import CardItem from '$lib/components/elements/card-item.svelte';
  import ContentHead from '$lib/components/elements/text-title.svelte';
  import ContentBody from '$lib/components/elements/text-sub.svelte';
  import type { TrackList } from '$lib/interface';

  export let data: PageData;

  const playTrack = (track: TrackList) => {
    audioElement.addTrack({
      hash: track.hash,
      title: track.title,
      album: track.album,
      artist: track.artist,
      albumhash: track.albumhash,
    });

    const trackIndex = audioElement.getState().trackList.length - 1;
    if (trackIndex === 0) {
      audioElement.setTrack(trackIndex);
    }
  }
</script>

<svelte:head>
  <title>{data.title} • mixel-music</title>
</svelte:head>

{#if data.list}
  <CardItemGroup title={data.title}>
    {#each data.list.list as track (track.hash)}
      <CardItem
        on:click={() => playTrack(track)}
        src={track.album == 'Unknown Album' ? getArtwork(track.hash, 300) : getArtwork(track.albumhash, 300)}
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
      <ButtonRd href={getPrevPage(data.page, data.item)}>
        <Icon icon='iconoir:nav-arrow-left' />
      </ButtonRd>
      <ButtonRd href={
        getNextPage(
          data.page,
          data.item,
          data.list.total
        )
      }>
        <Icon icon='iconoir:nav-arrow-right' />
      </ButtonRd>
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
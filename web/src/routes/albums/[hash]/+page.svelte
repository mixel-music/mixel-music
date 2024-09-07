<script lang="ts">
  import type { PageData } from './$types';
  import { getArtwork, convertDateTime, convertFileSize } from '$lib/tools';
  import PlayerService from '$lib/stores/stores';
  import Artwork from '$lib/components/elements/ArtworkImage.svelte';
  import AlbumTitle from '$lib/components/elements/AlbumHeader.svelte';
  import ButtonSq from '$lib/components/elements/ButtonSquare.svelte';
  import Table from '$lib/components/elements/Table.svelte';
  import TableItem from '$lib/components/elements/TableItem.svelte';

  export let data: PageData;

  function handleClick(item: any) {
    PlayerService.addTrack({
      hash: item.hash,
      title: item.title,
      album: data.item.album,
      artist: item.artist,
      albumhash: data.item.albumhash,
    }, 0);

    PlayerService.setTrack(0);
  }

  let columns = ['#', 'Title', 'Artist', 'Time'];
  let columnsRatios = [0.1, 4, 2, 1];
  let rows = data.item.tracks.map(item => ({
    row: [
      item.track != 0 ? item.track : '',
      item.title,
      item.artist,
      convertDateTime(item.duration),
    ],
    onClick: () => handleClick(item)
  }));
</script>

{#if data.item}
  <div class="album-header">
    <Artwork
      src={getArtwork(data.item.albumhash, 500)}
      alt={data.item.album}
      width={230}
      height={230}
    />

    <AlbumTitle
      album={data.item.album}
      albumartist={data.item.albumartist}
      year={data.item.year}
      totalTracks={data.item.tracktotals}
      totalLength={convertDateTime(data.item.durationtotals)}
      comment={data.item.tracks[0].comment}
      size={convertFileSize(data.item.sizetotals)}
    />
  </div>

  <div class="album-action">
    <ButtonSq
      href='.'
      width='150px'
      height='50px'
    >
      Play
    </ButtonSq>

    <ButtonSq
      href='.'
      width='150px'
      height='50px'
    >
      Shuffle
    </ButtonSq>
  </div>

  <div class="album-tracks">
    <Table headers={columns} columnRatios={columnsRatios}>
      {#each rows as { row, onClick }}
        <TableItem row={row} columnRatios={columnsRatios} onClick={onClick} />
      {/each}
    </Table>
  </div>
{/if}

<style>
  .album-header {
    display: flex;
    margin-top: 2em;
    gap: 24px;
  }

  .album-action {
    display: flex;
    margin-top: 24px;
    gap: 12px;
  }

  .album-tracks {
    margin-top: 24px;
  }
</style>
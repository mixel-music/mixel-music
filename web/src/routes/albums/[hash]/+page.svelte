<script lang="ts">
  import type { PageData } from './$types';
  import { handleClick, getArtwork, convertDateTime, convertFileSize, getArtistLink } from '$lib/tools';

  import Table from '$lib/components/elements/Table.svelte';
  import TableHead from '$lib/components/elements/TableHead.svelte';
  import TableHeadItem from '$lib/components/elements/TableHeadItem.svelte';
  import TableBody from '$lib/components/elements/TableBody.svelte';
  import TableBodyItem from '$lib/components/elements/TableBodyItem.svelte';
  import AlbumHeader from '$lib/components/elements/AlbumHeader.svelte';
  import ArtworkImage from '$lib/components/elements/ArtworkImage.svelte';
  import ButtonSquare from '$lib/components/elements/ButtonSquare.svelte';
  import TableMenu from '$lib/components/TableMenu.svelte';

  export let data: PageData;
</script>

<svelte:head>
  <title>{data.item.album} / {data.item.albumartist} • mixel-music</title>
</svelte:head>

{#if data.item}
  <div class="album-header">
    <ArtworkImage
      src={getArtwork(data.item.albumhash, 500)}
      alt={data.item.album}
      width={230}
      height={230}
    />

    <AlbumHeader
      album={data.item.album}
      albumartist={data.item.albumartist}
      year={data.item.year}
      totalTracks={data.item.tracktotals}
      totalLength={convertDateTime(data.item.durationtotals)}
      comment={data.item.tracks[0].comment}
      size={convertFileSize(data.item.sizetotals)}
      albumartisthash={data.item.albumartisthash}
    />
  </div>

  <div class="album-action">
    <ButtonSquare
      href='.'
      width='150px'
      height='50px'
    >
      Play
    </ButtonSquare>

    <ButtonSquare
      href='.'
      width='150px'
      height='50px'
    >
      Shuffle
    </ButtonSquare>
  </div>

  <div class="album-tracks">

    <Table>
      <TableHead>
        <TableHeadItem size='xs'>#</TableHeadItem>
        <TableHeadItem size='xl'>Title</TableHeadItem>
        <TableHeadItem size='m'>Artist</TableHeadItem>
        <TableHeadItem size="s">Time</TableHeadItem>
        <TableHeadItem size="xs"></TableHeadItem>
      </TableHead>

      {#each data.item.tracks as item}
        <TableBody>
          <TableBodyItem size='xs'>{item.track}</TableBodyItem>
          <TableBodyItem size='xl'>
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <!-- svelte-ignore a11y-missing-attribute -->
            <a on:click={handleClick(item, true)} on:keydown>
              {item.title}
            </a>
          </TableBodyItem>

          <TableBodyItem size='m'>
            <a href='{getArtistLink(item.artisthash)}'>
              {item.artist}
            </a>
          </TableBodyItem>

          <TableBodyItem size='s'>{convertDateTime(item.duration)}</TableBodyItem>
          <TableBodyItem size='xs'>
            <TableMenu />
          </TableBodyItem>
        </TableBody>
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
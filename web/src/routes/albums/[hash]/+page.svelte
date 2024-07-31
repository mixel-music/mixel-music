<script lang="ts">
  import type { PageData } from './$types';
  import { getFormattedTime, getCoverUrl } from '$lib/tools';

  import {
    trackHash,
    trackTitle,
    trackAlbum,
    trackArtist,
    trackImages,
  } from '$lib/stores/track';

  import AlbumCover from '$lib/components/albums/album-cover.svelte';
  import AlbumTitle from '$lib/components/albums/album-header.svelte';
  import TableBody from '$lib/components/elements/table-body.svelte';
  import TableCell from '$lib/components/elements/table-data.svelte';
  import TableRow from '$lib/components/elements/table-row.svelte';

  export let data: PageData;

  function SetTrack(tag: any): void {
    trackHash.set(tag.hash),
    trackTitle.set(tag.title),
    trackAlbum.set(data.albumItem.album),
    trackArtist.set(tag.artist), 
    trackImages.set(data.albumItem.imagehash)
  }
</script>

<div class="album-container">
  <AlbumCover
    src={ getCoverUrl(data.albumItem.imagehash, 500) }
    alt={ data.albumItem.album }
    width=256
    height=256
  />

  <AlbumTitle
    album={ data.albumItem.album }
    albumartist={ data.albumItem.albumartist }
    year={ data.albumItem.year }
    totalTracks={ data.albumItem.tracktotals }
    totalLength={ getFormattedTime(data.albumItem.durationtotals) }
  />
</div>

<div class="album-content">

<TableBody>

  {#each data.albumItem.tracks as album}

    <TableRow
      on:click={() => SetTrack(album)}
    >

      <TableCell bold text={ album.tracknumber } />
      <TableCell large text={ album.title } />
      <TableCell right text={ album.artist } />
      <TableCell right text={ getFormattedTime(album.duration) } />

    </TableRow>

  {/each}

</TableBody>

</div>

<style>
  .album-container {
    display: flex;
    width: 70%;
    margin: 0 auto;
    margin-top: 2em;
    gap: 24px;
  }

  .album-content {
    padding-top: var(--app-padding-l);
  }
</style>
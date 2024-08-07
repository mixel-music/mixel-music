<script lang="ts">
  import type { PageData } from './$types';
  import { getArtwork, convertDateTime, convertFileSize } from '$lib/tools';
  import { hash, title, album, artist, albumhash } from '$lib/stores/track';

  import AlbumCover from '$lib/components/albums/album-cover.svelte';
  import AlbumTitle from '$lib/components/albums/album-header.svelte';
  import TableBody from '$lib/components/elements/table-body.svelte';
  import TableCell from '$lib/components/elements/table-data.svelte';
  import TableRow from '$lib/components/elements/table-row.svelte';

  export let data: PageData;

  function SetTrack(tag: any): void {
    hash.set(tag.hash),
    title.set(tag.title),
    album.set(data.albumItem.album),
    artist.set(tag.artist)
    albumhash.set(data.albumItem.albumhash)
  }
</script>

<div class="album-container">
  <AlbumCover
    src={ getArtwork(data.albumItem.albumhash, 500) }
    alt={ data.albumItem.album }
    width=230
    height=230
  />

  <AlbumTitle
    album={ data.albumItem.album }
    albumartist={ data.albumItem.albumartist }
    year={ data.albumItem.year }
    totalTracks={ data.albumItem.tracktotals }
    totalLength={ convertDateTime(data.albumItem.durationtotals) }
    comment={ data.albumItem.tracks[0].comment }
    size={ convertFileSize(data.albumItem.sizetotals) }
  />
</div>

<div class="album-content">
<TableBody>
  {#each data.albumItem.tracks as album}
    <TableRow on:click={() => SetTrack(album)}>

      <TableCell sub text={ album.track !== 0 ? album.track : '-' } />
      <TableCell large text={ album.title } />
      <TableCell right text={ album.artist } />
      <TableCell sub right text={ convertDateTime(album.duration) } />

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
</style>
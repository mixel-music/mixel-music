<script lang="ts">
  import type { PageData } from './$types';
  import { getArtwork, convertDateTime, convertFileSize } from '$lib/tools';
  import PlayerService from '$lib/stores/stores';

  import Artwork from '$lib/newponents/elements/artwork.svelte';
  import AlbumTitle from '$lib/components/albums/album-header.svelte';
  import TableBody from '$lib/components/elements/table-body.svelte';
  import TableCell from '$lib/components/elements/table-data.svelte';
  import TableRow from '$lib/components/elements/table-row.svelte';

  export let data: PageData;
</script>

{#if data.item}
  <div class="album-container">
  <Artwork
    src={ getArtwork(data.item.albumhash, 500) }
    alt={ data.item.album }
    width=230
    height=230
  />

  <AlbumTitle
    album={ data.item.album }
    albumartist={ data.item.albumartist }
    year={ data.item.year }
    totalTracks={ data.item.tracktotals }
    totalLength={ convertDateTime(data.item.durationtotals) }
    comment={ data.item.tracks[0].comment }
    size={ convertFileSize(data.item.sizetotals) }
  />
  </div>

  <div class="album-content">
  <TableBody>
  {#each data.item.tracks as album}
    <TableRow on:click={() => {
      PlayerService.addTrack({
        hash: album.hash,
        title: album.title,
        album: data.item.album,
        artist: album.artist,
        albumhash: data.item.albumhash,
      }, 0)
      PlayerService.setTrack(0)
    }
  }>

      <TableCell sub text={ album.track !== 0 ? album.track : '-' } />
      <TableCell large text={ album.title } />
      <TableCell right text={ album.artist } />
      <TableCell sub right text={ convertDateTime(album.duration) } />

    </TableRow>
  {/each}
  </TableBody>
  </div>
{/if}

<style>
  .album-container {
    display: flex;
    margin-top: 2em;
    gap: 24px;
  }
</style>
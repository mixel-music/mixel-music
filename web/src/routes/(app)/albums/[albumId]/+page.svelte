<script lang="ts">
  import type { PageData } from './$types';
  import AlbumHeader from '$lib/components/AlbumHeader.svelte';
  import AlbumTable from '$lib/components/AlbumTable.svelte';
  import { _ } from 'svelte-i18n';

  export let data: PageData;
</script>

<svelte:head>
  <title>
    {data.item.album
      ? data.item.album : $_('unknown_album')
    } / {data.item.albumartist} • mixel-music
  </title>
</svelte:head>

{#if data.item}
  <AlbumHeader
    album={data.item.album}
    albumId={data.item.album_id}
    albumArtist={data.item.albumartist}
    albumArtistId={data.item.albumartist_id}
    comment={data.item.tracks[0].comment}
    durationTotal={data.item.duration_total}
    fileSizeTotal={data.item.filesize_total}
    trackTotal={data.item.tracks.length}
    year={data.item.year != 0 ? data.item.year : $_('unknown_year')}
    trackItems={data.item.tracks.map(track => ({
      ...track,
      album: data.item.album,
      album_id: data.item.album_id}
    ))}
  />
  
  <AlbumTable list={data.item} />
{/if}

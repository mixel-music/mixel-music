<script lang="ts">
  import type { PageData } from './$types';
  import AlbumHeader from '$lib/components/AlbumHeader.svelte';
  import ControlsBar from '$lib/components/ControlsBar.svelte';
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
    album_id={data.item.album_id}
    albumartist={data.item.albumartist}
    albumartist_id={data.item.albumartist_id}
    comment={data.item.tracks[0].comment}
    duration_total={data.item.duration_total}
    filesize_total={data.item.filesize_total}
    track_total={data.item.tracks.length}
    year={data.item.year != 0 ? data.item.year : $_('unknown_year')}
  />

  <ControlsBar tracks={data.item.tracks.map(track => ({
    ...track,
    album: data.item.album,
    album_id: data.item.album_id
  }))} />
  
  <AlbumTable list={data.item} />
{/if}
<script lang="ts">
  import type { PageData } from './$types';
  import AlbumTables from '$lib/components/AlbumTables.svelte';
  import AlbumHeader from '$lib/components/AlbumHeader.svelte';
  import ControlsBar from '$lib/components/ControlsBar.svelte';

  export let data: PageData;
</script>

<svelte:head>
  <title>{data.item.album} / {data.item.albumartist} • mixel-music</title>
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
    year={data.item.year}
  />

  <ControlsBar />
  <AlbumTables list={data.item} />
{/if}
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
    albumartist={data.item.albumartist}
    year={data.item.year}
    totalTracks={data.item.tracks.length}
    totalLength={data.item.total_duration}
    comment={data.item.tracks[0].comment}
    size={data.item.total_filesize}
    albumhash={data.item.album_id}
    albumartisthash={data.item.albumartist_id}
  />

  <ControlsBar />
  <AlbumTables list={data.item} />
{/if}
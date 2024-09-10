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
    totalTracks={data.item.tracktotals}
    totalLength={data.item.durationtotals}
    comment={data.item.tracks[0].comment}
    size={data.item.sizetotals}
    albumhash={data.item.albumhash}
    albumartisthash={data.item.albumartisthash}
  />

  <ControlsBar />
  <AlbumTables list={data.item} />
{/if}
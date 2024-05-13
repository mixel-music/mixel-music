<script lang="ts">
  import type { PageData } from './$types';
  import { getCoverUrl } from '$lib/tools';

  import AlbumCover from '$lib/components/albums/album-cover.svelte';
  import AlbumTitle from '$lib/components/albums/album-header.svelte';

  export let data: PageData;
</script>

<AlbumCover
  src={ getCoverUrl(data.albumItem.imagehash, 500) }
  alt={ data.albumItem.album }
  width=256
  height=256
/>

<AlbumTitle title={ data.albumItem.album } />

{ data.albumItem.albumartist }

{ data.albumItem.tracktotals } Tracks

<style>

</style>
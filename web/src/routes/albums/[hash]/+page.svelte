<script lang="ts">
  import type { PageData } from './$types';
  import { getFormattedTime } from '$lib/tools';
  import { getCoverUrl } from '$lib/tools';

  import AlbumCover from '$lib/components/albums/album-cover.svelte';
  import AlbumTitle from '$lib/components/albums/album-header.svelte';

  export let data: PageData;
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

<div>

</div>

<style>
  .album-container {
    display: flex;
    width: 70%;
    gap: 24px;
  }
</style>
<script lang="ts">
  import type { PageData } from './$types';
  import { getFormattedTime } from '$lib/tools';
  import { getCoverUrl } from '$lib/tools';

  import AlbumCover from '$lib/components/albums/album-cover.svelte';
  import AlbumTitle from '$lib/components/albums/album-header.svelte';
  import ContentHead from '$lib/components/elements/content-head.svelte';
  import ContentBody from '$lib/components/elements/content-body.svelte';

  import TableBody from '$lib/components/elements/table-body.svelte';
  import TableBodyRow from '$lib/components/elements/table-body-row.svelte';
  import TableCell from '$lib/components/elements/table-cell.svelte';

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

<div class="album-content">

<TableBody>

  <TableBodyRow>

  {#each data.albumItem.tracks as album}
    <TableCell text={ album.tracknumber } />
  {/each}

  </TableBodyRow>

  <TableBodyRow title>

  {#each data.albumItem.tracks as album}
    <TableCell text={ album.title } />
  {/each}

  </TableBodyRow>

  <TableBodyRow>

  {#each data.albumItem.tracks as album}
    <TableCell text={ album.artist } />
  {/each}

  </TableBodyRow>

  <TableBodyRow>

  {#each data.albumItem.tracks as album}
    <TableCell text={ getFormattedTime(album.duration) } />
  {/each}

  </TableBodyRow>

</TableBody>

</div>

<!--{#each data.albumItem.tracks as album}
<div>
  <ContentHead head={ album.title } />
  <ContentBody body={ album.artist } />
</div>
{/each}-->

<style>
  .album-container {
    display: flex;
    width: 70%;
    gap: 24px;
  }

  .album-content {
    padding-top: var(--app-padding-l);
  }
</style>
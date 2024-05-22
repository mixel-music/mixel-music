<script lang="ts">
  export let album: string;
  export let albumartist: string;
  export let year: number | undefined;
  export let totalTracks: number;
  export let totalLength: number | string;
</script>

<div class="album-header">
  <span class="album-name">
    {album}
  </span>

  <span class="album-info">
    {albumartist} • {year ? `${ year } •` : ''}
    {#if totalTracks === 1 || totalTracks === 0}
      {totalTracks} Track
    {:else}
      {totalTracks} Tracks
    {/if}
      •
    {totalLength}
  </span>
</div>

<style>
  .album-header {
    display: inline-flex;
    flex-direction: column;
    justify-content: flex-end;
  }

  .album-name {
    font-size: 48px;
    font-weight: 700;
    text-overflow: ellipsis;
    overflow: hidden;
  }

  .album-info {
    /* font-size: 97%; */
    color: var(--color-dark-text-2);
  }
</style>
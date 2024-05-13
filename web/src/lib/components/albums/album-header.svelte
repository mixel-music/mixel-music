<script lang="ts">
  export let album: string;
  export let albumartist: string;
  export let year: number | undefined;
  export let totalTracks: number;
  export let totalLength: number;
</script>

<span class="album-name">
  {album}
</span>

<span class="album-info">
  {albumartist} • {year ? `${ year } •` : ''} {totalTracks} • {totalLength}
</span>

<style>
  .album-name {
    display: inline-block;
    font-size: 52px;
    font-weight: 700;
    text-overflow: ellipsis;
    overflow: hidden;
  }

  .album-info {
    display: inline-block;
    font-size: 95%;
    color: var(--color-dark-text-2);
  }
</style>
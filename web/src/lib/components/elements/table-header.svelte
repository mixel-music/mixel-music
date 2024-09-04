<script lang="ts">
  export let columns: Array<string | number>;

  function getColumnClass(index: number): string {
    if (index === 0) return 'track';
    if (index === 1) return 'title';
    if (index === 2) return 'artist';
    return 'default';
  }
</script>

<div class="header">
  {#each columns as column, index}
    <div class="cell {getColumnClass(index)}">{column}</div>
  {/each}
  <div class="cell tools"> </div>
</div>
  
<style>
  .table {
    display: flex;
    flex-direction: column;
    width: 100%;
  }

  .header, .row {
    display: flex;
    flex-direction: row;
    width: 100%;
  }

  .cell.track {
    flex: 0 0 36px;
    padding: 12px 6px;
  }

  .cell.title {
    flex: 6;
    padding: 12px 6px;
  }

  .cell.artist {
    flex: 3;
    padding: 12px 6px;
  }

  .cell.default {
    flex: 0.5;
    padding: 12px 6px;
  }

  .cell.tools {
    flex: 0 0 64px;
    padding: 12px 6px;
    text-align: center;
  }

  .header {
    font-weight: bold;
    color: var(--color-dark-text-2);
    font-size: 75%;
    text-transform:uppercase;
    letter-spacing: 0.3px;
  }
</style>
<script lang="ts">
  import Icon from "@iconify/svelte";
  export let row: Array<string | number>;

  function getColumnClass(index: number): string {
    if (index === 0) return 'track';
    if (index === 1) return 'title';
    if (index === 2) return 'artist';
    return 'default';
  }
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<!-- svelte-ignore a11y-click-events-have-key-events -->
<div class="row" on:click>
  {#each row as cell, index}
    <div class="cell {getColumnClass(index)}">{cell}</div>
  {/each}
  <div class="cell tools">
    <span class="icon">
      <Icon icon='iconoir:more-horiz' width="21" height="21" />
    </span>
  </div>
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
    display: flex;
    justify-content: flex-end;
  }

  .icon {
    display: flex;
    color: var(--color-dark-text-2);
    align-items: center;
    justify-content: center;
  }
</style>
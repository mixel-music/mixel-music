<script lang="ts">
  export let row: (string | null)[];
  export let columnRatios: number[];
  export let onClick: () => void;
</script>

<div class="table-row" on:click={onClick}>
  {#each row as cell, index}
    <div class="cell" style="flex: {columnRatios[index] || 0.5};">
      {cell}
    </div>
  {/each}
</div>

<style>
  .table-row {
    display: flex;
    flex-direction: row;
    width: 100%;
  }

  .cell {
    padding: 12px 6px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
</style>
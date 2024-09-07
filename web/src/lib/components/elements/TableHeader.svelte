<script lang="ts">
  export let headers: (string | null)[];
  export let columnRatios: number[];
</script>

<div class="table-header">
  {#each headers as header, index}
    {#if header !== null}
      <div class="header-cell" style="flex: {columnRatios[index] || 0.5};">
        {header}
      </div>
    {/if}
  {/each}
</div>

<style>
  .table-header {
    display: flex;
    flex-direction: row;
    width: 100%;
  }

  .header-cell {
    font-weight: bold;
    color: var(--color-dark-text-2);
    font-size: 75%;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    display: inline-flex;
    padding: 12px 6px;
  }
</style>
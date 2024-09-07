<script lang="ts">
  import TableHeader from './TableHeader.svelte';
  import TableBody from './TableBody.svelte';

  export let headers: (string | null)[];
  export let columnRatios: number[];
</script>

<div class="table">
  {#if headers.length}
    <TableHeader {headers} {columnRatios} />
  {/if}
  <TableBody {columnRatios}>
    <slot />
  </TableBody>
</div>

<style>
  .table {
    display: flex;
    flex-direction: column;
    width: 100%;
  }
</style>
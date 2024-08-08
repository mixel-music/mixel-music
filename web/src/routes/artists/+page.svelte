<script lang="ts">
  import type { PageData } from './$types';
  import TableBody from '$lib/components/elements/table-body.svelte';
  import TableCell from '$lib/components/elements/table-data.svelte';
  import TableRow from '$lib/components/elements/table-row.svelte';

  export let data: PageData;
</script>

<svelte:head>
  <title>{ data.title } • mixel-music</title>
</svelte:head>

<TableBody>
  {#each data.list as artist (artist.artisthash)}
    <TableRow>
      <TableCell text={ artist.artist } />
    </TableRow>
  {/each}
</TableBody>
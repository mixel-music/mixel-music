<script lang="ts">
  import type { PageData } from './$types';
  import TableBody from '$lib/components/elements/table-body.svelte';
  import TableCell from '$lib/components/elements/table-item.svelte';
  import CardItemGroup from '$lib/components/elements/card-item-group.svelte';

  export let data: PageData;
</script>

<svelte:head>
  <title>{ data.title } • mixel-music</title>
</svelte:head>

{#if data.list}
  <CardItemGroup title={data.title} />
  <TableBody>
    {#each data.list.list as artist (artist.artisthash)}
        <TableCell text={ artist.artist } />
    {/each}
  </TableBody>
{/if}
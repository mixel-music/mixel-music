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

<!-- {#if data.artistListItem.length > 0}
  <CardItemGroup title={ data.title }>

    {#each data.artistListItem as artist (artist.artisthash)}
      <CardItem>

        <div>
          <ContentHead head={ artist.artist } />
        </div>

      </CardItem>
    {/each}

  </CardItemGroup>
{/if} -->

<div class="artist-content">

  <TableBody>
  
    {#each data.artistListItem as artist (artist.artisthash)}
      <TableRow>
        <TableCell bold text={ artist.artist } />
      </TableRow>
    {/each}
  
  </TableBody>
  
  </div>

<style>
  .artist-content {
    padding-top: var(--app-padding-l);
  }
</style>
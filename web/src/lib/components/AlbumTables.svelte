<script lang="ts">
  import type { AlbumItem } from "$lib/interface";
  import { 
    handleClick,
    getArtistLink,
    convertDateTime
  } from "$lib/tools";
  import Table from "./elements/Table.svelte";
  import TableHead from "./elements/TableHead.svelte";
  import TableHeadItem from "./elements/TableHeadItem.svelte";
  import TableBody from "./elements/TableBody.svelte";
  import TableBodyItem from "./elements/TableBodyItem.svelte";
  import TableMenu from "./elements/TableMenu.svelte";

  export let list: AlbumItem;
</script>

<Table>
  <TableHead>
    <TableHeadItem size='xs'>#</TableHeadItem>
    <TableHeadItem size='xl'>Title</TableHeadItem>
    <TableHeadItem size='m'>Artist</TableHeadItem>
    <TableHeadItem size="s">Time</TableHeadItem>
    <TableHeadItem size="xs"></TableHeadItem>
  </TableHead>

  {#each list.tracks as item}
    <TableBody>
      <TableBodyItem size='xs'>{item.track != 0 ? item.track : '-'}</TableBodyItem>
      <TableBodyItem size='xl'>
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <!-- svelte-ignore a11y-missing-attribute -->
        <a on:click={(event) => handleClick(item, true)} on:keydown>
          {item.title}
        </a>
      </TableBodyItem>

      <TableBodyItem size='m'>
        <a href='{getArtistLink(item.artisthash)}'>
          {item.artist}
        </a>
      </TableBodyItem>

      <TableBodyItem size='s'>{convertDateTime(item.duration)}</TableBodyItem>
      <TableBodyItem size='xs'>
        <TableMenu />
      </TableBodyItem>
    </TableBody>
  {/each}

</Table>
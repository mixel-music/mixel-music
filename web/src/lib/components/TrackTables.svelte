<script lang="ts">
  import type { TrackList } from "$lib/interface";
  import {
    handleClick,
    getAlbumLink,
    getArtistLink,
    convertDateTime,
  } from '$lib/tools';
  import Table from "./elements/Table.svelte";
  import TableHead from "./elements/TableHead.svelte";
  import TableHeadItem from "./elements/TableHeadItem.svelte";
  import TableBody from "./elements/TableBody.svelte";
  import TableBodyItem from "./elements/TableBodyItem.svelte";
  import TableMenu from "./elements/TableMenu.svelte";

  export let list: TrackList[];
</script>

<Table>
  <TableHead>
    <TableHeadItem size='l'>Title</TableHeadItem>
    <TableHeadItem size='m'>Album</TableHeadItem>
    <TableHeadItem size='m'>Artist</TableHeadItem>
    <TableHeadItem size="s">Time</TableHeadItem>
    <TableHeadItem size="xs"></TableHeadItem>
  </TableHead>

  {#each list as item}
    <TableBody>
      <TableBodyItem size='l'>
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <!-- svelte-ignore a11y-missing-attribute -->
        <a on:click={() => handleClick(item)} on:keydown>
          {item.title}
        </a>
      </TableBodyItem>
      <TableBodyItem size="m">
        <a href='{getAlbumLink(item.albumhash)}'>
          {item.album}
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
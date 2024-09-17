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
  import { _ } from 'svelte-i18n'

  export let list: TrackList[];
</script>

<Table>
  <TableHead>
    <TableHeadItem size='l'>{$_('label.title')}</TableHeadItem>
    <TableHeadItem size='m'>{$_('label.album')}</TableHeadItem>
    <TableHeadItem size='m'>{$_('label.artist')}</TableHeadItem>
    <TableHeadItem size="s">{$_('label.time')}</TableHeadItem>
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
        <a href='{getAlbumLink(item.album_id)}'>
          {item.album ? item.album : $_('unknown_album')}
        </a>
      </TableBodyItem>
      <TableBodyItem size='m'>
        <a href='{getArtistLink(item.artist_id)}'>
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
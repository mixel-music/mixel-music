<script lang="ts">
  import type { AlbumItem } from "$lib/interface";
  import { 
    getArtistLink,
    convertDateTime
  } from "$lib/tools";
  import Table from "./elements/Table.svelte";
  import TableHead from "./elements/TableHead.svelte";
  import TableHeadItem from "./elements/TableHeadItem.svelte";
  import TableBody from "./elements/TableBody.svelte";
  import TableBodyItem from "./elements/TableBodyItem.svelte";
  import TableMenu from "./elements/TableMenu.svelte";
  import PlayerService from "$lib/stores/stores";
  import { _ } from 'svelte-i18n'

  export let list: AlbumItem;
</script>

<Table>
  <TableHead>
    <TableHeadItem size='xs'>#</TableHeadItem>
    <TableHeadItem size='xl'>{$_('label.title')}</TableHeadItem>
    <TableHeadItem size='m'>{$_('label.artist')}</TableHeadItem>
    <TableHeadItem size="s">{$_('label.time')}</TableHeadItem>
    <TableHeadItem size="xs"></TableHeadItem>
  </TableHead>

  {#each list.tracks as item}
    <TableBody>
      <TableBodyItem size='xs'>
          <span class="text-sub normal">
            {item.track_number != 0 ? item.track_number : '-'}
          </span>
        </TableBodyItem>
      <TableBodyItem size='xl'>
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        <!-- svelte-ignore a11y-missing-attribute -->
        <a on:click={() =>
          PlayerService.addTrack(
            [{
              album: list.album,
              album_id: list.album_id,
              artist: item.artist,
              artist_id: item.artist_id,
              duration: item.duration,
              title: item.title,
              track_id: item.track_id,
            }]
          , true)
        }
        on:keydown>
          {item.title}
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
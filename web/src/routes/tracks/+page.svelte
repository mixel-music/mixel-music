<script lang="ts">
  import Icon from '@iconify/svelte';
  import type { PageData } from './$types';
  import { getArtwork, getNextPage, getPrevPage, convertDateTime } from '$lib/tools';
  import PlayerService from '$lib/stores/stores';

  import ButtonRound from '$lib/components/elements/ButtonRound.svelte';
  import Table from '$lib/components/elements/Table.svelte';
  import TableItem from '$lib/components/elements/TableItem.svelte';

  export let data: PageData;

  function handleClick(item: any) {
    PlayerService.addTrack({
      hash: item.hash,
      title: item.title,
      album: item.album,
      artist: item.artist,
      albumhash: item.albumhash,
    }, 0);

    PlayerService.setTrack(0);
  }

  let columns = ['#', 'Title', 'Album', 'Artist', 'Time', null];
  let columnsRatios = [0.15, 2, 2, 2, 1, 0.5];
  let rows = data.list.list.map(item => ({
    row: [
      item.title,
      item.album,
      item.artist,
      convertDateTime(item.duration),
    ],
    onClick: () => handleClick(item)
  }));
</script>

<svelte:head>
  <title>{data.title} • mixel-music</title>
</svelte:head>


{#if data.list}
  <div class="album-tracks">
    <Table headers={columns} columnRatios={columnsRatios}>
      {#each rows as { row, onClick }, index}
        <TableItem row={[index + 1, ...row]} columnRatios={columnsRatios} onClick={onClick} />
      {/each}
    </Table>
  </div>

  {#if data.list.total > data.item}
    <div class='bottom-ctl'>
      <ButtonRound href={getPrevPage(data.page, data.item)}>
        <Icon icon='iconoir:nav-arrow-left' />
      </ButtonRound>
      <ButtonRound href={
        getNextPage(
          data.page,
          data.item,
          data.list.total
        )
      }>
        <Icon icon='iconoir:nav-arrow-right' />
      </ButtonRound>
    </div>
  {/if}
{/if}

<style>
  div {
    padding-top: var(--app-padding-s);
  }

  .bottom-ctl {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
  }
</style>
<script lang="ts">
  import Icon from '@iconify/svelte';
  import type { PageData } from './$types';
  import { getArtwork, getNextPage, getPrevPage, convertDateTime } from '$lib/tools';
  import PlayerService from '$lib/stores/stores';

  import ButtonRd from '$lib/components/elements/button-rd.svelte';
  import Table from '$lib/components/elements/table.svelte';
  import TableHeader from '$lib/components/elements/table-header.svelte';
  import TableItem from '$lib/components/elements/table-item.svelte';
  import AlbumHeader from '$lib/components/elements/album-header.svelte';

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

  let columns = ['#', 'Title', 'Albums', 'Artist', 'Time'];
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

<AlbumHeader
album='Tracks'
/>

{#if data.list}
  <div class="album-tracks">
    <Table>
      <TableHeader columns={columns} />

      {#each rows as { row, onClick }, index}
        <TableItem row={[index + 1, ...row]} on:click={onClick} />
      {/each}
    </Table>
  </div>

  {#if data.list.total > data.item}
    <div class='bottom-ctl'>
      <ButtonRd href={getPrevPage(data.page, data.item)}>
        <Icon icon='iconoir:nav-arrow-left' />
      </ButtonRd>
      <ButtonRd href={
        getNextPage(
          data.page,
          data.item,
          data.list.total
        )
      }>
        <Icon icon='iconoir:nav-arrow-right' />
      </ButtonRd>
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
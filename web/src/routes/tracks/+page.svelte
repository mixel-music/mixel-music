<script lang="ts">
  import Icon from '@iconify/svelte';
  import type { PageData } from './$types';
  import { handleClick, getNextPage, getPrevPage, convertDateTime, getArtistLink, getAlbumLink } from '$lib/tools';

  import Table from '$lib/components/elements/Table.svelte';
  import TableHead from '$lib/components/elements/TableHead.svelte';
  import TableHeadItem from '$lib/components/elements/TableHeadItem.svelte';
  import TableBody from '$lib/components/elements/TableBody.svelte';
  import TableBodyItem from '$lib/components/elements/TableBodyItem.svelte';
  import ButtonRound from '$lib/components/elements/ButtonRound.svelte';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';

  export let data: PageData;
</script>

<svelte:head>
  <title>{data.title} • mixel-music</title>
</svelte:head>

{#if data.list}
  <div>
    <PageTitle title=Tracks />
    
    <Table>
      <TableHead>
        <TableHeadItem size='m'>Title</TableHeadItem>
        <TableHeadItem size='m'>Album</TableHeadItem>
        <TableHeadItem size='m'>Artist</TableHeadItem>
        <TableHeadItem size="s">Time</TableHeadItem>
        <TableHeadItem size="xs"></TableHeadItem>
      </TableHead>

      {#each data.list.list as item}
        <TableBody>
          <TableBodyItem size='m'>
            <!-- svelte-ignore a11y-no-static-element-interactions -->
            <!-- svelte-ignore a11y-missing-attribute -->
            <a on:click={handleClick(item)} on:keydown>
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
          <TableBodyItem size='xs'></TableBodyItem>
        </TableBody>
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

</style>
<script lang="ts">
  import type { PageData } from './$types';
  import type { AlbumListResponse } from '$lib/interface';
  import AlbumHeader from '$lib/components/AlbumHeader.svelte';
  import AlbumTable from '$lib/components/AlbumTable.svelte';
  import { _ } from 'svelte-i18n';
  import { getAlbumLink, getArtistLink } from '$lib/tools';

  import GridWrap from '$lib/components/elements/GridWrap.svelte';
  import GridItem from '$lib/components/elements/GridItem.svelte';
  import PageTitle from '$lib/components/elements/PageTitle.svelte';

  export let data: PageData;
  let albumList: AlbumListResponse = data;

  $: emptySlots = albumList?.list.length < 6 ? 6 - albumList.list.length : 0;
</script>

<svelte:head>
  <title>
    {data.item.album
      ? data.item.album : $_('unknown_album')
    } / {data.item.albumartist} • mixel-music
  </title>
</svelte:head>

{#if data.item}
  <AlbumHeader
    album={data.item.album}
    albumId={data.item.album_id}
    albumArtist={data.item.albumartist}
    albumArtistId={data.item.albumartist_id}
    comment={data.item.tracks[0].comment}
    durationTotal={data.item.duration_total}
    fileSizeTotal={data.item.filesize_total}
    trackTotal={data.item.tracks.length}
    year={data.item.year != 0 ? data.item.year : $_('unknown_year')}
    trackItems={data.item.tracks.map(track => ({
      ...track,
      album: data.item.album,
      album_id: data.item.album_id}
    ))}
  />
  
  <AlbumTable list={data.item} />
{/if}

{#if albumList.list}
  {#if albumList.list.length > 1}
    <PageTitle title="More Albums" size="l" />
    <GridWrap>
      {#each albumList.list as album (album.album_id)}
        {#if album.album_id != data.item.album_id}
          <GridItem
            href={getAlbumLink(album.album_id)}
            src={album.album_id}
            alt={album.album ? album.album : $_('unknown_album')}
            lazyload
          >
            <div class="info-card">
              <a href={getAlbumLink(album.album_id)}>
                <span class="text">{album.album ? album.album : $_('unknown_album')}</span>
              </a>
              <a href={getArtistLink(album.albumartist_id)}>
                <span class="text-sub">{data.item.albumartist}</span>
              </a>
            </div>
          </GridItem>
        {/if}
      {/each}

    {#if emptySlots > 0}
      {#each Array(emptySlots) as _}
        <GridItem Empty />
      {/each}
    {/if}
  </GridWrap>
  {/if}
{/if}

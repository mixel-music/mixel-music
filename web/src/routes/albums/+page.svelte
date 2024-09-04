<script lang="ts">
  import Icon from '@iconify/svelte';
  import type { PageData } from './$types';
  import { getNextPage, getPrevPage, getArtwork } from '$lib/tools';

  import CardItemGroup from '$lib/components/elements/card-item-group.svelte';
  import CardItem from '$lib/components/elements/card-item.svelte';
  import ContentHead from '$lib/components/elements/text-title.svelte';
  import ContentBody from '$lib/components/elements/text-sub.svelte';
  import ButtonRd from '$lib/components/elements/button-rd.svelte';

  export let data: PageData;
</script>

<svelte:head>
  <title>{data.title} • mixel-music</title>
</svelte:head>

{#if data.list}
  <CardItemGroup title={data.title}>
    {#each data.list.list as album (album.albumhash)}
      <CardItem
        href='/albums/{ album.albumhash }'
        src={getArtwork(album.albumhash, 300)}
        alt={album.album}
        lazyload
      >
        <div>
          <a href='/albums/{album.albumhash}'>
            <ContentHead head={album.album} />
          </a>
          <a href='/artists'>
            <ContentBody body={album.albumartist} />
          </a>
        </div>
      </CardItem>
    {/each}
  </CardItemGroup>

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
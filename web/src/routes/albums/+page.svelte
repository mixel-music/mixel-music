<script lang="ts">
  import type { PageData } from './$types';
  import { getNextPage, getPrevPage } from '$lib/tools';

  import CardItemGroup from '$lib/components/elements/card-item-group.svelte';
  import CardItem from '$lib/components/elements/card-item.svelte';
  import ContentHead from '$lib/components/elements/text-title.svelte';
  import ContentBody from '$lib/components/elements/text-sub.svelte';
  import NavbarButton from '$lib/components/layouts/navbar/navbar-button.svelte';

  export let data: PageData;

  const ARTWORK_BASE_URL = 'http://localhost:2843/api/artwork';
  const IMAGE_SIZE = 300;
</script>

<svelte:head>
  <title>{data.title} • mixel-music</title>
</svelte:head>

{#if data.list.length > 0}
  <CardItemGroup title={data.title}>
    {#each data.list as album (album.albumhash)}
      <CardItem
        href="/albums/{ album.albumhash }"
        src={`${ARTWORK_BASE_URL}/${album.albumhash}?size=${IMAGE_SIZE}`}
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

  <div class="bottom-ctl">
    <NavbarButton
      icon="iconoir:nav-arrow-left"
      href={getPrevPage(data.page, data.item)}
    />
    <NavbarButton
      icon="iconoir:nav-arrow-right"
      href={
        getNextPage(
          data.page,
          data.item,
          data.total,
        )
      }
    />
  </div>
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
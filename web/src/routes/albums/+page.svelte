<script lang="ts">
  import type { PageData } from './$types';
  import { getNextPageLink, getPrevPageLink } from '$lib/tools';

  import CardItemGroup from '$lib/components/elements/card-item-group.svelte';
  import CardItem from '$lib/components/elements/card-item.svelte';
  import ContentHead from '$lib/components/elements/text-title.svelte';
  import ContentBody from '$lib/components/elements/text-sub.svelte';
  import NavbarButton from '$lib/components/layouts/navbar/navbar-button.svelte';

  export let data: PageData;
</script>

<svelte:head>
  <title>{ data.title } • mixel-music</title>
</svelte:head>

{#if data.albumListItem.length > 0}
  <CardItemGroup title={ data.title }>

    {#each data.albumListItem as album (album.albumhash)}
      <CardItem
        href="/albums/{ album.albumhash }"
        src={`http://localhost:2843/api/artwork/${ album.albumhash }?size=300`}
        alt="{ album.album }"
        lazyload
      >

        <div>
          <a href="/albums/{ album.albumhash }">
            <ContentHead head={ album.album } />
          </a>
          <ContentBody body={ album.albumartist } />
        </div>

      </CardItem>
    {/each}

  </CardItemGroup>

  <div class="bottom-ctl">
    <NavbarButton
      icon="iconoir:nav-arrow-left"
      href='{ getPrevPageLink(data.pageCount, data.itemCount) }'
    />
    <NavbarButton
      icon='iconoir:nav-arrow-right'
      href='{ getNextPageLink(data.pageCount, data.itemCount, data.totalCountItem.count) }'
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
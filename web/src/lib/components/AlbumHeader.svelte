<script lang="ts">
  import ArtworkImage from "./elements/ArtworkImage.svelte";
  import { 
    getArtistLink,
    getArtwork,
    convertDateTime,
    convertFileSize,
  } from "$lib/tools";
  import { _ } from "svelte-i18n";

  export let album: string;
  export let album_id: string;
  export let albumartist: string;
  export let albumartist_id: string;
  export let comment: string = '';
  export let duration_total: number;
  export let filesize_total: number;
  export let track_total: number;
  export let year: number | string;

  $: strLength = convertDateTime(duration_total);
  $: artwork = getArtwork(album_id, 500);
  $: {year != 0 ? $_('info.year',{values:{year:year}})  : $_('unknown_year') };
  $: strSize = convertFileSize(filesize_total);
</script>

<div class="album-header">
  <ArtworkImage
    src={artwork}
    alt={album}
    width={256}
    height={256}
    WrapCover
    FullCover
  />

  <div class="album-details">
    <span class="title">{album ? album : $_('unknown_album')}</span>
    {#if albumartist}
      <a href={getArtistLink(albumartist_id)}>
        <span class="artist">{albumartist}</span>
      </a>
    {/if}

    <div>
      <span class="detail">
        {#if track_total === 1} {$_('info.track',{values:{track_total:track_total}})}
        {:else} {$_('info.tracks',{values:{track_total:track_total}})} {/if}

        ({strLength}) · {year} · {strSize}
      </span>

      <span class="detail">{comment}</span>
    </div>
  </div>
</div>

<style>
  .album-header {
    display: flex;
    width: 100%;
    gap: var(--space-m);
    flex-direction: row;
    margin-top: var(--space-xs);
    margin-bottom: var(--space-l);
  }

  .album-header span {
    width: fit-content;
  }

  .album-details {
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 100%;
  }

  .album-details div {
    margin-top: var(--space-s);
    width: fit-content;
  }

  .title {
    font-size: clamp(1rem, 4vw, 2.5rem);
    font-weight: 700;
    text-overflow: ellipsis;
    overflow: hidden;
  }

  .artist {
    color: var(--dark-text-sub);
    font-size: 110%;
  }

  .detail {
    color: var(--dark-text-sub);
    font-size: 80%;
    line-height: 1rem;
    letter-spacing: 0;
    display: block;
  }
</style>

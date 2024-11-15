<script lang="ts">
  import type { Tracks } from "$lib/interface";
  import ArtworkImage from "./elements/ArtworkImage.svelte";
  import ControlsBar from "./ControlsBar.svelte";
  import { 
    getArtistLink,
    getArtwork,
    convertDateTime,
    convertFileSize,
  } from "$lib/tools";
  import { _ } from "svelte-i18n";
  export let album: string;
  export let albumId: string;
  export let albumArtist: string;
  export let albumArtistId: string;
  export let comment: string = '';
  export let durationTotal: number;
  export let fileSizeTotal: number;
  export let trackTotal: number;
  export let year: number | string;
  export let tracks: Tracks[] | undefined = undefined;

  $: strLength = convertDateTime(durationTotal);
  $: strSize = convertFileSize(fileSizeTotal);
  $: artwork = getArtwork(albumId, 500);
</script>

<div class="album-header">
  <ArtworkImage
    src={artwork}
    alt={album}
    width={256}
    height={256}
    WrapCover
    FullCover
    lazyload={false}
  />

  <div class="album-details">
    <div>
      <span class="title">
        {album ? album : $_('unknown_album')}
      </span>

      {#if albumArtist}
        <a href={getArtistLink(albumArtistId)}>
          <span class="artist">
            {albumArtist}
          </span>
        </a>
      {/if}

      <!-- <div>
        <span class="detail">
          {year != 0 ? $_('info.year',{values: {year: year}}) : $_('unknown_year')}
      </div> -->

    </div>

      {#if tracks}
        <ControlsBar {tracks} />
      {/if}

  </div>
</div>

<style>
  .album-header {
    display: flex;
    width: 100%;
    gap: var(--space-l);
    flex-direction: row;
    margin-bottom: var(--space-l);
  }

  .album-details {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: var(--space-xs);
  }

  .album-details > div {
    display: flex;
    height: 100%;
    flex-direction: column;
    justify-content: flex-end;
  }

  .title {
    font-size: clamp(1rem, 3vw, 2rem);
    font-weight: bold;
    text-overflow: ellipsis;
    overflow: hidden;
  }

  .artist {
    color: var(--dark-text-sub);
    font-size: clamp(1rem, 3vw, 2rem);
  }

  .detail {
    color: var(--dark-text-sub);
    font-size: 85%;
    line-height: 1rem;
    letter-spacing: 0;
    display: block;
  }
</style>

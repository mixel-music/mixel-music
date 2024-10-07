<script lang="ts">
  import type { TrackList } from "$lib/interface";
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
  export let trackItems: TrackList[] | undefined = undefined;

  $: strLength = convertDateTime(durationTotal);
  $: strSize = convertFileSize(fileSizeTotal);
  $: artwork = getArtwork(albumId, 500);
  $: {year != 0 ? $_('info.year',{values: {year: year}})  : $_('unknown_year') };
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
      <span class="title">{album ? album : $_('unknown_album')}</span>
      {#if albumArtist}
        <a href={getArtistLink(albumArtistId)}>
          <span class="artist">{albumArtist}</span>
        </a>
      {/if}

      <div>
        <span class="detail">
          {#if trackTotal === 1} {$_('info.track',{values: {track_total: trackTotal}})}
          {:else} {$_('info.tracks',{values: {track_total: trackTotal}})} {/if}

          ({strLength}) · {year} · {strSize}
        </span>

        <span class="detail">{comment}</span>
      </div>
    </div>

    {#if trackItems}
      <ControlsBar {trackItems} />
    {/if}
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
    width: 100%;
  }

  .album-details > div {
    display: flex;
    height: 100%;
    flex-direction: column;
    justify-content: center;
  }

  .album-details > div > div {
    margin-top: var(--space-s);
  }

  .title {
    font-size: clamp(1rem, 3vw, 2.3rem);
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

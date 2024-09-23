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

<div class="album-wrap" style:background-image="url('{artwork}')" />
<div class="album-header">
  <ArtworkImage
    src={artwork}
    alt={album}
    width={230}
    height={230}
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
  .album-wrap {
    position: fixed;
    width: 100%;
    height: 50%;
    padding: 0;
    z-index: -1;
    margin-left: 100px;
    margin-top: -30px;
    left: 0%;
    filter: blur(12px);
    background-size: cover;
    background-position-y: center;
    border-image: fill 0 linear-gradient(
      to top,
      hsl(0, 0%, 7%) 0%,
      hsla(0, 0%, 7.13%, 0.997) 8.6%,
      hsla(0, 0%, 7.49%, 0.99) 17.5%,
      hsla(0, 0%, 8.02%, 0.979) 26.5%,    
      hsla(0, 0%, 8.65%, 0.965) 35.6%,   
      hsla(0, 0%, 9.33%, 0.948) 44.6%,  
      hsla(0, 0%, 10.04%, 0.93) 53.3%,   
      hsla(0, 0%, 10.73%, 0.91) 61.7%,    
      hsla(0, 0%, 11.39%, 0.89) 69.6%,     
      hsla(0, 0%, 12.01%, 0.87) 76.9%,  
      hsla(0, 0%, 12.57%, 0.852) 83.4%, 
      hsla(0, 0%, 13.05%, 0.835) 89%,   
      hsla(0, 0%, 13.44%, 0.821) 93.6%, 
      hsla(0, 0%, 13.74%, 0.81) 97.1%, 
      hsla(0, 0%, 13.93%, 0.803) 99.2%, 
      hsla(0, 0%, 14%, 0.8) 100%
    );

  }

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
    font-size: clamp(1rem, 2vw, 2.25rem);
    font-weight: 700;
    text-overflow: ellipsis;
    overflow: hidden;
  }

  .artist {
    color: var(--dark-text-sub);
    font-size: 115%;
  }

  .detail {
    color: var(--dark-text-sub);
    font-size: 80%;
    line-height: 1rem;
    letter-spacing: 0;
    display: block;
  }
</style>
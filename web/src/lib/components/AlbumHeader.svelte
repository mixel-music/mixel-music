<script lang="ts">
  import ArtworkImage from "./elements/ArtworkImage.svelte";
  import { 
    getArtistLink,
    getArtwork,
    convertDateTime,
    convertFileSize,
  } from "$lib/tools";

  export let album: string;
  export let albumhash: string;
  export let albumartist: string;
  export let albumartisthash: string;
  export let totalTracks: number;
  export let totalLength: number;
  export let year: string;
  export let size: number;
  export let comment: string = '';

  let strLength = convertDateTime(totalLength);
  let strSize = convertFileSize(size);
  let artwork = getArtwork(albumhash, 500);
</script>

<div class="album-wrap" style="background-image: url({artwork});" />
<div class="album-header">
  <ArtworkImage
    src={artwork}
    alt={album}
    width={230}
    height={230}
    WrapCover
  />

  <div class="album-details">
    <span class="title">{album}</span>
    {#if albumartist}
      <a href={getArtistLink(albumartisthash)}>
        <span class="artist">{albumartist}</span>
      </a>
    {/if}

    <div>
      <span class="detail">
        {#if totalTracks === 1} {totalTracks} Track
        {:else} {totalTracks} Tracks {/if}

        ({strLength}) · {year} · {strSize}
      </span>

      <span class="detail">{comment}</span>
    </div>
  </div>
</div>

<style>
  .album-wrap {
    width: 100%;
    padding: 0;
    height: 55%;
    position: fixed;
    z-indeX: -1;
    background-position-y: center;
    background-size: cover;
    filter: blur(8px);
    border-image: fill 0 linear-gradient(rgb(22 22 22 / 80%), rgb(20 20 20 / 97%), rgb(18 18 18));
    left: 0%;
    margin-left: 210px;
    margin-top: -30px;
  }

  .album-header {
    display: flex;
    width: 100%;
    gap: var(--space-m);
    flex-direction: row;
    margin: var(--space-l) 0;
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
    font-size: clamp(1rem, 2vw, 2rem);
    font-weight: 800;
    text-overflow: ellipsis;
    overflow: hidden;
  }

  .artist {
    color: var(--color-dark-text-2);
    font-size: 110%;
  }

  .detail {
    color: var(--color-dark-text-2);
    font-size: 80%;
    line-height: 1rem;
    display: block;
  }
</style>
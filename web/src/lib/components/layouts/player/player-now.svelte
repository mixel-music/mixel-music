<script lang="ts">
  import ArtworkImage from "$lib/components/elements/ArtworkImage.svelte";
  import { convertDateTime, getAlbumLink, getArtistLink, getArtwork } from "$lib/tools";
  import PlayerService from "$lib/stores/stores";

  $: trk = $PlayerService;
</script>

<div class="player-now">
  {#if trk.hash}
    <ArtworkImage
      src={trk.album === 'Unknown Album'
        ? getArtwork(trk.hash, 128)
        : trk.albumhash && getArtwork(trk.albumhash, 128)
      }
      width=60
      height=60
      alt="Front Cover"
    />

    <div class="track">
      <span class="text">{trk.title}</span>
      <span class="text-sub">
        <a href="{getArtistLink(trk.artisthash)}">
          {trk.artist}
        </a>
        -
        <a href="{getAlbumLink(trk.albumhash)}">
          {trk.album}
        </a>  
      </span>
      <span class="text-sub">
        {convertDateTime(trk.currentTime)} / {convertDateTime(trk.duration)}
      </span>
    </div>
  {/if}
</div>

<style>
  .player-now {
    display: flex;
    align-items: center;
    gap: var(--space-s);
    line-height: 100%
  }

  .track {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    height: 100%;
  }
</style>
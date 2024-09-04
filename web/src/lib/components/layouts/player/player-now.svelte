<script lang="ts">
  import Artwork from "$lib/components/elements/artwork.svelte";
  import { convertDateTime, getArtwork } from "$lib/tools";
  import PlayerService from "$lib/stores/stores";

  $: trk = $PlayerService;
</script>

<div class="player-now">
  {#if trk.hash}
    <Artwork
      src={trk.album === 'Unknown Album'
        ? getArtwork(trk.hash, 128)
        : trk.albumhash && getArtwork(trk.albumhash, 128)
      }
      width=60
      height=60
      alt="Front Cover"
    />

    <div class="track">
      <span class="title">{trk.title}</span>
      <span class="description">{trk.artist} - {trk.album}</span>
      <span class="description">
        {convertDateTime(trk.currentTime)} / {convertDateTime(trk.duration)}
      </span>
    </div>
  {/if}
</div>

<style>
  .player-now {
    display: flex;
    align-items: center;
    gap: var(--app-padding-s);
  }

  .track {
    display: flex;
    flex-direction: column;
    justify-content: space-around;
    height: 100%;
  }
  
  .title {
    display: block;
    font-size: 95%;
    font-weight: 600;
    text-overflow: ellipsis;
    overflow: hidden;
  }

  .description {
    display: block;
    color: var(--color-dark-text-2);
    font-size: 80%;
    text-overflow: ellipsis;
    overflow: hidden;
  }
</style>
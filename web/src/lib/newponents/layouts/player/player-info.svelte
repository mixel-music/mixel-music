<script lang="ts">
  import Artwork from "$lib/newponents/elements/artwork.svelte";
  import { convertDateTime, getArtwork } from "$lib/tools";
  import { trackStore } from "$lib/stores/track-store";
</script>

<div class="player-info">
  {#if $trackStore.hash}
    <Artwork
      src={$trackStore.album === 'Unknown Album'
        ? getArtwork($trackStore.hash, 128)
        : $trackStore.albumhash && getArtwork($trackStore.albumhash, 128)
      }
      width=60
      height=60
      alt="Front Cover"
    />

    <div class="track">
      <span class="title">{$trackStore.title}</span>
      <span class="description">{$trackStore.artist} - {$trackStore.album}</span>
      <span class="description">
        {convertDateTime($stateStore.currentTime)} / {convertDateTime($stateStore.duration)}
      </span>
    </div>
  {/if}
</div>

<style>
  .player-info {
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
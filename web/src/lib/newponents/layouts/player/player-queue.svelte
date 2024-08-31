<script lang="ts">
  import Artwork from "$lib/newponents/elements/artwork.svelte";
  import { isQueueOpen } from "$lib/stores/layout";
  import PlayerService from "$lib/stores/stores";
  import { getArtwork } from "$lib/tools";

  import { fly } from "svelte/transition";
  import { circOut } from "svelte/easing";

  $: lists = $PlayerService;
</script>

{#if $isQueueOpen}
  <div class="player-queue" transition:fly={
    {
      delay: 10,
      duration: 400,
      y: document.querySelector('.player-queue').clientHeight,
      opacity: 1,
      easing: circOut,
    }
  }>
    Play Queue
    
    {#each lists.lists as trk}
      <div class="track">
        <Artwork
          src={trk.album === 'Unknown Album'
            ? getArtwork(trk.hash, 128)
            : trk.albumhash && getArtwork(trk.albumhash, 128)
          }
          width=45
          height=45
          alt="Front Cover"
          FullCover
        />

        <div class="texts">
          <span class="title">{trk.title}</span>
          <span class="description">{trk.artist}</span>
        </div>
      </div>
    {/each}
  </div>
{/if}

<style>
  .player-queue {
    position: fixed;
    right: 64px;
    bottom: 96px;

    z-index: 0;
    flex-shrink: 0;
    padding: 24px 21px;
    background-color: var(--color-dark-bg-2);
    border: 1px solid var(--color-dark-border);
    border-radius: var(--app-radius) var(--app-radius) 0 0;

    width: 25%;
    height: 50%;
    display: flex;
    gap: var(--app-padding-l);
    flex-direction: column;
    overflow-y: scroll;

    padding-top: 24px;
  }

  .track {
    display: flex;
    flex-direction: row;
    gap: var(--app-padding-s);
  }

  .texts {
    display: inline-flex;
    flex-direction: column;
    justify-content: space-around;
    white-space: nowrap;
    overflow: hidden;
  }
  
  .title {
    display: block;
    font-size: 100%;
    font-weight: 600;
    text-overflow: ellipsis;
    overflow: hidden;
  }

  .description {
    display: block;
    color: var(--color-dark-text-2);
    text-overflow: ellipsis;
    overflow: hidden;
    font-size: 90%;
  }
</style>
<script lang="ts">
  import Artwork from "$lib/components/elements/ArtworkImage.svelte";
  import { isQueueOpen } from "$lib/stores/layout";
  import PlayerService from "$lib/stores/stores";
  import { getArtistLink, getArtwork } from "$lib/tools";

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
    
    {#each lists.lists as trk, index}
      <div class="track">
        <Artwork
          src={trk.album === ''
            ? getArtwork(trk.track_id, 128)
            : trk.album_id && getArtwork(trk.album_id, 128)
          }
          width=45
          height=45
          alt="Front Cover"
          FullCover
        />

        <div class="texts">
          <!-- svelte-ignore a11y-missing-attribute -->
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <!-- svelte-ignore a11y-click-events-have-key-events -->
            <span class="title">
                {trk.title}
            </span>
            <span class="description">
              <a href="{getArtistLink(trk.artist_id)}">
                {trk.artist}
              </a>
            </span>
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
    background-color: var(--black-2);
    border: 1px solid var(--black-4);
    border-radius: var(--app-radius) var(--app-radius) 0 0;

    width: 25%;
    height: 50%;
    display: flex;
    gap: var(--space-s);
    flex-direction: column;
    overflow-y: scroll;

    padding-top: 24px;
  }

  .track {
    display: flex;
    flex-direction: row;
    gap: var(--space-s);
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
    color: var(--dark-text-sub);
    text-overflow: ellipsis;
    overflow: hidden;
    font-size: 90%;
  }
</style>
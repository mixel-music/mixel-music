<script lang="ts">
  import Artwork from "$lib/components/elements/ArtworkImage.svelte";
  import PlayerService from "$lib/stores/stores";
  import { getArtistLink, getArtwork } from "$lib/tools";
  import { isQueueOpen } from "$lib/stores/layout";
  import { cubicOut } from "svelte/easing";
  import { fly } from "svelte/transition";
  import { _ } from "svelte-i18n";

  $: lists = $PlayerService;
</script>

{#if $isQueueOpen}
  <div class="player-queue"
  transition:fly={
    { 
      delay: 10,
      duration: 600,
      x: document.querySelector('.player-queue').clientWidth + 30,
      opacity: 1,
      easing: cubicOut
    }
  }>
    <span class="title">{$_('player.queue')}</span>
    {#each lists.lists as trk, index}
      <div class="track">
        <Artwork
          src={trk.album === ''
            ? getArtwork(trk.track_id, 128)
            : trk.album_id && getArtwork(trk.album_id, 128)
          }
          width=45
          height=45
          alt={$_('player.front_cover')}
          FullCover
        />

        <div class="texts">
          <!-- svelte-ignore a11y-missing-attribute -->
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <!-- svelte-ignore a11y-click-events-have-key-events -->
            <span class="text normal">
                {trk.title}
            </span>
            <span class="text-sub normal small">
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
    right: 32px;
    bottom: 126px;

    z-index: 0;
    flex-shrink: 0;
    padding: var(--space-m);
    background-color: var(--dark-queue);
    border: 1px solid var(--dark-border);
    border-radius: var(--radius-m);

    width: 500px;
    height: 60%;
    display: flex;
    gap: var(--space-m);
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
    font-weight: 500;
    font-size: 120%;
  }
</style>
<script lang="ts">
  import ArtworkImage from "$lib/components/elements/ArtworkImage.svelte";
  import PlayerService from "$lib/stores/stores";
  import { convertDateTime, getArtistLink, getArtwork } from "$lib/tools";
  import { isQueueOpen } from "$lib/stores/layout";
  import { cubicOut } from "svelte/easing";
  import { fly, fade } from "svelte/transition";
  import { _ } from "svelte-i18n";
  import JustButton from "$lib/components/elements/JustButton.svelte";
  import Icon from "@iconify/svelte";

  $: lists = $PlayerService;
</script>

{#if $isQueueOpen}
  <div class="player-queue"
  transition:fly={
    { 
      delay: 10,
      duration: 600,
      x: document.querySelector('.player-queue').clientWidth + 20,
      opacity: 1,
      easing: cubicOut
    }
  }>
    <!-- <span class="title">{$_('player.queue')}</span> -->
    {#each lists.lists as trk, index}
      <div transition:fade={{ delay: 10, duration: 70 }} class="track">
        <ArtworkImage
          src={trk.album === ''
            ? getArtwork(trk.track_id, 128)
            : trk.album_id && getArtwork(trk.album_id, 128)
          }
          width=45
          height=45
          alt={$_('player.front_cover')}
          FullCover
        />

        <div class="left">
          <!-- svelte-ignore a11y-missing-attribute -->
          <!-- svelte-ignore a11y-no-static-element-interactions -->
          <!-- svelte-ignore a11y-click-events-have-key-events -->
            <a class="text normal" on:click={() =>
              PlayerService.setTrack(index)
            }>
                {trk.title}
            </a>
            <span class="text-sub normal small">
              <a href="{getArtistLink(trk.artist_id)}">
                {trk.artist}
              </a>
            </span>
        </div>

        <div class="right">
          <span class="text-sub small">
            {convertDateTime(trk.duration)}
          </span>

          <JustButton
            width="21px"
            height="32px"
            on:click={(event) => PlayerService.delTrack(index)}
            title
          >
            <Icon icon="iconoir:xmark" width="21" height="21" />
          </JustButton>
        </div>
      </div>
    {/each}
  </div>
{/if}

<style>
  .player-queue {
    z-index: 0;
    display: flex;
    position: fixed;
    top: var(--space-m);
    right: var(--space-m);
    flex-direction: column;
    flex-shrink: 0;
    width: 410px;
    height: calc(100% - 96px - calc(var(--space-m)* 2));
    box-shadow: 0 0 0 1px var(--dark-border) inset;
    background-color: var(--dark-queue);
    border-radius: var(--radius-m);
    gap: var(--space-m);
    overflow-y: scroll;
    padding: var(--space-s);
    padding-top: var(--space-m);
    backdrop-filter: blur(64px);
  }

  .track {
    display: flex;
    flex-direction: row;
    gap: var(--space-s);
  }

  .left {
    display: inline-flex;
    flex-direction: column;
    justify-content: space-around;
    white-space: nowrap;
    overflow: hidden;
  }

  .normal {
    display: block;
    font-size: 100%;
    line-height: normal;
    text-overflow: ellipsis;
    overflow: hidden;
  }

  .small {
    font-size: 90%;
  }

  .right {
    display: inline-flex;
    margin-left: auto;
    align-items: center;
    gap: var(--space-xs);
  }

  a {
    width: auto;
  }

  /* .title {
    font-weight: 500;
    font-size: 130%;
    padding: var(--space-xs) 0;
  } */
</style>
<script lang="ts">
  import PlayerService from "$lib/stores/stores";
  import PlayerButton from '$lib/newponents/layouts/player/player-button.svelte'
  import PlayerNow from '$lib/newponents/layouts/player/player-now.svelte';
  import { updated } from "$app/stores";
  import { isQueueOpen } from "$lib/stores/layout";

  $: trk = $PlayerService;
</script>

<div class="player">
  <div class="player-center">
    <div class="player-controls">
      <PlayerButton
        on:click={PlayerService.goPrev}
        icon="iconoir:skip-prev-solid"
        ControlButton
        alt="Previous"
      />

      {#if trk.isPlaying}
        <PlayerButton
          on:click={PlayerService.toggle}
          icon="iconoir:pause-solid"
          disabled={!trk.isLoaded}
          ControlButton
          PrimaryButton
          alt="Pause"
        />
      {:else}
        <PlayerButton
          on:click={PlayerService.toggle}
          icon="iconoir:play-solid"
          disabled={!trk.isLoaded}
          ControlButton
          PrimaryButton
          alt="Play"
        />
      {/if}

      <PlayerButton
        on:click={PlayerService.goNext}
        icon="iconoir:skip-next-solid"
        ControlButton
        alt="Next"
      />
    </div>

    <input
      on:input={(event) =>
        PlayerService.seek(parseFloat(event.target.value))
      }
      type="range"
      min="0"
      max={trk.duration}
      value={trk.currentTime}
      disabled={!trk.isLoaded}
    />
  </div>

  <div class="player-contents">
    <PlayerNow />
    
    <div class="player-settings">
      <div class="player-volume">
        <input
          on:input={(event) => {
            PlayerService.volume(parseFloat(event.target.value))
          }}
          type="range"
          min="0"
          max="100"
          value={trk.mute ? 0 : trk.volumeRange}
          style="width: 95px; margin: 0 8px;"
        />

        <PlayerButton
          on:click={PlayerService.mute}
          alt="Volume"
          icon={trk.volume === 0 || trk.mute
            ? "iconoir:sound-off" : trk.volumeRange < 50
            ? "iconoir:sound-low" : "iconoir:sound-high"
          }
          off={trk.volume === 0 || trk.mute}
        />
      </div>
    
      <PlayerButton
        on:click={PlayerService.loop}
        alt={trk.loop === 2 ? "Repeat one" : "Repeat"}
        icon={trk.loop === 1
          ? "iconoir:repeat" : trk.loop === 2
          ? "iconoir:repeat-once" : "iconoir:repeat"
        }
        off={!trk.loop}
      />
    
      <PlayerButton
        on:click={() => {
          $isQueueOpen = !$isQueueOpen
        }}
        alt="Playlist"
        icon="iconoir:playlist"
      />

      <PlayerButton
        icon="iconoir:nav-arrow-up"
      />
    </div>
  </div>
</div>

<style>
  .player {
    display: flex;
    align-items: center;
    justify-content: space-between;
    position: fixed;
    bottom: 0;
    z-index: 2;
    width: 100%;
    height: 96px;
    background-color: var(--color-dark-bg-trk);
    box-shadow: 0 0 0 1px var(--color-dark-border) inset;
    backdrop-filter: blur(64px);
  }

  .player-center {
    position: fixed;
    left: 50%;
    transform: translate(-50%, 0);
  }

  .player-controls {
    display: flex;
    justify-content: center;
    margin-left: 2px;
    gap: 24px;
  }

  .player-contents {
    width: 100%;
    display: flex;
    padding: 0 21px;
    justify-content: space-between;
  }

  .player-settings {
    display: flex;
    align-items: center;
  }

  .player-volume {
    display: flex;
    align-items: center;
    gap: 4px;
  }

  .player-volume input {
    opacity: 0;
  }
  
  .player-volume:hover input {
    opacity: 1;
    transition: all 0.2s ease;
  }
</style>
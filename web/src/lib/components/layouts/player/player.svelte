<script lang="ts">
  import PlayerService from "$lib/stores/stores";
  import { isQueueOpen } from "$lib/stores/layout";
  import PlayerButton from '$lib/components/layouts/player/PlayerButton.svelte'
  import PlayerInfo from '$lib/components/layouts/player/PlayerInfo.svelte';
  import { _ } from 'svelte-i18n'

  $: trk = $PlayerService;
</script>

<div class="player">
  <div class="player-center">
    <div class="player-controls">
      <PlayerButton
        on:click={PlayerService.goPrev}
        icon="iconoir:skip-prev-solid"
        ControlButton
        alt={$_('player.previous')}
      />

      {#if trk.isPlaying}
        <PlayerButton
          on:click={PlayerService.toggle}
          icon="iconoir:pause-solid"
          disabled={!trk.isLoaded}
          ControlButton
          PrimaryButton
          alt={$_('player.pause')}
        />
      {:else}
        <PlayerButton
          on:click={PlayerService.toggle}
          icon="iconoir:play-solid"
          disabled={!trk.isLoaded}
          ControlButton
          PrimaryButton
          alt={$_('player.play')}
        />
      {/if}

      <PlayerButton
        on:click={PlayerService.goNext}
        icon="iconoir:skip-next-solid"
        ControlButton
        alt={$_('player.next')}
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
    <PlayerInfo />
    
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
          alt={$_('player.volume')}
          icon={trk.volume === 0 || trk.mute
            ? "iconoir:sound-off" : trk.volumeRange < 50
            ? "iconoir:sound-low" : "iconoir:sound-high"
          }
          off={trk.volume === 0 || trk.mute}
        />
      </div>
    
      <PlayerButton
        on:click={PlayerService.loop}
        alt={
          trk.loop === 2 ? $_('player.repeat_one') :
          trk.loop === 1 ? $_('player.repeat_all') : $_('player.repeat')
        }
        icon={trk.loop === 1
          ? "iconoir:repeat" : trk.loop === 2
          ? "iconoir:repeat-once" : "iconoir:repeat"
        }
        off={!trk.loop}
      />

      <!-- <PlayerButton
        icon="iconoir:closed-captions-tag"
        off
      /> -->
    
      <PlayerButton
        on:click={() => {
          $isQueueOpen = !$isQueueOpen
        }}
        alt={$_('player.queue')}
        icon="iconoir:playlist"
        off={!$isQueueOpen}
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
    background-color: var(--dark-player);
    box-shadow: 0 0 0 1px var(--dark-border) inset;
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
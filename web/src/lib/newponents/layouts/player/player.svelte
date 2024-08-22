<script lang="ts">
  import { stateStore } from '$lib/stores/state-store';
  import { playTrack, prevTrack, nextTrack, seekTrack } from './controls';

  import PlayerButton from './player-button.svelte';
  import PlayerRange from './player-range.svelte';
  import PlayerInfo from './player-info.svelte';
  import PlayerMenu from './player-menu.svelte';
  import Handler from './handler.svelte';

  let value: number;

  $: {
    if (!$stateStore.isSeeking) {
      value = $stateStore.currentTime;
    }
  }
</script>

<Handler />

<div class="player">
  <div class="player-center">
    <div class="player-button">
      <PlayerButton
        alt='Previous'
        on:click={prevTrack}
        icon='iconoir:skip-prev-solid'
        ControlButton
      />

      <PlayerButton
        on:click={playTrack}
        alt={$stateStore.isPlaying ? 'Pause' : 'Play'}
        icon={$stateStore.isPlaying ?
          'iconoir:pause-solid' : 'iconoir:play-solid'
        }
        ControlButton
        PrimaryButton
      />

      <PlayerButton
        alt='Next'
        on:click={nextTrack}
        icon='iconoir:skip-next-solid'
        ControlButton
      />
    </div>

    <PlayerRange
      bind:value={value}
      name='length'
      width='550px'
      max={$stateStore.duration}
    />
  </div>

  <div class="player-area">
    <PlayerInfo />
    <PlayerMenu />
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

  .player-area {
    width: 100%;
    display: flex;
    padding: 0 21px;
    justify-content: space-between;
  }

  .player-center {
    position: fixed;
    left: 50%;
    transform: translate(-50%, 0);
  }

  .player-button {
    display: flex;
    justify-content: center;
    padding: 0 6px;
    padding-top: 3px;
    padding-bottom: 2px;
    gap: 24px;
  }
</style>
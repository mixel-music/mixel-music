<script lang="ts">
  import PlayerButton from "./player-button.svelte";
  import PlayerRange from "./player-range.svelte";
  import { stateStore } from '$lib/stores/state-store';

  import { muteTrack } from "./controls";
</script>

<div class="player-menu">
  <div class="player-volume">
    <!-- <PlayerRange
      name='volume'
      width='110px'
      on:click:bind:seekVolume
      on:mousedown={(event) => console.debug("test")}
    /> -->

    <PlayerButton
      on:click={muteTrack}
      alt="Volume"
      icon={$stateStore.volume === 0 || $stateStore.mute
        ? 'iconoir:sound-off' : $stateStore.volume * 100 < 50
        ? 'iconoir:sound-low' : 'iconoir:sound-high'
      }
      off={$stateStore.volume === 0 || $stateStore.mute}
    />
  </div>

  <PlayerButton
    on:click
    alt={$stateStore.loop === 2 ? 'Repeat one' : 'Repeat'}
    icon={$stateStore.loop === 1
      ? 'iconoir:repeat' : $stateStore.loop === 2
      ? 'iconoir:repeat-once' : 'iconoir:repeat'
    }
    off={!$stateStore.loop}
  />

  <PlayerButton
    alt='Shuffle'
    icon='iconoir:shuffle'
    off
  />

  <PlayerButton
    alt='Playlist'
    icon='iconoir:playlist'
  />
</div>

<style>
  .player-menu {
    display: flex;
    align-items: center;
  }

  .player-volume {
    display: flex;
    align-items: center;
    gap: 4px;
  }
</style>
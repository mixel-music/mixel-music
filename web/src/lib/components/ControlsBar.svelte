<script lang="ts">
  import Icon from "@iconify/svelte";
  import SquareButton from "./elements/SquareButton.svelte";
  import { _ } from 'svelte-i18n'
  import RoundButton from "./elements/RoundButton.svelte";
  import type { TrackList } from "$lib/interface";
  import PlayerService from "$lib/stores/stores";

  export let tracks: TrackList[];
</script>

<div class="controls-bar">
  <div>
    <SquareButton
      width='150px'
      height='50px'
      title={$_('controls.play')}
      on:click={() =>
        PlayerService.addTrack(
          tracks.map(track => ({
            album: track.album,
            album_id: track.album_id,
            artist: track.artist,
            artist_id: track.artist_id,
            duration: track.duration,
            title: track.title,
            track_id: track.track_id,
          }))
        , true)
      }
    >
      <Icon icon="iconoir:play-solid" />
      {$_('controls.play')}
    </SquareButton>

    <SquareButton
      width='150px'
      height='50px'
      title={$_('controls.shuffle')}
    >
    <Icon icon="iconoir:shuffle" />
      {$_('controls.shuffle')}
    </SquareButton>
  </div>
  <div>
    <RoundButton
      width="50px"
      height="50px"
      title={$_('controls.favorite')}
    >
      <Icon icon="iconoir:heart" width="21" height="21" />
    </RoundButton>
    
    <SquareButton
      width='150px'
      height='50px'
      title={$_('controls.album_info')}
    >
    <Icon icon="iconoir:info-circle-solid" />
      {$_('controls.album_info')}
    </SquareButton>

    <!-- <SquareButton
      href='.'
      width='140px'
      height='50px'
      title={$_('controls.download')}
    >
    <Icon icon="iconoir:download" />
      {$_('controls.download')}
    </SquareButton> -->
  </div>
</div>

<style>
  .controls-bar {
    display: flex;
    margin-bottom: var(--space-l);
    justify-content: space-between;
  }

  .controls-bar > div {
    display: flex;
    gap: var(--space-s);
  }
</style>
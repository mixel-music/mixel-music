<script lang="ts">
  import type { TrackList } from "$lib/interface";
  import PlayerService from "$lib/stores/stores";
  import Button from "./elements/Button.svelte";
  import { _ } from 'svelte-i18n'

  export let tracks: TrackList[];
</script>

<div class="controls-bar">
  <div>
    <Button
      button='square'
      width='150px'
      height='50px'
      title={$_('controls.play')}
      iconName='iconoir:play-solid'
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
      {$_('controls.play')}
    </Button>

    <Button
      button='square'
      width='150px'
      height='50px'
      title={$_('controls.shuffle')}
      iconName='iconoir:shuffle'
    >
      {$_('controls.shuffle')}
    </Button>
  </div>
  <div>
    <Button
      button='round'
      width="50px"
      title={$_('controls.favorite')}
      iconName='iconoir:heart'
      iconSize='21'
    />
    
    <Button
      button='square'
      width='150px'
      height='50px'
      title={$_('controls.album_info')}
      iconName='iconoir:info-circle-solid'
    >
      {$_('controls.album_info')}
    </Button>
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
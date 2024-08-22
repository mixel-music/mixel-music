<script lang="ts">
  import { onDestroy } from 'svelte';
  import { trackStore } from '$lib/stores/track-store';
  import { stateStore } from '$lib/stores/state-store';
  import { playTrack, prevTrack, nextTrack } from './controls';
  import { getArtwork } from '$lib/tools';

  let trackElement: HTMLAudioElement = new Audio();

  $: $trackStore.hash, streamTrack();

  $: if (trackElement) {
    $stateStore.isPlaying = !trackElement.paused;

    if ($stateStore.mute == false && trackElement.muted) {
      trackElement.muted = false;
    }
    else if ($stateStore.mute == true && !trackElement.muted) {
      trackElement.muted = true;
    }

    if ($stateStore.isPlaying == true && trackElement.paused) {
      trackElement.play();
    }
    else if ($stateStore.isPlaying == false && !trackElement.paused) {
      trackElement.pause();
    }
  }

  function streamTrack(): void {
    if ($trackStore.hash) {
      trackElement.src = `http://localhost:2843/api/stream/${$trackStore.hash}`;
      trackStore.update(track => ({
        ...track,
        artwork: getArtwork($trackStore.hash, 128),
      }))

      trackElement.addEventListener('loadedmetadata', handleMetadataLoaded);
      trackElement.addEventListener('timeupdate', handleTimeUpdate);
    }
  }

  function handleMetadataLoaded() {
    stateStore.update(state => ({
      ...state,
      duration: trackElement.duration,
      isPlaying: true,
    }));

    trackElement.play();
    setTrackInfo();
  }

  function handleTimeUpdate() {
    if (!$stateStore.isUpdated) {
      stateStore.update(state => ({
        ...state,
        currentTime: trackElement.currentTime,
      }));
    }
    else {
      trackElement.currentTime = $stateStore.currentTime;

      stateStore.update(state => ({
        ...state,
        isUpdated: false,
      }));
    }

    if (trackElement.currentTime >= trackElement.duration) {
      trackElement.pause();

      stateStore.update(state => ({
        ...state,
        isPlaying: false,
      }));
    }
  }

  function setTrackInfo(): void {
    if ('mediaSession' in navigator) {
      navigator.mediaSession.metadata = new MediaMetadata({
        title: $trackStore.title,
        album: $trackStore.album,
        artist: $trackStore.artist,
        artwork: [{src: $trackStore.artwork}],
      });

      navigator.mediaSession.setActionHandler('play', playTrack);
      navigator.mediaSession.setActionHandler('pause', playTrack);
      navigator.mediaSession.setActionHandler('seekbackward', () => { trackElement.currentTime -= 10; });
      navigator.mediaSession.setActionHandler('seekforward', () => { trackElement.currentTime += 10; });
      navigator.mediaSession.setActionHandler('previoustrack', prevTrack);
      navigator.mediaSession.setActionHandler('nexttrack', nextTrack);
    }
  }

  onDestroy(() => {
    trackElement.removeEventListener("loadedmetadata", handleMetadataLoaded);
    trackElement.removeEventListener("timeupdate", handleTimeUpdate);

    if (trackElement) {
      trackElement.src = '';
    }
  });
</script>
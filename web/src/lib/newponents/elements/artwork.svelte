<script lang="ts">
  export let alt: string | undefined = undefined;
  export let src: string | undefined = undefined;
  export let width: string | number | undefined = undefined;
  export let height: string | number | undefined = undefined;

  let displayArtwork = true;

  function loadFailed() {
    displayArtwork = false;
  }
</script>

<div style='height: {height}px;'>
  {#if displayArtwork}
    <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
    <img
      {src}
      {alt}
      {width}
      {height}
      on:click
      on:keydown
      on:mousedown
      on:mouseleave
      on:error={loadFailed}
    />
  {/if}
</div>

<style>
  div {
    aspect-ratio: 1/1;
    display: inline-flex;
    background-color: var(--color-dark-bg-2);
    box-shadow: 0 0 0 1px var(--color-dark-border) inset;
    border-radius: calc(var(--app-radius) / 2);
  }

  img {
    object-fit: scale-down;
    aspect-ratio: 1/1;
    border-radius: calc(var(--app-radius) / 2);
  }
</style>
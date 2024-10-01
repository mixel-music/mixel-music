<script lang="ts">
  export let alt: string | undefined = undefined;
  export let src: string | undefined = undefined;
  export let width: string | number | undefined = undefined;
  export let height: string | number | undefined = undefined;
  export let FullCover: boolean = false;
  export let WrapCover: boolean = false;
  
  $: showArtwork = true;
</script>

<div class:wrap={WrapCover} style="height: {height}px;">
  {#if showArtwork}
    <!-- svelte-ignore a11y-no-noninteractive-element-interactions -->
    <img
      loading="lazy"
      {src}
      {alt}
      {width}
      {height}
      on:click
      on:keydown
      on:mousedown
      on:mouseleave
      on:error={() => showArtwork = !showArtwork}
      class:full={FullCover}
    />
  {/if}
</div>

<style>
  div {
    aspect-ratio: 1/1;
    display: inline-flex;
    background-color: var(--dark-element);
    box-shadow: 0 0 0 1px var(--dark-border) inset;
    border-radius: var(--radius-s);
  }

  img {
    aspect-ratio: 1/1;
    border-radius: var(--radius-s);
    object-fit: scale-down;
  }

  .full {
    object-fit: cover;
  }

  .wrap {
    box-shadow: 0 0 0 1px #ffffff0c inset;
    background-color: #1818184f;
  }
</style>

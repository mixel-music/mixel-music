<script lang="ts">
  export let alt: string | undefined = undefined;
  export let src: string | undefined = undefined;
  export let width: string | number | undefined = undefined;
  export let height: string | number | undefined = undefined;
  export let FullCover: boolean = false;
  export let WrapCover: boolean = false;
  let isDisplay = true;

  function loadFailed() {
    isDisplay = false;
  }
</script>

<div class:wrap-cover={WrapCover} style="height: {height}px;">
  {#if isDisplay}
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
      class:full-cover={FullCover}
      loading="lazy"
    />
  {/if}
</div>

<style>
  div {
    aspect-ratio: 1/1;
    display: inline-flex;
    background-color: var(--color-dark-bg-2);
    box-shadow: 0 0 0 1px var(--color-dark-border) inset;
    border-radius: var(--radius-s);
  }

  img {
    aspect-ratio: 1/1;
    border-radius: var(--radius-s);
    object-fit: scale-down;
  }

  .full-cover {
    object-fit: cover;
  }

  .wrap-cover {
    box-shadow: 0 0 0 1px #ffffff0c inset;
    background-color: #1818184f;
  }
</style>
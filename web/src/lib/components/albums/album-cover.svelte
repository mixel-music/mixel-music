<script lang="ts">
  export let alt: string | undefined = undefined;
  export let src: string | undefined = undefined;
  export let width: string | number | undefined = undefined;
  export let height: string | number | undefined = undefined;
</script>

<div>
  <img
    {src}
    {alt}
    {width}
    {height}
    on:click
    on:mousedown
    on:mouseleave
  />
</div>

<style>
  div {
    width: fit-content;
    display: inline-flex;
    background-color: var(--color-dark-bg-2);
    box-shadow: 0 0 0 1px var(--color-dark-border) inset;
    border-radius: var(--app-radius);
    aspect-ratio: 1/1;
  }

  img {
    width: 100%;
    display: block;
    object-fit: scale-down;
    aspect-ratio: 1/1;
    border-radius: var(--app-radius);
  }
</style>
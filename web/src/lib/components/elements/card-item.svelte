<script lang="ts">
  export let lazy: boolean = false;
  export let link: string | undefined = undefined;
  export let alt: string | undefined = undefined;
  export let src: string | undefined = undefined;
</script>

<div>
  {#if src}
    <a href={link} on:click>
      <img
        loading={lazy ? 'lazy' : null}
        {src} {alt}
      >
    </a>
    <slot />

  {:else}
    <a href={link} on:click>
      
    </a>
    <slot />

  {/if}
</div>

<style>
  div {
    white-space: nowrap;
    margin-bottom: 16px;
  }

  a {
    width: auto;
    display: flex;
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
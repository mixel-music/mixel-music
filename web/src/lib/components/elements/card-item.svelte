<script lang="ts">
  export let lazyload: boolean = false;
  export let href: string | undefined = undefined;
  export let alt: string | undefined = undefined;
  export let src: string | undefined = undefined;
</script>

<div class="card-item">
  {#if src}
    <div class="card-body">
      <a {href} on:click>
        <img
          loading={lazyload ? 'lazy' : null}
          {src} {alt}
        >
      </a>
    </div>
    <slot />

  {:else}
    <div class="card-body">

    </div>
    <slot />

  {/if}
</div>

<style>
  .card-item {
    white-space: nowrap;
    margin-bottom: 16px;
  }

  .card-body {
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
    object-fit: cover;
    aspect-ratio: 1/1;
    border-radius: var(--app-radius);
  }
</style>
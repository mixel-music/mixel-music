<script lang="ts">
  export let lazyload: boolean = false;
  export let href: string | undefined = undefined;
  export let alt: string | undefined = undefined;
  export let src: string | undefined = undefined;
  export let round: boolean = false;

  let showArtwork = true;

  function loadFailed() {
    showArtwork = false;
  }
</script>

<div class="card-item">
  {#if src}
    <div class="card-body {round ? 'round' : ''}">
        <a tabindex="-1" {href} on:click>
        {#if showArtwork}
          <img
            loading={lazyload ? 'lazy' : null}
            {src} {alt} on:error={loadFailed}
          >
        {/if}
      </a>
    </div>
    <slot />

  {:else}
    <div class="card-body {round ? 'round' : ''}">
      <a tabindex="-1" {href} on:click />
    </div>
    <slot />

  {/if}
</div>

<style>
  .card-item {
    white-space: nowrap;
    margin-bottom: var(--space-s);
  }

  .card-body {
    width: auto;
    display: flex;
    background-color: var(--color-dark-bg-2);
    box-shadow: 0 0 0 1px var(--color-dark-border) inset;
    aspect-ratio: 1/1;
    border-radius: var(--radius-s);
  }

  .round {
    border-radius: 50%;
  }

  a {
    display: block;
    width: 100%;
    height: 100%;
  }

  img {
    width: 100%;
    height: 100%;
    display: block;
    object-fit: scale-down;
    aspect-ratio: 1/1;
    border-radius: var(--radius-s);
  }
</style>
<script lang="ts">
  import { getArtwork } from "$lib/tools";

  export let lazyload: boolean = false;
  export let href: string | undefined = undefined;
  export let alt: string | undefined = undefined;
  export let src: string | undefined = undefined;
  export let round: boolean = false;
  export let Empty: boolean = false;

  let showArtwork = true;

  function loadFailed() {
    showArtwork = false;
  }
</script>

{#if !Empty}
  <div class="card-item">
    {#if src}
      <div class="card-body {round ? 'round' : ''}">
        <a tabindex="-1" {href} on:click>
          {#if showArtwork}
            <img
              loading={lazyload ? 'lazy' : null}
              src={getArtwork(src, 300)} {alt} on:error={loadFailed}
            >
          {/if}
        </a>
      </div>

      <slot />
    {:else}
      <div class="card-body {round ? 'round' : ''}">
        <a tabindex="-1" {href} on:click>

        </a>
      </div>
      <slot />
    {/if}
  </div>
{:else}
  <div class="card-item empty">
    
  </div>
{/if}

<style>
  .card-body {
    width: auto;
    display: flex;
    background-color: var(--color-dark-bg-2);
    box-shadow: 0 0 0 1px var(--color-dark-border) inset;
    aspect-ratio: 1/1;
    border-radius: var(--radius-s);
  }

  .card-item {
    white-space: nowrap;
    margin-bottom: var(--space-s);
  }

  .empty {
    visibility: hidden;
  }

  .round {
    border-radius: var(--radius-l);
  }

  .round *:focus {
    border-radius: var(--radius-l);
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
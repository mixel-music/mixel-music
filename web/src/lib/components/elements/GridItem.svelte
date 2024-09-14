<script lang="ts">
  import { getArtwork } from "$lib/tools";

  export let lazyload: boolean = false;
  export let href: string | undefined = undefined;
  export let alt: string | undefined = undefined;
  export let src: string | undefined = undefined;
  export let round: boolean = false;
  export let Empty: boolean = false;

  $: showArtwork = true;
</script>

{#if !Empty}
  <div class="grid-item">
    {#if src}
      <div class="item-body {round ? 'round' : ''}">
        <a tabindex="-1" {href} on:click>
          {#if showArtwork}
            <img
              loading={lazyload ? 'lazy' : null}
              src={getArtwork(src, 300)} {alt} on:error={() => showArtwork = !showArtwork}
            >
          {/if}
        </a>
      </div>

      <slot />
    {:else}
      <div class="item-body {round ? 'round' : ''}">
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
  .grid-item {
    white-space: nowrap;
    margin-bottom: var(--space-s);
  }

  .item-body {
    width: auto;
    display: flex;
    background-color: var(--dark-element);
    box-shadow: 0 0 0 1px var(--dark-border) inset;
    aspect-ratio: 1/1;
    border-radius: var(--radius-s);
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
<script lang="ts">
  export let type: string | undefined = undefined;
  export let href: string | undefined = undefined;
  export let width: string = '42px';
  export let height: string = '42px';
  export let preload: string = 'false';
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<svelte:element
  data-sveltekit-preload-data={preload ? preload : 'false'}
  type={href ? undefined : type}
  this={href ? 'a' : 'button'}
  style:height={height}
  style:width={width}
  on:click
  on:focus
  {href}
>
  <slot />
</svelte:element>

<style>
  a, button {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-dark-text-2);
    background-color: var(--dark-bg-2);
    border: 1px solid var(--color-dark-border);
    transition: 0.2s ease;
    font-size: 18px;

    border-radius: var(--radius-l);
    padding: var(--space-xs);
  }

  a:hover, button:hover {
    color: var(--color-dark-text-1);
    transition: 0.2s ease;
  }
</style>

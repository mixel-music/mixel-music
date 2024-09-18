<script lang="ts">
  export let type: string | undefined = undefined;
  export let href: string | undefined = undefined;
  export let width: string = '1px';
  export let height: string = '1px';
  export let preload: string = 'false';
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<svelte:element
  data-sveltekit-preload-data={preload ? preload : 'false'}
  type={href ? undefined : type}
  this={href ? 'a' : 'button'}
  style:height={height}
  style:width={width}
  {...$$restProps}
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
    color: var(--dark-text-sub);
    transition: 0.2s ease;
    font-size: 24px;
    background-color: transparent;
    border: none;
  }

  a:hover, button:hover {
    color: var(--dark-text);
    transition: 0.2s ease;
  }
</style>
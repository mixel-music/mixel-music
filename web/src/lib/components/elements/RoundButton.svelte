<script lang="ts">
  export let type: string | undefined = undefined;
  export let href: string | undefined = undefined;
  export let title: string | undefined = undefined;
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
  {...$$restProps}
  title={title}
  on:click
  on:focus
  {href}
>
  <slot />
</svelte:element>

<style>
  a, button {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: var(--dark-text-sub);
    background-color: var(--dark-element);
    border: 1px solid var(--dark-border);
    transition: 0.2s ease;
    font-weight: 500;
    font-size: 18px;

    border-radius: var(--radius-l);
    padding: var(--space-xs);
    text-decoration: none;
  }

  a:hover, button:hover {
    color: var(--dark-text);
    transition: 0.2s ease;
  }
</style>

<script lang="ts">
  import Icon from "@iconify/svelte";

  export let type: string | undefined = undefined;
  export let href: string | undefined = undefined;
  export let title: string | undefined = undefined;
  export let button: string = '';
  export let iconName: string = '';
  export let iconSize: string = '';
  export let width: string = '42px';
  export let height: string = '42px';
  export let preload: string = 'false';
</script>

<!-- svelte-ignore a11y-no-static-element-interactions -->
<svelte:element
  class:round={button == 'round'}
  class:square={button == 'square'}
  class:custom={button == 'custom'}
  data-sveltekit-preload-data={preload}
  type={href ? undefined : type}
  this={href ? 'a' : 'button'}
  title={title}
  style:width={width}
  style:height={button != 'round' ? height : width}
  {...$$restProps}
  on:click
  on:focus
  {href}
>
  {#if iconName}
    <Icon
      icon={iconName}
      width={iconSize}
    />
  {/if}

  {#if button != 'round'}
    <slot />
  {/if}
</svelte:element>

<style>
  .round {
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

  .square {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    color: var(--dark-text-sub);
    background-color: var(--dark-element);
    border: 1px solid var(--dark-border);
    transition: 0.2s ease;
    font-weight: 500;
    font-size: 16px;

    border-radius: var(--radius-s);
    padding: var(--space-xs);
    gap: var(--space-xs);
    text-decoration: none;
  }

  .custom {
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--dark-text-sub);
    background-color: transparent;
    transition: 0.2s ease;
    text-decoration: none;
    font-size: 24px;
    border: none;
  }

  a:hover, button:hover {
    color: var(--dark-text);
    transition: 0.2s ease;
  }
</style>
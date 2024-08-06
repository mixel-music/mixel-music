<script lang="ts">
  import Icon from '@iconify/svelte';
  export let icon: string | undefined = undefined;
  export let title: string = '';
  export let href: string = '';
</script>

<a
  {href}
  on:click
  class="button"
  data-sveltekit-noscroll
>
  {#if icon}
    <Icon {icon} />
  {/if}
  {title}
</a>

<style>
  .button {
    display: flex;
    align-items: center;
    justify-content: center;

    width: 42px;
    height: 42px;

    padding: 12px;
    font-size: 18px;
    transition: 0.2s ease;

    color: var(--color-dark-text-2);
    background-color: var(--color-dark-bg-2);
    border: 1px solid var(--color-dark-border);
    border-radius: 50%;
  }

  .button:hover {
    color: var(--color-dark-text-1);
    transition: 0.2s ease;
  }
</style>
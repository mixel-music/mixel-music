<script lang="ts">
  import Icon from '@iconify/svelte';
  export let icon: string | undefined = undefined;
  export let href: string | undefined = undefined;
</script>

<li>
  <a {href} on:click>
    {#if icon}
      <span>
        <Icon {icon} />
      </span>
    {/if}

    <slot />
  </a>
</li>

<style>
  li {
    list-style: none;
    padding: 0 12px;
    border-radius: var(--radius-m);
  }

  a {
    display: flex;
    align-items: center;
    gap: var(--space-xs);
    width: 100%;
    font-size: 15px;
    padding: 6px 12px;
    border-radius: var(--radius-m);
    text-decoration: none;
  }

  a:hover,
  a:focus,
  a:active {
    outline-offset: 8px;
  }

  a:hover {
    background-color: var(--black-4);
  }

  span {
    min-height: 36px;
    display: flex;
    font-size: 21px;
    color: var(--dark-text-sub);
    align-items: center;
    justify-content: center;
  }
</style>

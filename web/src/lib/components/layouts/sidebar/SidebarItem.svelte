<script lang="ts">
  import Icon from '@iconify/svelte';
  export let icon: string | undefined = undefined;
  export let href: string;
</script>

<li>
  <a {href}>
    {#if icon}
      <span>
        <Icon {icon} width="24" height="24" />
      </span>
    {/if}

    <slot />
  </a>
</li>

<style>
  li {
    display: flex;
    margin-bottom: var(--space-s);
    align-items: center;
  }

  a {
    display: flex;
    align-items: center;
    min-height: 36px;
    width: 100%;
  }

  a:hover,
  a:focus,
  a:active {
    outline-offset: 8px;
  }

  span {
    width: 36px;
    min-height: 36px;
    display: flex;
    color: var(--dark-text-sub);
    align-items: center;
    justify-content: center;
  }
</style>

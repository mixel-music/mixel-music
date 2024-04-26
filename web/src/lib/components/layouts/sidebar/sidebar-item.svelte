<script lang="ts">
  import Icon from '@iconify/svelte';

  export let link: string;
  export let icon: string | undefined = undefined;
  export let title: string;
</script>

<li>
  <a href={link}>
    {#if icon}
      <span class="sidebar-icon">
        <Icon icon={icon} width="24" height="24"></Icon>
      </span>
    {/if}
    {title}
  </a>
</li>

<style>
  .sidebar-icon {
    width: 36px;
    min-height: 36px;
    display: flex;
    color: var(--color-dark-text-2);
    align-items: center;
    justify-content: center;
  }

  li {
    display: flex;
    margin-bottom: 16px;
    align-items: center;
  }

  a {
    display: flex;
    align-items: center;
    min-height: 36px;
    width: 100%;
  }

  a:focus {
    outline-offset: 8px;
  }
</style>
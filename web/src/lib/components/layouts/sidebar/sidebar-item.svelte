<script lang="ts">
  import Icon from '@iconify/svelte';

  export let href: string;
  export let icon: string | undefined = undefined;
  export let title: string;
</script>

<li>
  <a {href}>
    {#if icon}
      <span>
        <Icon {icon} width="24" height="24" />
      </span>
    {/if}

    {title}
  </a>
</li>

<style>
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

    & span {
      width: 36px;
      min-height: 36px;
      display: flex;
      color: var(--color-dark-text-2);
      align-items: center;
      justify-content: center;
    }
  }

  a:hover, a:active, a:focus {
    outline-offset: 8px;
  }
</style>
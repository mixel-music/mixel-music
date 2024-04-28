<script lang="ts">
  import Icon from '@iconify/svelte';

  export let title: string | undefined = undefined;
  export let icon: string | undefined = undefined;
  export let disabled: boolean = false;
  export let turn_off: boolean = false;
  export let control_button: boolean = false;
  export let primary_button: boolean = false;
  export let text: string = '';
</script>

<button
  {title}
  on:click
  style:padding={control_button ? '0 16px' : ''}
  style:color={turn_off ? 'var(--color-dark-disabled)' : null}
  {disabled}
>
  {#if icon}
    <Icon
      {icon}
      width={primary_button ? '29' : '24'}
      height={primary_button ? '29' : '24'}
    />
  {/if}

  {text}
</button>

<style>
  button {
    display: flex;
    padding: 12px;
    border: none;
    background-color: transparent;
    color: var(--color-dark-text-1);
    transition: 0.2s ease;
    align-items: center;
    justify-content: center;
  }

  button:hover {
    color: var(--color-dark-focus);
    transition: all 0.2s ease;
  }
</style>
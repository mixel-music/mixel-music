<script lang="ts">
  import Icon from '@iconify/svelte';

  export let title: string | undefined = undefined;
  export let icon: string | undefined = undefined;
  export let disabled: boolean = false;
  export let ControlButton: boolean = false;
  export let PrimaryButton: boolean = false;
  export let state: boolean = false;
  export let text: string = '';
</script>

<button
  {title}
  on:click
  class:control-button={ControlButton}
  class:primary-button={PrimaryButton}
  class:turn-off={state}
  aria-disabled={disabled}
  {disabled}
>
  {#if icon}
    <Icon
      {icon}
      width={PrimaryButton ? '29' : '23'}
      height={PrimaryButton ? '29' : '23'}
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

  .control-button {
    width: 32px;
    height: 32px;
    padding: 3px;
  }

  .turn-off {
    color: var(--color-dark-disabled);
  }
</style>
<script lang="ts">
  import Icon from '@iconify/svelte';
  
  export let alt: string = '';
  export let off: boolean = false;
  export let icon: string = '';
  export let text: string = '';
  export let disabled: boolean = false;
  export let ControlButton: boolean = false;
  export let PrimaryButton: boolean = false;
</script>

<button
  on:click
  title={alt}
  class:off={off}
  class:control={ControlButton}
  class:primary={PrimaryButton}
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
    transition: 0.2s ease;
    color: var(--dark-text);
    background-color: transparent;
    justify-content: center;
    align-items: center;
  }

  button:focus {
    outline: none;
  }

  button:hover {
    color: var(--dark-hover);
    transition: all 0.2s ease;
  }

  button:active {
    color: var(--dark-active);
  }

  .control {
    width: 32px;
    height: 32px;
    padding: 3px;
  }

  .off {
    color: var(--dark-disabled);
  }
</style>
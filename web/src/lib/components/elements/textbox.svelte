<script lang="ts">
  export let type: string = 'text';
  export let name: string = 'text';
  export let placeholder: string = '';
  export let disabled: boolean = false;
  export let width: string = '100%';
  export let value: string = '';
</script>

<input
  {type}
  {name}
  {value}
  {disabled}
  {placeholder}
  style:width={width}
/>

<style>
  input {
    height: 100%;
    padding: 12px;
    background-color: var(--dark-element);
    border: 1px solid var(--dark-border);
    border-radius: var(--radius-m);
    color: var(--dark-text);
    font-family: var(--font-family);
    transition: all 0.2s ease;
    backdrop-filter: blur(32px);
  }
</style>

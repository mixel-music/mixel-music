<script lang="ts">
  export let size = 'm';

  $: flexSize = {
    xs: 0.2,
    s: 1,
    m: 2,
    l: 3,
    xl: 5
  }[size] || 1;
</script>

<div style={`flex: ${flexSize};`}>
  <slot />
</div>

<style>
  div {
    font-weight: bold;
    color: var(--color-dark-text-2);
    font-size: 75%;
    text-transform: uppercase;
    letter-spacing: 0.3px;
    display: flex;
    padding: var(--table-padding);
    text-align: left;
  }
</style>
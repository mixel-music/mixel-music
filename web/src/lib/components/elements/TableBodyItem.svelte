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
    padding: var(--table-padding);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
</style>
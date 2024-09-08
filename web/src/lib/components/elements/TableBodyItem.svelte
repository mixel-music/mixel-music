<script lang="ts">
  export let size = 'm';

  $: flexSize = {
    xs: 0.3,
    s: 1,
    m: 2,
    l: 3,
    xl: 5
  }[size] || 1;
</script>

<div class="table-body-item" style={`flex: ${flexSize};`}>
  <slot />
</div>

<style>
  .table-body-item {
    padding: var(--table-padding);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
</style>
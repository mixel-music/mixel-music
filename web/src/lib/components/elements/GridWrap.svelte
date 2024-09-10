<script lang="ts">

</script>

<div>
  <slot />
</div>

<style>
  div {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    grid-gap: var(--space-m);
    overflow-x: hidden;
  }
</style>
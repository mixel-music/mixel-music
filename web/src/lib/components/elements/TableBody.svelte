<script lang="ts">
  export let columnRatios: number[];
</script>

<div class="table-body">
  <slot />
</div>

<style>
  .table-body {
    display: flex;
    flex-direction: column;
    width: 100%;
  }
</style>
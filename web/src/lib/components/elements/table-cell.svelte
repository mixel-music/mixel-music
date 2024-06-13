<script lang="ts">
  export let text: string;
</script>

<div class="table-item">
  <span>
    { text }
  </span>
</div>

<style>
  .table-item {
    padding: var(--app-padding-s);
  }
</style>
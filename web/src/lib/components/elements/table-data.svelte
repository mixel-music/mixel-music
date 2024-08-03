<script lang="ts">
  export let text: string;
  export let bold: boolean = false;
  export let right: boolean = false;
  export let large: boolean = false;
</script>

<td
  class="table-item"
  class:bold={bold}
  class:right={right}
  class:large={large}
>
  <span>
    { text }
  </span>
</td>

<style>
  .table-item {
    padding: var(--app-padding-s);
    width: 3%;
    min-width: 3%;
    max-width: 10%;
    box-sizing: border-box;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  .bold {
    font-weight: bold;
  }

  .right {
    text-align: right;
  }

  .large {
    width: 80%;
    width: min-content;
  }
</style>
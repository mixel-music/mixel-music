<script lang="ts">
  import TabHeader from "./tab-header.svelte";

  export let title: string | undefined = undefined;
</script>

<TabHeader title={title} />

<div>
  <slot />
</div>

<style>
  div {
    display: grid;
    grid-gap: 21px;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    overflow-x: hidden;
  }
</style>
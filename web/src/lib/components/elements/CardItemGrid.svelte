<script lang="ts">
  import PageTitle from "./PageTitle.svelte";
  export let title: string | undefined = undefined;
</script>

<PageTitle {title} />
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
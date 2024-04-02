<script lang="ts">
export let title: string;

</script>

<div class="content-header">
  <span class="content-title">
    {#if title}
      {title}
    {/if}
  </span>
</div>

<style>
.content-header {
  margin: 72px 0 21px 0;
}

.content-title {
  font-size: 64px;
  font-weight: bolder;
  letter-spacing: -1px;
}
</style>
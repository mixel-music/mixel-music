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
  margin: 24px 0 21px 0;
}

.content-title {
  font-size: 36px;
  font-weight: bolder;
  letter-spacing: -1px;
  line-height: 1;
}
</style>
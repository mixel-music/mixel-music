<script lang="ts">
  export let title: string | undefined;
</script>

{#if title}
<div>
  <span>
    {title}
  </span>
</div>
{/if}

<style>
  div {
    margin: 21px 0;
  }

  span {
    font-size: 32px;
    font-weight: bolder;
    letter-spacing: -1px;
    line-height: 1;
  }
</style>
<script lang="ts">
  export let title: string;
</script>

<div>
  <span>
    {#if title}
      {title}
    {/if}
  </span>
</div>

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
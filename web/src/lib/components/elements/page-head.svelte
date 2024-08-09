<script lang="ts">
  export let title: string | undefined;
  export let inline: boolean = false;
</script>

{#if title}
<div style:display={ inline ? 'inline' : ''}>
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
    font-size: 36px;
    font-weight: bolder;
    letter-spacing: -1px;
    line-height: 1;
  }
</style>
<script lang="ts">
  export let title: string;
  export let inline: boolean = false;
</script>

{#if title}
  <div style:display={ inline ? 'inline' : ''}>
    <span>{title}</span>
  </div>
{/if}

<style>
  div {
    margin-top: var(--space-l);
    margin-bottom: var(--space-m);
  }

  span {
    font-size: 32px;
    font-weight: bolder;
    letter-spacing: -1px;
    line-height: 1;
  }
</style>

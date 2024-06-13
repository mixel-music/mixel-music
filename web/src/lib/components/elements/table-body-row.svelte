<script lang="ts">
  export let title: boolean;
</script>

{#if title}
<div class="bold">
  <slot />
</div>
{:else}
<div class="normal">
  <slot />
</div>
{/if}

<style>
  .bold {
    font-weight: 600;
  }

  .normal {

  }
</style>
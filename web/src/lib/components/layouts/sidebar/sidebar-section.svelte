<script lang="ts">
  export let title: string | undefined = undefined;
</script>

<ul title={title}>
  <slot />
</ul>

<style>
  ul[title]::before {
    content: attr(title);
    display: flex;
    margin-top: 36px;
    margin-bottom: 12px;
    color: var(--color-dark-text-2);
    font-size: smaller;
  }

  ul {
    list-style: none;
  }
</style>
<script lang="ts">
  export let title: string | undefined = undefined;
</script>

<ul {title}>
  <slot />
</ul>

<style>
  ul[title]::before {
    display: flex;
    margin-top: 36px;
    margin-bottom: 12px;
    
    font-size: smaller;
    content: attr(title);
    color: var(--color-dark-text-2);
  }

  ul {
    list-style: none;
  }
</style>
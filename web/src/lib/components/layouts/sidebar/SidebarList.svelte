<script lang="ts">
  export let name: string | undefined = undefined;
</script>

<ul title={name}>
  <slot />
</ul>

<style>
  ul[title]::before {
    display: flex;
    font-size: 85%;
    color: var(--dark-text-sub);
    content: attr(title);
    margin-top: var(--space-l);
    margin-left: var(--space-s);
    margin-bottom: var(--space-xs);
  }

  ul {
    list-style: none;
  }
</style>

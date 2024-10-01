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
    margin-top: var(--space-l);
    margin-bottom: var(--space-s);
    content: attr(title);
    color: var(--dark-text-sub);
  }

  ul {
    list-style: none;
  }
</style>

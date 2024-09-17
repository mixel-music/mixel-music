<script lang="ts">
  import SquareButton from "./elements/SquareButton.svelte";
  import { _ } from 'svelte-i18n'
</script>

<div>
  <SquareButton
    href='.'
    width='150px'
    height='50px'
  >
    {$_('play')}
  </SquareButton>

  <SquareButton
    href='.'
    width='150px'
    height='50px'
  >
    {$_('shuffle')}
  </SquareButton>
</div>

<style>
  div {
    display: flex;
    margin-bottom: var(--space-l);
    gap: 12px;
  }
</style>
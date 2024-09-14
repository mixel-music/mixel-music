<script lang="ts">
  import SquareButton from "./elements/SquareButton.svelte";
</script>

<div>
  <SquareButton
    href='.'
    width='150px'
    height='50px'
  >
    Play
  </SquareButton>

  <SquareButton
    href='.'
    width='150px'
    height='50px'
  >
    Shuffle
  </SquareButton>
</div>

<style>
  div {
    display: flex;
    margin-bottom: var(--space-l);
    gap: 12px;
  }
</style>
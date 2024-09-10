<script lang="ts">
  import SquareButton from "./elements/SquareButton.svelte";
</script>

<div class="controls-bar">
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
  .controls-bar {
    display: flex;
    margin-bottom: var(--space-l);
    gap: 12px;
  }
</style>
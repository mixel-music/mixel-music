<script lang="ts">
  import Icon from "@iconify/svelte";
import SquareButton from "./elements/SquareButton.svelte";
  import { _ } from 'svelte-i18n'
  import RoundButton from "./elements/RoundButton.svelte";
</script>

<div class="controls-bar">
  <div>
    <SquareButton
      href='.'
      width='150px'
      height='50px'
    >
      <Icon icon="iconoir:play-solid" />
      {$_('play')}
    </SquareButton>

    <SquareButton
      href='.'
      width='150px'
      height='50px'
    >
    <Icon icon="iconoir:shuffle" />
      {$_('shuffle')}
    </SquareButton>
  </div>
  <div>
    <RoundButton width="50px" height="50px">
      <Icon icon="iconoir:heart" />
    </RoundButton>
    <SquareButton
      href='.'
      width='130px'
      height='50px'
    >
    <Icon icon="iconoir:info-circle-solid" />
      {$_('info')}
    </SquareButton>
    <SquareButton
      href='.'
      width='130px'
      height='50px'
    >
    <Icon icon="iconoir:download" />
      {$_('download')}
    </SquareButton>
  </div>
</div>

<style>
  .controls-bar {
    display: flex;
    margin-bottom: var(--space-l);
    justify-content: space-between;
  }

  .controls-bar > div {
    display: flex;
    gap: var(--space-xs);
  }
</style>
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
      title={$_('controls.play')}
    >
      <Icon icon="iconoir:play-solid" />
      {$_('controls.play')}
    </SquareButton>

    <SquareButton
      href='.'
      width='150px'
      height='50px'
      title={$_('controls.shuffle')}
    >
    <Icon icon="iconoir:shuffle" />
      {$_('controls.shuffle')}
    </SquareButton>
  </div>
  <div>
    <RoundButton
      width="50px"
      height="50px"
      title={$_('controls.favorite')}
    >
      <Icon icon="iconoir:heart" width="21" height="21" />
    </RoundButton>
    
    <SquareButton
      href='.'
      width='130px'
      height='50px'
      title={$_('controls.info')}
    >
    <Icon icon="iconoir:info-circle-solid" />
      {$_('controls.info')}
    </SquareButton>

    <SquareButton
      href='.'
      width='140px'
      height='50px'
      title={$_('controls.download')}
    >
    <Icon icon="iconoir:download" />
      {$_('controls.download')}
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
    gap: var(--space-s);
  }
</style>
<script lang="ts">
  import RoundButton from '$lib/components/elements/RoundButton.svelte';
  import Dropdown from '$lib/components/elements/Dropdown.svelte';
  import TextBox from '$lib/components/elements/Textbox.svelte';
  import Icon from '@iconify/svelte';
  import { _ } from 'svelte-i18n'
</script>

<nav>
  <div>
    <RoundButton on:click={() => history.back()}>
      <Icon icon="iconoir:nav-arrow-left" />
    </RoundButton>
    <RoundButton on:click={() => history.forward()}>
      <Icon icon="iconoir:nav-arrow-right" />
    </RoundButton>
  </div>

  <div>
    <TextBox
      name="search"
      type="search"
      width="290px"
      placeholder={$_('navbar.search')}
    />
    <RoundButton>
      <Icon icon="iconoir:refresh" />
    </RoundButton>
    <RoundButton>
      <Icon icon="iconoir:user" />
    </RoundButton>
  </div>
</nav>

<style>
  nav {
    position: sticky;
    max-width: 100%;
    top: 0;

    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-m) 0;
    padding-bottom: var(--space-m);
  }

  div {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }
</style>
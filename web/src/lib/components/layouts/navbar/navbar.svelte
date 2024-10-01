<script lang="ts">
  import Dropdown from '$lib/components/elements/Dropdown.svelte';
  import TextBox from '$lib/components/elements/Textbox.svelte';
  import Button from '$lib/components/elements/Button.svelte';
  import { _ } from 'svelte-i18n'
</script>

<nav>
  <div>
    <Button
      button='round'
      iconName='iconoir:nav-arrow-left'
      on:click={() => history.back()}
    />
    <Button
      button='round'
      iconName='iconoir:nav-arrow-right'
      on:click={() => history.forward()}
    />
  </div>

  <div>
    <TextBox
      name="search"
      type="search"
      width="290px"
      placeholder={$_('navbar.search')}
    />
    <Button button='round' iconName='iconoir:refresh' />
    <Button button='round' iconName='iconoir:user' />
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

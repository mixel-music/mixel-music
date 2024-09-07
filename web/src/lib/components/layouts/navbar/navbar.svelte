<script lang="ts">
  import ButtonRound from '$lib/components/elements/ButtonRound.svelte';
  import TextBox from '$lib/components/elements/TextBox.svelte';
  import Icon from '@iconify/svelte';
</script>

<nav>
  <div>
    <ButtonRound on:click={() => history.back()}>
      <Icon icon="iconoir:nav-arrow-left" />
    </ButtonRound>
    <ButtonRound on:click={() => history.forward()}>
      <Icon icon="iconoir:nav-arrow-right" />
    </ButtonRound>
  </div>

  <div>
    <TextBox
      name="search"
      type="search"
      width="290px"
      placeholder="Search"
    />
    <ButtonRound>
      <Icon icon="iconoir:refresh" />
    </ButtonRound>
    <ButtonRound>
      <Icon icon="iconoir:user" />
    </ButtonRound>
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
    padding: 24px 0;
  }

  div {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }
</style>
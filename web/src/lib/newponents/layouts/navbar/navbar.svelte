<script lang="ts">
  import ButtonRd from '$lib/newponents/elements/button-rd.svelte';
  import TextBox from '$lib/newponents/elements/textbox.svelte';
  import Icon from '@iconify/svelte';
</script>

<nav>
  <div>
    <ButtonRd on:click={() => history.back()}>
      <Icon icon="iconoir:nav-arrow-left" />
    </ButtonRd>
    <ButtonRd on:click={() => history.forward()}>
      <Icon icon="iconoir:nav-arrow-right" />
    </ButtonRd>
  </div>

  <div>
    <TextBox
      name="search"
      type="search"
      width="290px"
      placeholder="Search"
    />
    <ButtonRd>
      <Icon icon="iconoir:refresh" />
    </ButtonRd>
    <ButtonRd>
      <Icon icon="iconoir:user" />
    </ButtonRd>
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
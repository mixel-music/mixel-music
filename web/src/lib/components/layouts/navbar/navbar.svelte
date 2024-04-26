<script lang="ts">
  import NavbarButton from '$lib/components/layouts/navbar/navbar-button.svelte';
  import SearchBar from '$lib/components/elements/search-bar.svelte';
</script>

<nav>
  <div>
    <NavbarButton
      icon="iconoir:nav-arrow-left"
      on:click={() => history.back()}
    />
    <NavbarButton
      icon="iconoir:nav-arrow-right"
      on:click={() => history.forward()}
    />
  </div>

  <div>
    <SearchBar width="290px" />
    <NavbarButton
      icon="iconoir:refresh"
    />
    <NavbarButton
      icon="iconoir:user"
    />
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
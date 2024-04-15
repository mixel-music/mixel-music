<script lang="ts">
  import Icon from '@iconify/svelte';
</script>

<nav class="navbar">
  <div class="navbar-area">
    <div class="navbar-area-1">
      <button
        type="button"
        class="navbar-link navbar-explore"
        on:click={() => history.back()}
      >
        <Icon icon="iconoir:nav-arrow-left"></Icon>
      </button>
      <button
        type="button"
        class="navbar-link navbar-explore"
        on:click={() => history.forward()}
      >
        <Icon icon="iconoir:nav-arrow-right"></Icon>
      </button>
    </div>

    <div class="navbar-area-2">
    </div>

    <div class="navbar-area-3">
    </div>
  </div>
</nav>

<style>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  padding: 24px 0;
  max-width: 100%;
  user-select: none;
}

.navbar-area {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.navbar-area-1 {
  display: flex;
  align-items: center;
  gap: 12px;
  cursor: pointer;
}

.navbar-area-3 {
  display: flex;
  align-items: center;
  padding: var(--app-padding-l) 0;
  gap: 12px;
}

.navbar-link {
  display: flex;
  align-items: center;
  color: var(--color-dark-text-2);
  font-size: 18px;
  font-weight: 600;
  transition: 0.2s ease;
}

.navbar-link:hover {
  color: var(--color-dark-text-1);
  transition: 0.2s ease;
}

.navbar-explore {
  align-items: center;
  justify-content: center;
  flex-direction: row-reverse;
  margin: 0;
  padding: 12px;
  width: 42px;
  height: 42px;
  background-color: var(--color-dark-bg-2);
  border: 1px solid var(--color-dark-border);
  border-radius: 50%;
}
</style>
<script lang="ts">
import IconamoonArrowLeft2 from '~icons/iconamoon/arrow-left-2';
import IconamoonArrowRight2 from '~icons/iconamoon/arrow-right-2';
</script>

<nav class="navbar">
  <div class="navbar-area">
    <div class="navbar-area-1">
      <button
        type="button"
        class="navbar-link navbar-explore"
        on:click={() => history.back()}
      >
        <IconamoonArrowLeft2 class="navbar-icon" />
      </button>
      <button
        type="button"
        class="navbar-link navbar-explore"
        on:click={() => history.forward()}
      >
        <IconamoonArrowRight2 class="navbar-icon" />
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
  user-select: none;
  max-width: 100%;
}

.navbar-area {
  width: 100%;
  display: flex;
  padding: 32px 0;
  align-items: center;
  justify-content: space-between;
}

.navbar-area-1 {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  text-wrap: nowrap;
  cursor: pointer;
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

.navbar-area-3 {
  display: flex;
  align-items: center;
  padding: var(--app-padding-l) 0;
  gap: 12px;
}

.navbar-icon {
  font-size: 16px;
}

.navbar-explore {
  align-items: center;
  justify-content: center;
  flex-direction: row-reverse;
  margin: 0;
  padding: 11px;
  border: 1px solid var(--color-dark-border);
  border-radius: 50%;
  background-color: var(--color-dark-nav-itm);
  backdrop-filter: blur(32px);
}
</style>
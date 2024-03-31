<script lang="ts">
import IconamoonArrowLeft2 from '~icons/iconamoon/arrow-left-2';
import IconamoonArrowRight2 from '~icons/iconamoon/arrow-right-2';
import IconamoonProfileCircle from '~icons/iconamoon/profile-circle';
import logo from '$lib/images/mixel-music.svg';
</script>

<nav class="navbar">
  <div class="navbar-area">
    <div class="navbar-area-left">
      <span class="navbar-link" id="navbar-logo">
        <a href="/">
          <img src="{logo}" alt="mixel-music" width="32px">
        </a>
      </span>
      <span class="navbar-link">
        <a href="/albums">Albums</a>
      </span>
      <span class="navbar-link">
        <a href="/tracks">Tracks</a>
      </span>
      <span class="navbar-link">
        <a href="/artists">Artists</a>
      </span>
    </div>

    <div class="navbar-area-center">
      
    </div>

    <div class="navbar-area-right">
      <input type="text" id="navbar-input" name="Search" placeholder="Search">
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
  </div>
</nav>

<style>
.navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  width: 100%;
  height: 96px;
  background-color: var(--color-dark-nav);
  backdrop-filter: blur(32px);
  user-select: none;
}

.navbar-area {
  width: 100%;
  display: flex;
  padding: 0 16px;
  align-items: center;
  justify-content: space-between;
}

.navbar-area-left {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 21px;
  padding: var(--app-padding-l) 0;
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

#navbar-logo {
  font-size: 0;
}

.navbar-area-right {
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
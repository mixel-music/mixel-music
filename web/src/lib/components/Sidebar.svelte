<script lang="ts">
  import Icon from '@iconify/svelte';
  import logo from '$lib/images/mixel-music.svg';
</script>

<div class="sidebar">
  <div class="sidebar-logo">
    <a href="/">
      <img src={logo} alt="mixel-music" width="42px">
    </a>
  </div>
  <ul class="sidebar-list">
    <li>
      <a href="/albums">
        <span class="sidebar-icon">
          <Icon icon="iconoir:compact-disc" width="24" height="24"></Icon>
        </span>
        Albums
      </a>
    </li>
    <li>
      <a href="/tracks">
        <span class="sidebar-icon">
          <Icon icon="iconoir:music-double-note" width="24" height="24"></Icon>
        </span>
        Tracks
      </a>
    </li>
    <li>
      <a href="/artists">
        <span class="sidebar-icon">
          <Icon icon="iconoir:microphone" width="24" height="24"></Icon>
        </span>
        Artists
      </a>
    </li>
    <li>
      <a href="#">
        <span class="sidebar-icon">
          <Icon icon="iconoir:headset" width="24" height="24"></Icon>
        </span>
        Mixes
      </a>
    </li>
  </ul>
</div>

<style>
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  z-index: 0;
  
  width: 250px;
  height: 100%;

  padding-left: 21px;
  padding-right: 21px;
  padding-top: 24px;
  padding-bottom: 24px;

  background-color: var(--color-dark-bg-2);
  border-right: 1px solid var(--color-dark-border);
}

.sidebar-logo {
  display: flex;
  align-items: center;
  font-size: 0;
}

.sidebar-list {
  list-style: none;

  & .sidebar-icon {
    width: 42px;
    height: 42px;
    font-size: 19px;
    display: flex;
    color: var(--color-dark-text-2);
    align-items: center;
    justify-content: center;
  }

  & li {
    display: flex;
    margin: 16px 0;
  }

  & a {
    display: flex;
    align-items: center;
    width: 100%;
  }
}
</style>
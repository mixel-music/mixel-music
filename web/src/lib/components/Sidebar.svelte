<script lang="ts">
import IconamoonPlaylist from '~icons/iconamoon/playlist';
import IconamoonMusicAlbum from '~icons/iconamoon/music-album';
import IconamoonMusic2 from '~icons/iconamoon/music-2';
import IconamoonMusicArtist from '~icons/iconamoon/music-artist';
import IconamoonHeadphone from '~icons/iconamoon/headphone';
import IconamoonSignPlus from '~icons/iconamoon/sign-plus';
import logo from '$lib/images/mixel-music.svg';
</script>

<div class="sidebar">
  <div class="sidebar-logo">
    <a href="/">
      <img src={logo} alt="mixel-music" width="42px">
    </a>
  </div>
  <ul class="sidebar-list">
    <!-- <input type="text"> -->
    <li>
      <a href="/albums">
        <span class="sidebar-icon">
          <IconamoonMusicAlbum />
        </span>
        Albums
      </a>
    </li>
    <li>
      <a href="/tracks">
        <span class="sidebar-icon">
          <IconamoonMusic2 />
        </span>
        Tracks
      </a>
    </li>
    <li>
      <a href="/artists">
        <span class="sidebar-icon">
          <IconamoonMusicArtist />
        </span>
        Artists
      </a>
    </li>
    <li>
      <a href="#">
        <span class="sidebar-icon">
          <IconamoonPlaylist />
        </span>
        Playlists
      </a>
    </li>
    <li>
      <a href="#">
        <span class="sidebar-icon">
          <IconamoonHeadphone />
        </span>
        Mixes
      </a>
    </li>
  </ul>
</div>

<style>
.sidebar {
  width: 250px;
  background-color: var(--color-dark-bg-2);
  position: fixed;
  top: 0;
  left: 0;
  z-index: 0;
  min-height: 100%;
  padding: 32px 16px;
  border-right: 1px solid var(--color-dark-border);
}

.sidebar-logo {
  display: flex;
  align-items: center;
  margin-bottom: 55.2px; /* 133.2 - 78px */
}

.sidebar-list {
  list-style: none;
}

.sidebar-list li {
  display: flex;
  margin: 12px 0;
  font-size: 18px;
  font-weight: 600;
}

.sidebar-list a {
  display: flex;
  align-items: center;
  gap: 12px;
}

.sidebar-icon {
  width: 36px;
  height: 36px;
  font-size: 21px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
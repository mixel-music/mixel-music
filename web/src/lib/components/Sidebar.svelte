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
  padding: 21px;
  border-right: 1px solid var(--color-dark-border);
}

.sidebar-logo {
  display: flex;
  font-size: 0;
  align-items: center;
}

.sidebar-list {
  list-style: none;
  margin-top: 42px;
}

.sidebar-list li {
  display: flex;
  margin: 16px 0;
  font-weight: 500;
}

.sidebar-list a {
  display: flex;
  align-items: center;
  gap: 12px;
  width: 100%;
}

.sidebar-icon {
  width: 32px;
  height: 32px;
  font-size: 21px;
  display: flex;
  color: var(--color-dark-text-2);
  align-items: center;
  justify-content: center;
}
</style>
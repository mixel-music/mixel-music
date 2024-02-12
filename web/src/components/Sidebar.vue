<template>
  <div class="sidebar-item sidebar-item-top">
    <router-link to="/" class="sidebar-link">
      <!-- <IconamoonHome class="sidebar-icon" /> -->
      <span class="sidebar-text">Home</span>
    </router-link>
  </div>
  <div class="sidebar-divider"></div>
  <div class="sidebar-item">
    <router-link to="/tracks" class="sidebar-link">
      <!-- <IconamoonMusic2 class="sidebar-icon" /> -->
      <span class="sidebar-text">Songs</span>
    </router-link>
  </div>
  <div class="sidebar-item">
    <router-link to="/artists" class="sidebar-link">
      <!-- <IconamoonMusicArtist class="sidebar-icon" /> -->
      <span class="sidebar-text">Artists</span>
    </router-link>
  </div>
  <div class="sidebar-item">
    <router-link to="/albums" class="sidebar-link">
      <!-- <IconamoonMusicAlbum class="sidebar-icon" /> -->
      <span class="sidebar-text">Albums</span>
    </router-link>
  </div>
  <div class="sidebar-item">
    <router-link to="/mixes" class="sidebar-link">
      <!-- <IconamoonHeadphone class="sidebar-icon" /> -->
      <span class="sidebar-text">Radio</span>
    </router-link>
  </div>
  <div class="sidebar-divider"></div>
  <div class="sidebar-item">
    <router-link to="/playlists" class="sidebar-link">
      <!-- <IconamoonPlaylist class="sidebar-icon" /> -->
      <span class="sidebar-text">Playlists</span>
    </router-link>
  </div>
</template>

<script>
import IconamoonHome from '~icons/iconamoon/home';
import IconamoonPlaylist from '~icons/iconamoon/playlist';
import IconamoonMusicAlbum from '~icons/iconamoon/music-album';
import IconamoonMusic2 from '~icons/iconamoon/music-2';
import IconamoonMusicArtist from '~icons/iconamoon/music-artist';
import IconamoonHeadphone from '~icons/iconamoon/headphone';

export default {
  components: {
    IconamoonHome,
    IconamoonMusicAlbum,
    IconamoonMusic2,
    IconamoonMusicArtist,
    IconamoonPlaylist,
    IconamoonHeadphone,
  },
}
</script>
<template>
  <div class="sidebar-item">
    <IconamoonPlaylist class="sidebar-icon" />
    <router-link to="/playlists" class="sidebar-link">
      Playlists
    </router-link>
  </div>
  <div class="sidebar-item">
    <IconamoonMusicAlbum class="sidebar-icon" />
    <router-link to="/albums" class="sidebar-link">
      Albums
    </router-link>
  </div>
  <div class="sidebar-item">
    <IconamoonMusic2 class="sidebar-icon" />
    <router-link to="/tracks" class="sidebar-link">
      Tracks
    </router-link>
  </div>
  <div class="sidebar-item">
    <IconamoonMusicArtist class="sidebar-icon" />
    <router-link to="/artists" class="sidebar-link">
      Artists
    </router-link>
  </div>
  <div class="sidebar-item">
    <IconamoonHeadphone class="sidebar-icon" />
    <router-link to="/mixes" class="sidebar-link">
      Mixes
    </router-link>
  </div>
</template>

<script>
import IconamoonPlaylist from '~icons/iconamoon/playlist';
import IconamoonMusicAlbum from '~icons/iconamoon/music-album';
import IconamoonMusic2 from '~icons/iconamoon/music-2';
import IconamoonMusicArtist from '~icons/iconamoon/music-artist';
import IconamoonHeadphone from '~icons/iconamoon/headphone';

export default {
  components: {
    IconamoonMusicAlbum,
    IconamoonMusic2,
    IconamoonMusicArtist,
    IconamoonPlaylist,
    IconamoonHeadphone,
  },
}
</script>
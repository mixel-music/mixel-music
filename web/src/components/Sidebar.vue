<template>
  <div class="sidebar-item sidebar-item-logo">
    <img src="/tamaya.svg" class="sidebar-logo">
  </div>
  <div class="sidebar-item">
    <Transition name="SidebarFade">
      <router-link to="/" class="sidebar-text">
        <!-- <IconamoonHome class="sidebar-icon" /> -->
        Home
      </router-link>
    </Transition>
  </div>
    <div class="sidebar-item">
      <Transition name="SidebarFade">
        <router-link to="/search" class="sidebar-text">
          Search
        </router-link>
      </Transition>
    </div>
  <div class="sidebar-item">
    <Transition name="SidebarFade">
      <router-link to="/library" class="sidebar-text">
        Library
      </router-link>
    </Transition>
  </div>
  <div class="sidebar-divider"></div>
  <div class="sidebar-item">
    <Transition name="SidebarFade">
      <router-link to="/albums" class="sidebar-link">
        <IconamoonMusicAlbum class="sidebar-icon" />
        &nbsp;
        Albums
      </router-link>
    </Transition>
  </div>
  <div class="sidebar-item">
    <Transition name="SidebarFade">
      <router-link to="/songs" class="sidebar-link">
        <IconamoonMusic2 class="sidebar-icon" />
        &nbsp;
        Songs
      </router-link>
    </Transition>
  </div>
  <div class="sidebar-item">
    <Transition name="SidebarFade">
      <router-link to="/artists" class="sidebar-link">
        <IconamoonMusicArtist class="sidebar-icon" />
        &nbsp;
        Artists
      </router-link>
    </Transition>
  </div>
  <div class="sidebar-item">
    <router-link to="/radios" class="sidebar-link">
      <IconamoonHeadphone class="sidebar-icon" />
      &nbsp;
      Radios
    </router-link>
  </div>
  <div class="sidebar-divider"></div>
  <div class="sidebar-item">
    <router-link to="/playlists" class="sidebar-text">
      Playlists
      <IconamoonSignPlus />
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
import IconamoonSignPlus from '~icons/iconamoon/sign-plus';

export default {
  components: {
    IconamoonHome,
    IconamoonMusicAlbum,
    IconamoonMusic2,
    IconamoonMusicArtist,
    IconamoonPlaylist,
    IconamoonHeadphone,
    IconamoonSignPlus,
  },
}
</script>
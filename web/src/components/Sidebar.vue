<template>
  <div class="sidebar-menu sidebar-menu-logo">
    <RouterLink to ="/" class="sidebar-link-logo">
      <img src="/tamaya.svg" class="sidebar-icon sidebar-icon-logo">
    </RouterLink>
  </div>
  <div class="sidebar-menu">
    <RouterLink to ="/" class="sidebar-link">
      <IconamoonHome class="sidebar-icon" />
      &nbsp;
      Home
    </RouterLink>
  </div>
  <div class="sidebar-menu">
    <RouterLink to ="/account" class="sidebar-link">
      <IconamoonProfile class="sidebar-icon" />
      &nbsp;
      Account
    </RouterLink>
  </div>
  <div class="sidebar-menu">
    <RouterLink to ="/settings" class="sidebar-link">
      <IconamoonSettings class="sidebar-icon" />
      &nbsp;
      Settings
    </RouterLink>
  </div>
  <div class="sidebar-group">
    <div class="sidebar-info" @click="ToggleMenu('Browse')">
      Browse
      <IconamoonArrowUp2Bold v-if="ToggleBrowse" />
      <IconamoonArrowDown2Bold v-else />
    </div>
    <Transition name="SidebarFade">
      <div class="MenuTransition" :class="{ MenuTransitionHidden: !ToggleBrowse }">
        <div class="sidebar-menu sidebar-menu-group">
          <RouterLink to="/" class="sidebar-link sidebar-link-group">
            <IconamoonMusicAlbum class="sidebar-icon" />
            &nbsp;
            Albums
          </RouterLink>
        </div>
        <div class="sidebar-menu sidebar-menu-group">
          <RouterLink to="/" class="sidebar-link sidebar-link-group">
            <IconamoonMusic2 class="sidebar-icon" />
            &nbsp;
            Tracks
          </RouterLink>
        </div>
        <div class="sidebar-menu sidebar-menu-group">
          <RouterLink to="/" class="sidebar-link sidebar-link-group">
            <IconamoonMusicArtist class="sidebar-icon" />
            &nbsp;
            Artists
          </RouterLink>
        </div>
        <!-- <div class="sidebar-menu sidebar-menu-group">
          <RouterLink to="/" class="sidebar-link sidebar-link-group">
            <IconamoonHeadphone class="sidebar-icon" />
            &nbsp;
            Mixes
          </RouterLink>
        </div> -->
      </div>
    </Transition>
  </div>
  <div class="sidebar-group">
    <div class="sidebar-info" @click="ToggleMenu('Playlists')">
      Playlists
      <IconamoonArrowUp2Bold v-if="TogglePlaylists" />
      <IconamoonArrowDown2Bold v-else />
    </div>
    <Transition name="SidebarFade">
      <div v-if="TogglePlaylists">
          <div class="sidebar-menu sidebar-menu-group">
              <RouterLink to="/" class="sidebar-link sidebar-link-group">
                <IconamoonSignPlusCircleBold />
                &nbsp;
                Create new
              </RouterLink>
          </div>
      </div>
    </Transition>
  </div>
</template>

<script>
import IconamoonArrowUp2Bold from '~icons/iconamoon/arrow-up-2-bold';
import IconamoonArrowDown2Bold from '~icons/iconamoon/arrow-down-2-bold';
import IconamoonProfile from '~icons/iconamoon/profile';
import IconamoonSettings from '~icons/iconamoon/settings';
import IconamoonHome from '~icons/iconamoon/home';
import IconamoonPlaylist from '~icons/iconamoon/playlist';
import IconamoonMusicAlbum from '~icons/iconamoon/music-album';
import IconamoonMusic2 from '~icons/iconamoon/music-2';
import IconamoonMusicArtist from '~icons/iconamoon/music-artist';
import IconamoonHeadphone from '~icons/iconamoon/headphone';
import IconamoonSignPlusCircleBold from '~icons/iconamoon/sign-plus-circle-bold';

export default {
  components: {
    IconamoonArrowUp2Bold,
    IconamoonArrowDown2Bold,
    IconamoonProfile,
    IconamoonSettings,
    IconamoonHome,
    IconamoonMusicAlbum,
    IconamoonMusic2,
    IconamoonMusicArtist,
    IconamoonPlaylist,
    IconamoonHeadphone,
    IconamoonSignPlusCircleBold
  },

  data() {
    return {
      ToggleBrowse: true,
      TogglePlaylists: false,
    }
  },

  methods: {
    ToggleMenu(value) {
      if (value == 'Browse') {
        this.ToggleBrowse = !this.ToggleBrowse;
      }
      else if (value == 'Playlists') {
        this.TogglePlaylists = !this.TogglePlaylists;
      }
    },
  },
}
</script>
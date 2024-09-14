<script lang="ts">
  import SidebarList from './SidebarList.svelte';
  import SidebarItem from './SidebarItem.svelte';
</script>

<div>
  <SidebarList>
    <SidebarItem href='/'>
      Home
    </SidebarItem>
    <SidebarItem href='/'>
      Search
    </SidebarItem>
    <SidebarItem href='/'>
      My Mix
    </SidebarItem>
  </SidebarList>

  <SidebarList name='Library'>
    <SidebarItem href='/albums' icon='iconoir:compact-disc'>
      Albums
    </SidebarItem>
    <SidebarItem href='/artists' icon='iconoir:microphone'>
      Artists
    </SidebarItem>
    <SidebarItem href='/tracks' icon='iconoir:music-double-note'>
      Tracks
    </SidebarItem>
  </SidebarList>

  <SidebarList name='Playlists'>
    <SidebarItem href='' icon='iconoir:plus'>
      Create Playlist
    </SidebarItem>
  </SidebarList>
</div>

<style>
  div {
    z-index: 0;
    width: 240px;
    flex-shrink: 0;
    min-height: 100dvh;
    padding: 24px 21px;
    background-color: var(--dark-sidebar);
    border-right: 1px solid var(--dark-border);
  }
</style>
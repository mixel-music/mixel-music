<script lang="ts">
  import SidebarList from './SidebarList.svelte';
  import SidebarItem from './SidebarItem.svelte';
  import { _ } from 'svelte-i18n'
</script>

<div>
  <SidebarList>
    <SidebarItem href='/'>
      {$_('sidebar.home')}
    </SidebarItem>
    <SidebarItem href='/'>
      {$_('sidebar.search')}
    </SidebarItem>
    <SidebarItem href='/'>
      {$_('sidebar.my_mix')}
    </SidebarItem>
  </SidebarList>

  <SidebarList name={$_('sidebar.library')}>
    <SidebarItem href='/albums' icon='iconoir:compact-disc'>
      {$_('sidebar.library.albums')}
    </SidebarItem>
    <SidebarItem href='/artists' icon='iconoir:microphone'>
      {$_('sidebar.library.artists')}
    </SidebarItem>
    <SidebarItem href='/tracks' icon='iconoir:music-double-note'>
      {$_('sidebar.library.tracks')}
    </SidebarItem>
  </SidebarList>

  <SidebarList name={$_('sidebar.playlists')}>
    <SidebarItem href='' icon='iconoir:plus'>
      {$_('sidebar.playlists.create')}
    </SidebarItem>
  </SidebarList>
</div>

<style>
  div {
    font-size: 16px !important;
    z-index: 0;
    width: 240px;
    flex-shrink: 0;
    min-height: 100dvh;
    padding: 24px 21px;
    background-color: var(--dark-sidebar);
    border-right: 1px solid var(--dark-border);
  }
</style>
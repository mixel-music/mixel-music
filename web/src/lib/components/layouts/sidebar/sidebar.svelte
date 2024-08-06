<script lang="ts">
  import SidebarSection from '$lib/components/layouts/sidebar/sidebar-section.svelte';
  import SidebarItem from '$lib/components/layouts/sidebar/sidebar-item.svelte';
</script>

<div>
  <SidebarSection>
    <SidebarItem href='/' title='Home' />
    <SidebarItem href='/' title='Search' />
    <SidebarItem href='/' title='My Mix' />
  </SidebarSection>

  <SidebarSection title='Library'>
    <SidebarItem
      href='/albums'
      title='Albums'
      icon='iconoir:compact-disc'
    />
    <SidebarItem
      href='/artists'
      title='Artists'
      icon='iconoir:microphone'
    />
    <SidebarItem
      href='/tracks'
      title='Tracks'
      icon='iconoir:music-double-note'
    />
  </SidebarSection>

  <SidebarSection title='Playlists'>
    <SidebarItem
      href=''
      title='Create Playlist'
      icon='iconoir:plus'
    />
  </SidebarSection>
</div>

<style>
  div {
    position: fixed;
    width: 250px;
    height: 100%;
    top: 0;
    left: 0;
    z-index: 0;
    padding: 24px 21px;
    background-color: var(--color-dark-bg-2);
    border-right: 1px solid var(--color-dark-border);
  }
</style>
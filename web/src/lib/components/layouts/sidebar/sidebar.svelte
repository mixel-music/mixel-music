<script lang="ts">
  import SidebarSection from '$lib/components/layouts/sidebar/sidebar-section.svelte';
  import SidebarItem from '$lib/components/layouts/sidebar/sidebar-item.svelte';
</script>

<div>
  <SidebarSection>
      <SidebarItem link="/" title="Home" />
      <SidebarItem link="/" title="Search" />
      <SidebarItem link="/" title="My Mix" />
  </SidebarSection>

  <SidebarSection title="Library">
    <SidebarItem
      link="/albums"
      title="Albums"
      icon="iconoir:compact-disc"
    />
    <SidebarItem
      link="/artists"
      title="Artists"
      icon="iconoir:microphone"
      />
    <SidebarItem
      link="/tracks"
      title="Tracks"
      icon="iconoir:music-double-note"
    />
  </SidebarSection>
  
  <SidebarSection title="PlayLists">
    <SidebarItem
      link=""
      title="Create Playlist"
      icon="iconoir:plus"
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
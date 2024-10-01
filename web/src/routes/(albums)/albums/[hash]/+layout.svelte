<script lang="ts">
  import Navbar from "$lib/components/layouts/navbar/Navbar.svelte";
  import AlbumWrap from "$lib/components/AlbumWrap.svelte";
  import { page } from "$app/stores";

  const currentPathname = $page.url.pathname.slice(-32);
</script>

<AlbumWrap artworkSrc={currentPathname} />

<div id="contents">
  <Navbar />
  <slot />
</div>

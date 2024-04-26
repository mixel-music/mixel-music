<script lang="ts">
	import './style.css';
	import Sidebar from '$lib/components/layouts/sidebar/sidebar.svelte';
	import Navbar from '$lib/components/layouts/navbar/navbar.svelte';
	import Player from '$lib/components/layouts/player/player.svelte';
</script>

<div id="app">
	<Sidebar />

	<section>
		<Navbar />
		<slot />
	</section>

	<Player />
</div>

<style>
	#app {
		width: 100%;
		display: flex;
		min-height: 100dvh;
		flex-direction: column;
		box-sizing: border-box;
	}

	section {
  	max-width: 100%;
  	padding: 64px;
		padding-top: 0;
		margin-left: 250px;
    margin-bottom: 96px;
	}
</style>

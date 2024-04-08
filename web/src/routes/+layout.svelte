<script lang="ts">
	import './style.css';
	import Sidebar from '$lib/components/Sidebar.svelte';
	import Navbar from '$lib/components/Navbar.svelte';
	import Player from '$lib/components/Player.svelte';
</script>

<div id="app">
	<Sidebar />
	<section class="content">
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

	.content {
  	max-width: 100%;
  	padding: 64px;
		padding-top: 0;
		margin-left: 250px;
    margin-bottom: 96px;
	}
</style>

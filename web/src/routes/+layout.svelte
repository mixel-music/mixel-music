<script lang="ts">
	import './style.css';
	import Navbar from '$lib/components/Navbar.svelte';
	import Player from '$lib/components/Player.svelte';
	
</script>

<div id="app">
	<Navbar />
	<section class="content">
		<slot />
	</section>
	<Player />
</div>

<style>
	#app {
		display: flex;
		flex-direction: column;
		width: 100%;
		min-height: 100dvh;
	}

	.content {
  	width: -webkit-fill-available;
  	padding: 0 18%;
  	margin-bottom: 180px;
	}
</style>

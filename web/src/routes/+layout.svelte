<script>
	import './style.css';
</script>

<div id="app">
	<section class="content">
		<slot />
	</section>
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
  	padding: 0 19%;
  	margin-bottom: 180px;
	}
</style>

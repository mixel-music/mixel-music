<script lang="ts">
  import type { PageData } from './$types';

  import CoverBorder from '$lib/components/albums/cover-border.svelte';
  import ContentHead from '$lib/components/elements/content-head.svelte';
  import ContentBody from '$lib/components/elements/content-body.svelte';
  import PageHead from '$lib/components/elements/page-head.svelte';

  export let data: PageData;
</script>

<CoverBorder
  src={ `http://localhost:2843/api/images/${ data.albumItem.imagehash }?size=500` }
  alt={ data.title }
  width=256
  height=256
/>

<PageHead title={ data.title } inline />

<ContentBody body={ data.albumItem.albumartist } />
<ContentBody body={ ` ${ data.albumItem.tracktotals } Tracks` } />

<style>

</style>
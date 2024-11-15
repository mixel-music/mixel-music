<script lang="ts">
  import { getArtwork } from '$lib/tools';
  import { encode, decode } from 'blurhash';
  import { writable } from "svelte/store";
  import { onMount } from "svelte";

  export let albumId: string;
  export let blurhashBackground = writable<string | null>(null);

  let imageUrl = getArtwork(albumId, 500);

  async function generateBlurhash(image: HTMLImageElement) {
    const width = 32;
    const height = 32;

    const canvas = document.createElement('canvas');
    canvas.width = width;
    canvas.height = height;

    const ctx = canvas.getContext('2d');
    ctx?.drawImage(image, 0, 0, width, height);
    const imageData = ctx?.getImageData(0, 0, width, height);

    if (imageData) {
      const blurhash = encode(imageData.data, imageData.width, imageData.height, 4, 4);
      const pixels = decode(blurhash, width, height);
      const decodedCanvas = document.createElement('canvas');

      decodedCanvas.width = width;
      decodedCanvas.height = height;

      const decodedCtx = decodedCanvas.getContext('2d');

      if (decodedCtx) {
        const decodedImageData = decodedCtx.createImageData(width, height);
        decodedImageData.data.set(pixels);
        decodedCtx.putImageData(decodedImageData, 0, 0);

        const dataUrl = decodedCanvas.toDataURL();
        blurhashBackground.set(dataUrl);
      }
    }
  }

  onMount(async () => {
    try {
      const img = new Image();
      img.crossOrigin = "use-credentials";
      img.src = imageUrl;
      img.onload = () => {
        generateBlurhash(img);
      };
    } catch (error) {
      console.error('Error generating Blurhash:', error);
    }
  });
</script>

<div
  class="album-wrap"
  style="background-image: url({$blurhashBackground})"
/>

<style>
  .album-wrap {
    position: absolute;
    width: 100%;
    height: 45dvh;
    z-index: -1;
    background-size: cover;
    background-position-y: center;
    border-image: fill 0 linear-gradient(
      to top,
      hsl(0, 0%, 7%) 0%,
      hsla(0, 0%, 7.13%, 0.997) 8.6%,
      hsla(0, 0%, 7.49%, 0.99) 17.5%,
      hsla(0, 0%, 8.02%, 0.979) 26.5%,    
      hsla(0, 0%, 8.65%, 0.965) 35.6%,   
      hsla(0, 0%, 9.33%, 0.948) 44.6%,  
      hsla(0, 0%, 10.04%, 0.93) 53.3%,   
      hsla(0, 0%, 10.73%, 0.91) 61.7%,    
      hsla(0, 0%, 11.39%, 0.89) 69.6%,     
      hsla(0, 0%, 12.01%, 0.87) 76.9%,  
      hsla(0, 0%, 12.57%, 0.852) 83.4%, 
      hsla(0, 0%, 13.05%, 0.835) 89%,   
      hsla(0, 0%, 13.44%, 0.821) 93.6%, 
      hsla(0, 0%, 13.74%, 0.81) 97.1%, 
      hsla(0, 0%, 13.93%, 0.803) 99.2%, 
      hsla(0, 0%, 14%, 0.8) 100%
    );
  }
</style>

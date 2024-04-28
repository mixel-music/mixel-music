<script lang="ts">
  export let width: string;
  export let value: number | string = 0;
  export let unique: string = 'slider';
</script>

<div
  on:click
  on:mousedown
  role='slider'
  class='slider-ctl {unique}'
  style:width={width}
>
  <div
    style:width={value}%
    class="slider-ctl__now"
  />
</div>

<style>
  .slider-ctl {
      background-color: var(--color-dark-trk-len);
      border-radius: calc(var(--app-radius) * 2);
      background-clip: content-box;
      cursor: pointer;
      padding: 8px;

    & .slider-ctl__now {
      justify-content: left;
      width: 0;
      height: 3px;
      background-color: var(--color-dark-trk-now);
      border-radius: var(--app-radius);
    }
  }

  .slider-ctl:focus {
    outline: none;
  }
</style>
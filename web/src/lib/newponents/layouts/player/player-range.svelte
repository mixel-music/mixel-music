<script lang="ts">
  export let max: number;
  export let width: string;
  export let value: number;
  export let name: string = 'range';

  import { stateStore } from "$lib/stores/state-store";

  let rangeElement: HTMLDivElement | null = null;

  function handleSeek(event: MouseEvent): void {
    event.preventDefault();
    
    if (rangeElement) {
      const ctlWidth = rangeElement.clientWidth;
      const ctlBound = rangeElement.getBoundingClientRect();
      const newValue = Math.max(0, Math.min(event.clientX - ctlBound.left, ctlWidth));

      value = (newValue / ctlWidth);
    }
  }

  function handleDrag(event: MouseEvent): void {
    event.preventDefault();
    stateStore.update(state => ({
      ...state,
      isSeeking: true,
    }));

    const moveHandler = (event: MouseEvent) => {
      handleSeek(event);
    };

    const postHandler = () => {
      document.removeEventListener("mousemove", moveHandler);
      document.removeEventListener("mouseup", postHandler);

      stateStore.update(state => ({
        ...state,
        currentTime: value * max,
        isSeeking: false,
      }));
    };

    document.addEventListener("mousemove", moveHandler);
    document.addEventListener("mouseup", postHandler);
    moveHandler(event);
  }

  function handleKeydown(event: KeyboardEvent): void {
    const step = 5;

    if (event.key === 'ArrowLeft' || event.key === 'ArrowDown') {
      value = Math.max(0, value - step);
    }
    else if (event.key === 'ArrowRight' || event.key === 'ArrowUp') {
      value = Math.min(100, value + step);
    }
  }
</script>

<div
  bind:this={rangeElement}
  on:click={event => handleSeek(event)}
  on:keydown={handleKeydown}
  on:mousedown={handleDrag}
  tabindex="0"
  role="slider"
  aria-valuemin="0"
  aria-valuemax="100"
  aria-valuenow={value}
  class={`range-ctl ${name}`}
  style:width={width}
>
  <div
    style:width={ $stateStore.isSeeking ? `${value * 100}%` : `${value / max * 100}%`}
    class="range-ctl__now"
  />
</div>

<style>
  .range-ctl {
    background-color: var(--color-dark-trk-len);
    border-radius: calc(var(--app-radius) * 2);
    background-clip: content-box;
    cursor: pointer;
    padding: 8px;
  }

  .range-ctl__now {
    width: 0;
    height: 3px;
    justify-content: left;
    background-color: var(--color-dark-trk-now);
    border-radius: var(--app-radius);
  }
</style>
<script lang="ts">
  import Button from "./Button.svelte";
  import { onMount, onDestroy } from "svelte";
  import { fade } from "svelte/transition";
  import { cubicOut } from "svelte/easing";

  let isDropdownOpen = false;
  export let dropdownWidth: string = '0px';
  export let dropdownOpenIcon: string | undefined = undefined;
  export let dropdownCloseIcon: string | undefined = undefined;

  let dropdownElement;

  if (dropdownCloseIcon === undefined && dropdownOpenIcon) {
    dropdownCloseIcon = dropdownOpenIcon;
  }

  const handleDropdownClick = () => {
    isDropdownOpen = !isDropdownOpen;
  };

  const handleClickOutside = (event) => {
    if (dropdownElement && !dropdownElement.contains(event.target)) {
      isDropdownOpen = false;
    }
  };

  onMount(() => {
    document.addEventListener("click", handleClickOutside);
  });

  onDestroy(() => {
    document.removeEventListener("click", handleClickOutside);
  });
</script>

<div bind:this={dropdownElement} class="dropdown">
  <Button
    button="round"
    iconName={isDropdownOpen ? dropdownCloseIcon : dropdownOpenIcon}
    on:click={handleDropdownClick}
  />
  {#if isDropdownOpen}
    <div
      class="dropdown-content"
      style:width={dropdownWidth}
      in:fade={{ duration: 100 }}
      out:fade={{ duration: 100 }}
    >
      <slot /> 
    </div>
  {/if}
</div>

<style>
  .dropdown-content {
    padding: 12px 0;
    background-color: var(--black-2a);
    box-shadow: 0 0 0 1px var(--dark-border) inset;
    backdrop-filter: blur(64px);
    border-radius: var(--radius-m);
    top: calc(var(--space-xl) + var(--space-s));
    position: absolute;
    right: 0;
  }
</style>

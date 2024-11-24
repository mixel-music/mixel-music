<script lang="ts">
  import Button from "./Button.svelte";
  import { onMount, onDestroy } from "svelte";
  import { fade } from "svelte/transition";

  let isDropdownOpen = false;
  export let dropdownStyle: string = 'round';
  export let dropdownWidth: string = '';
  export let dropdownOpenIcon: string | undefined = undefined;
  export let dropdownCloseIcon: string | undefined = undefined;

  let dropdownElement;
  let buttonElement;
  let dropdownPosition = { top: 0, right: 0 };

  if (dropdownCloseIcon === undefined && dropdownOpenIcon) {
    dropdownCloseIcon = dropdownOpenIcon;
  }

  const handleDropdownClick = () => {
    isDropdownOpen = !isDropdownOpen;

    if (isDropdownOpen && buttonElement) {
      const rect = buttonElement.getBoundingClientRect();

      dropdownPosition = {
        top: rect.bottom + window.scrollY,
        right: window.scrollX,
      };
    }
  };

  const handleClickOutside = (event) => {
    if (dropdownElement && !dropdownElement.contains(event.target) && !buttonElement.contains(event.target)) {
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

<div bind:this={buttonElement} class="dropdown">
  <Button
    button={dropdownStyle}
    iconName={isDropdownOpen ? dropdownCloseIcon : dropdownOpenIcon}
    on:click={handleDropdownClick}
  />
</div>

{#if isDropdownOpen}
  <div
    bind:this={dropdownElement}
    class="dropdown-content"
    style="
      position: fixed;
      width: {dropdownWidth};
      top: calc({dropdownPosition.top}px + var(--space-xs));
      right: calc({dropdownPosition.right}px + 80px);"
    in:fade={{ duration: 100 }}
    out:fade={{ duration: 100 }}
  >
    <slot />
  </div>
{/if}

<style>
  .dropdown {
    display: inline-block;
  }

  .dropdown-content {
    padding: 12px 0;
    background-color: var(--black-3a);
    box-shadow: 0 0 0 1px var(--dark-border) inset;
    backdrop-filter: blur(64px);
    border-radius: var(--radius-m);
    z-index: 1000;
  }
</style>

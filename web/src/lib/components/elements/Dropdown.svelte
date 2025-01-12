<script lang="ts">
  import Button from "./Button.svelte";
  import { onMount, onDestroy, tick } from "svelte";
  import { fade } from "svelte/transition";

  let isDropdownOpen = false;
  export let dropdownStyle: string = 'round';
  export let dropdownWidth: string = '';
  export let dropdownOpenIcon: string | undefined = undefined;
  export let dropdownCloseIcon: string | undefined = undefined;

  let dropdownElement: HTMLElement | null = null;
  let buttonElement: HTMLElement | null = null;
  let dropdownPosition = { top: 0, left: 0 };
  let wrapElement: HTMLElement | null = null;

  if (dropdownCloseIcon === undefined && dropdownOpenIcon) {
    dropdownCloseIcon = dropdownOpenIcon;
  }

  const calculateDropdownPosition = async () => {
    await tick(); // DOM 업데이트 후 실행 보장

    if (!buttonElement || !dropdownElement) return;

    // 버튼과 드롭다운의 위치 정보
    const buttonRect = buttonElement.getBoundingClientRect();
    const dropdownRect = dropdownElement.getBoundingClientRect();

    // 화면 스크롤 보정
    const scrollX = window.scrollX;
    const scrollY = window.scrollY;

    // 초기 위치 (버튼 아래 왼쪽)
    let top = buttonRect.bottom + scrollY + 12;
    let left = buttonRect.left + scrollX;

    // 아래쪽 공간 부족 시 위로 이동
    if (top + dropdownRect.height > scrollY + window.innerHeight) {
      // top = dropdownElement.offsetTop + dropdownElement.scrollHeight;
      top = buttonRect.top + scrollY - dropdownRect.height - 12;
    }

    // 오른쪽 공간 부족 시 왼쪽으로 이동
    if (left + dropdownRect.width > scrollX + window.innerWidth) {
      left = buttonElement.offsetLeft - dropdownElement.offsetWidth + buttonRect.width;
    }

    // 최종 위치 설정
    dropdownPosition = { 
      top: Math.max(0, top), 
      left: Math.max(0, left) 
    };
  };

  const handleDropdownClick = () => {
    isDropdownOpen = !isDropdownOpen;

    if (isDropdownOpen) {
      calculateDropdownPosition(); // 드롭다운 열릴 때 위치 계산

      if (wrapElement) {
        wrapElement.style.overflow = 'hidden';
      }
    }
    else {
      if (wrapElement) {
        wrapElement.style.overflow = '';
      }
    }
  };

  const handleClickOutside = (event: MouseEvent) => {
    if (
      dropdownElement && !dropdownElement.contains(event.target as Node) &&
      buttonElement && !buttonElement.contains(event.target as Node)
    ) {
      if (wrapElement) {
        wrapElement.style.overflow = '';
      }
      isDropdownOpen = false;
    }
  };

  onMount(() => {
    wrapElement = document.getElementById("wrap");
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
    aria-expanded={isDropdownOpen}
    aria-controls="dropdown-menu"
  />
</div>

{#if isDropdownOpen}
  <div
    bind:this={dropdownElement}
    id="dropdown-menu"
    class="dropdown-content"
    style="
      position: absolute;
      top: {dropdownPosition.top}px;
      left: {dropdownPosition.left}px;
      width: {dropdownWidth || 'max-content'};
    "
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
    background-color: var(--black-3);
    box-shadow: 0 0 0 1px var(--dark-border) inset;
    border-radius: var(--radius-m);
    z-index: 1000;
    overflow: hidden;
    padding: 12px 0;
  }
</style>

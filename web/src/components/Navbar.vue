<template>
  <nav class="navbar">
    <div class="navbar-left">
      <button class="navbar-button navbar-previous" @click="$router.back()">
        <IconamoonArrowLeft2 class="navbar-icon" />
      </button>
      <button class="navbar-button navbar-next" @click="$router.go(1)">
        <IconamoonArrowRight2 class="navbar-icon" />
      </button>
    </div>
    <div class="navbar-center">
      
    </div>
    <div class="navbar-right">
      <input type="text" placeholder="Search">
    </div>
  </nav>
</template>

<script>
import IconamoonArrowLeft2 from '~icons/iconamoon/arrow-left-2';
import IconamoonArrowRight2 from '~icons/iconamoon/arrow-right-2';

export default {
  components: {
    IconamoonArrowLeft2,
    IconamoonArrowRight2,
  },
}
</script>

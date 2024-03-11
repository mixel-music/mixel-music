<template>
  <nav class="navbar">
    <div class="navbar-left">
      <span class="navbar-link" @click="$router.back()">
        <IconamoonArrowLeft2 class="navbar-icon" />
      </span>
      <span class="navbar-link" @click="$router.forward()">
        <IconamoonArrowRight2 class="navbar-icon" />
      </span>
      <span class="navbar-link">
        <router-link to="/albums">Albums</router-link>
      </span>
      <span class="navbar-link">
        <router-link to="/tracks">Tracks</router-link>
      </span>
      <span class="navbar-link">
        <router-link to="/artists">Artists</router-link>
      </span>
    </div>
    <div class="navbar-center">
      
    </div>
    <div class="navbar-right">
      <input type="text" id="navbar-input" name="Search" placeholder="Search">
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

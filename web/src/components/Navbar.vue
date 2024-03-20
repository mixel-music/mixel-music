<template>
  <nav class="navbar">
    <div class="navbar-left">
      <span class="navbar-link" id="navbar-logo">
        <router-link to="/">
          <img src="/src/assets/logo.svg" width="42.8px">
        </router-link>
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
      <span class="navbar-link navbar-explore" @click="$router.back()">
        <IconamoonArrowLeft2 class="navbar-icon" />
      </span>
      <span class="navbar-link navbar-explore" @click="$router.forward()">
        <IconamoonArrowRight2 class="navbar-icon" />
      </span>
    </div>
    <!-- <div class="navbar-right">
      <span class="navbar-link navbar-explore" @click="$router.back()">
        <IconamoonArrowLeft2 class="navbar-icon" />
      </span>
      <span class="navbar-link navbar-explore" @click="$router.forward()">
        <IconamoonArrowRight2 class="navbar-icon" />
      </span>
      <span class="navbar-link">
        <IconamoonProfileCircle class="navbar-user" />
      </span>
    </div> -->
  </nav>
</template>

<script>
import IconamoonArrowLeft2 from '~icons/iconamoon/arrow-left-2';
import IconamoonArrowRight2 from '~icons/iconamoon/arrow-right-2';
import IconamoonProfileCircle from '~icons/iconamoon/profile-circle';

export default {
  components: {
    IconamoonArrowLeft2,
    IconamoonArrowRight2,
    IconamoonProfileCircle,
  },
}
</script>

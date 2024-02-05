import { createRouter, createWebHistory } from 'vue-router'
import songs from '../views/songs.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'songs',
      component: songs
    },
    {
      path: '/album',
      name: 'album',
      component: () => import('../views/album.vue')
    }
  ]
})

export default router
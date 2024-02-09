import { createRouter, createWebHistory } from 'vue-router'
import music from '../views/music.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'music',
      component: music,
    },

    {
      path: '/album',
      name: 'album',
      component: () => import('../views/album.vue'),
    }
  ]
})

export default router
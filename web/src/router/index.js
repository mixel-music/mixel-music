import { createRouter, createWebHistory } from 'vue-router'
import Tracks from '../views/Tracks.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/tracks', 
    },

    {
      path: '/tracks',
      name: 'Tracks',
      component: Tracks,
    },

    {
      path: '/albums',
      name: 'Albums',
      component: () => import('../views/Albums.vue'),
    },

    {
      path: '/artists',
      name: 'Artists',
      component: () => import('../views/Artists.vue'),
    },
  ]
})

export default router
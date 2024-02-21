import { createRouter, createWebHistory } from 'vue-router'
import Tracks from '../views/Tracks.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Main',
      component: Tracks,  
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
  ]
})

export default router
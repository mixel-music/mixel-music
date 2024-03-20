import { createRouter, createWebHistory } from 'vue-router'
import Tracks from '../views/Tracks.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      redirect: '/albums', 
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
      path: '/albums/:hash',
      name: 'Album',
      component: () => import('../views/Album.vue'),
    },

    {
      path: '/artists',
      name: 'Artists',
      component: () => import('../views/Artists.vue'),
    },

    {
      path: '/:pathMatch(.*)*',
      redirect: '/',
    },
  ]
})

export default router
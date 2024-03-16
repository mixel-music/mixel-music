import { createRouter, createWebHistory } from 'vue-router'
import Tracks from '../views/Tracks.vue'

const router = createRouter({
  history: createWebHistory(),
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
      path: '/tracks/:hash',
      name: 'Track',
      component: Tracks,
    },

    {
      path: '/albums',
      name: 'Albums',
      component: () => import('../views/Albums.vue'),
    },

    {
      path: '/albums/:albumhash',
      name: 'Album',
      component: () => import ('../views/Album.vue'),
    },

    {
      path: '/artists',
      name: 'Artists',
      component: () => import('../views/Artists.vue'),
    },

    {
      path: '/artists/:artisthash',
      name: 'Artist',
      component: () => import('../views/Artists.vue'),
    },
  ]
})

export default router
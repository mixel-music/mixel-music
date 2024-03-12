import { createApp } from 'vue'
import App from './App.vue'
import './assets/style.css'
import './assets/logo.svg'
import router from './router/index.js'
import VueLazyload from 'vue-lazyload'

createApp(App).use(router).use(VueLazyload).mount('#app')
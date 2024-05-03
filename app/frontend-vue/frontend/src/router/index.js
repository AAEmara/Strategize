import { createRouter, createWebHistory } from 'vue-router'
import GeneralStrategy from '../components/GeneralStrategy.vue'
import PerspectiveCard from '../components/PerspectiveCard.vue'

const routes = [
  {
    path: '/general_strategy',
    name: 'GeneralStrategy',
    component: GeneralStrategy
  },
  {
    path: '/perspective',
    name: 'PerspectiveCard',
    component: PerspectiveCard
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

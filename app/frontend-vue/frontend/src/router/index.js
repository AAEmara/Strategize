import { createRouter, createWebHistory } from 'vue-router'
import GeneralStrategy from '../components/GeneralStrategy.vue'
import PerspectiveCard from '../components/PerspectiveCard.vue'
import Objectives from '../components/StrategyObjectives.vue'

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
  },
  {
    path: '/objectives',
    name: 'Objectives',
    component: Objectives
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router

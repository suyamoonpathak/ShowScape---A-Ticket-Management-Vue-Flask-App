import { createRouter, createWebHistory } from 'vue-router'
import TestComponent from '../components/common/TestComponent'
import SignUp from '../components/pages/SignUp'
import HomePage from '../components/pages/HomePage'

const routes = [
  {
    path: '/test',
    name:'Test',
    component: TestComponent
  },
  {
    path: '/signup',
    component: SignUp
  },
  {
    path: '/',
    component: SignUp
  },
  {
    path: '/home',
    component: HomePage
  }
]
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})
export default router
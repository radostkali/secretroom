import Vue from 'vue'
import Router from 'vue-router'

const routerOptions = [
  {
    path: '/',
    component: 'Main',
    name: 'main'
  },
  {
    path: '/:roomId',
    component: 'Room',
    name: 'room'
  },
  { path: '*',
    component: 'NotFound',
    name: 'notFound'
  }
]

const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})

Vue.use(Router)

const router = new Router({
  routes,
  mode: 'history'
})

export default router

import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/about',
      name: 'about',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue')
    },
    {
      path: '/bottom/tams',
      name: 'tams',
      component: () => import('../components/TAMTable.vue')
    },
    {
      path: '/bottom/tams_history',
      name: 'tams_histroy',
      component: () => import('../components/TAMHistory.vue')
    },
    {
      path: '/bottom/config',
      name: 'bottom_config',
      component: () => import('../components/ConfigTable.vue')
    },
    {
      path: '/main/trading',
      name: 'main_trading',
      component: () => import('../components/TradingTable.vue')
    },
    {
      path: '/main/alltradeposinfo',
      name: 'main_all_trade_pos_info',
      component: () => import('../components/TradePosInfo.vue')
    },
    {
      path: '/main/allclosedposinfo',
      name: 'main_all_close_pos_info',
      component: () => import('../components/ClosedPosInfo.vue')
    }
  ]
})

export default router

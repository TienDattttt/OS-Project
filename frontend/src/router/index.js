import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import ForecastView from '../views/ForecastView.vue'
import WeatherMapView from '../views/WeatherMapView.vue'
import LocationView from '../views/LocationView.vue'
import AlertsView from '../views/AlertsView.vue'
import ProfileView from '../views/ProfileView.vue'
import NewsView from '../views/NewsView.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/forecast',
      name: 'forecast',
      component: ForecastView
    },
    {
      path: '/map',
      name: 'map',
      component: WeatherMapView
    },
    {
      path: '/location',
      name: 'location',
      component: LocationView
    },
    {
      path: '/alerts',
      name: 'alerts',
      component: AlertsView
    },
    {
      path: '/profile',
      name: 'profile',
      component: ProfileView
    },
    {
      path: '/news',
      name: 'news',
      component: NewsView
    }
  ]
})

export default router
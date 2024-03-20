import { createRouter, createWebHistory } from 'vue-router';
import RegisterView from '../views/RegisterView.vue';
import LoginView from '../views/LoginView.vue';
import LobbyView from '../views/LobbyView.vue';
import OTPView from '@/views/OTPView.vue'
import LandingPage from '@/views/LandingPage.vue';
import MainDashboard from '@/views/MainDashboard.vue';
import ProfileView from '@/views/ProfileView.vue';

const routes = [
  {
    path: '/',
    name: 'LandingPage',
    component: LandingPage,
  },
  {
    path: '/Register',
    name: 'RegisterView',
    component: RegisterView,
  },
  {
    path: '/Login',
    name: 'LoginView',
    component: LoginView,
  },
  {
    path: '/Lobby',
    name: 'LobbyView',
    component: LobbyView,
  },
  {
    path: '/otp',
    name: 'OTPView',
    component: OTPView,
  },
  {
    path: '/dashboard',
    name: 'MainDashboard',
    component: MainDashboard,
  },
  {
    path: '/profile',
    name: 'ProfileView',
    component: ProfileView,
  }
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;

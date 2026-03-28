// frontend/src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'

import LoginPage from '../pages/LoginPage.vue'
import RegisterPage from '../pages/RegisterPage.vue'
import DashboardPage from '../pages/DashboardPage.vue'
import SimuladosPage from '../pages/SimuladosPage.vue'
import ProvaPage from '../pages/ProvaPage.vue'
import ResultadoPage from '../pages/ResultadoPage.vue'
import RankingPage from '../pages/RankingPage.vue'
import AdminAlunosPage from '../pages/AdminAlunosPage.vue'
import AdminAlunoDashboardPage from '../pages/AdminAlunoDashboardPage.vue'

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login', name: 'login', component: LoginPage, meta: { guest: true } },
  { path: '/register', name: 'register', component: RegisterPage, meta: { guest: true } },
  { path: '/dashboard', name: 'dashboard', component: DashboardPage, meta: { requiresAuth: true } },
  { path: '/simulados', name: 'simulados', component: SimuladosPage, meta: { requiresAuth: true } },
  { path: '/simulado/:id', name: 'prova', component: ProvaPage, meta: { requiresAuth: true } },
  { path: '/resultado/:id', name: 'resultado', component: ResultadoPage, meta: { requiresAuth: true } },
  { path: '/ranking', name: 'ranking', component: RankingPage, meta: { requiresAuth: true } },

  // Rotas do professor — requiresAdmin bloqueia alunos no guard
  {
    path: '/admin/alunos',
    name: 'admin-alunos',
    component: AdminAlunosPage,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
  {
    path: '/admin/alunos/:id',
    name: 'admin-aluno-dashboard',
    component: AdminAlunoDashboardPage,
    meta: { requiresAuth: true, requiresAdmin: true }
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const role = localStorage.getItem('user_role') // salvo no login

  if (to.meta.requiresAuth && !token) {
    next({ name: 'login' })
  } else if (to.meta.guest && token) {
    next({ name: 'dashboard' })
  } else if (to.meta.requiresAdmin && role !== 'admin') {
    // Aluno tentando acessar rota de professor — redireciona para dashboard
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router
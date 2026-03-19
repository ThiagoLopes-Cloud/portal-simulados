// Importa as funções necessárias do Vue Router
import { createRouter, createWebHistory } from 'vue-router'

// Importa as páginas que vamos criar
// Cada import corresponde a uma página do sistema
import LoginPage from '../pages/LoginPage.vue'
import RegisterPage from '../pages/RegisterPage.vue'
import DashboardPage from '../pages/DashboardPage.vue'
import SimuladosPage from '../pages/SimuladosPage.vue'
import ProvaPage from '../pages/ProvaPage.vue'
import ResultadoPage from '../pages/ResultadoPage.vue'
import RankingPage from '../pages/RankingPage.vue'

// Define as rotas do sistema
// Cada objeto é uma rota com path (URL) e component (página)
const routes = [
  {
    // Rota raiz — redireciona para o dashboard
    path: '/',
    redirect: '/dashboard'
  },
  {
    // Página de login — não requer autenticação
    path: '/login',
    name: 'login',
    component: LoginPage,
    // meta.guest — indica que é uma rota pública
    meta: { guest: true }
  },
  {
    // Página de registro — não requer autenticação
    path: '/register',
    name: 'register',
    component: RegisterPage,
    meta: { guest: true }
  },
  {
    // Dashboard — requer autenticação
    path: '/dashboard',
    name: 'dashboard',
    component: DashboardPage,
    // meta.requiresAuth — indica que precisa de token JWT
    meta: { requiresAuth: true }
  },
  {
    // Lista de simulados — requer autenticação
    path: '/simulados',
    name: 'simulados',
    component: SimuladosPage,
    meta: { requiresAuth: true }
  },
  {
    // Tela de prova — recebe o ID do simulado na URL
    // ex: /simulado/1 → abre o simulado de ID 1
    path: '/simulado/:id',
    name: 'prova',
    component: ProvaPage,
    meta: { requiresAuth: true }
  },
  {
    // Tela de resultado — recebe o ID do resultado na URL
    path: '/resultado/:id',
    name: 'resultado',
    component: ResultadoPage,
    meta: { requiresAuth: true }
  },
  {
    // Ranking de alunos — requer autenticação
    path: '/ranking',
    name: 'ranking',
    component: RankingPage,
    meta: { requiresAuth: true }
  },
]

// Cria o router com histórico de navegação
// createWebHistory — usa URLs limpas sem # (ex: /dashboard em vez de /#/dashboard)
const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation Guard — executado antes de cada navegação
// Verifica se o usuário tem permissão para acessar a rota
router.beforeEach((to, from, next) => {

  // Verifica se existe um token no localStorage
  const token = localStorage.getItem('access_token')

  // Se a rota requer autenticação e não tem token
  // Redireciona para o login
  if (to.meta.requiresAuth && !token) {
    next({ name: 'login' })

  // Se a rota é pública e o usuário já está logado
  // Redireciona para o dashboard
  } else if (to.meta.guest && token) {
    next({ name: 'dashboard' })

  // Caso contrário, permite a navegação normalmente
  } else {
    next()
  }
})

// Exporta o router para ser usado no main.js
export default router
import { createRouter, createWebHistory } from 'vue-router'

// Eager: auth pages (carregamento imediato, UX crítica)
import LoginPage    from '../pages/LoginPage.vue'
import RegisterPage from '../pages/RegisterPage.vue'

// Lazy: demais páginas (carregadas sob demanda)
const DashboardPage           = () => import('../pages/DashboardPage.vue')
const SimuladosPage           = () => import('../pages/SimuladosPage.vue')
const ProvaPage               = () => import('../pages/ProvaPage.vue')
const ResultadoPage           = () => import('../pages/ResultadoPage.vue')
const RankingPage             = () => import('../pages/RankingPage.vue')
const TurmaPortal             = () => import('../pages/TurmaPortal.vue')
const TrilhasPage             = () => import('../pages/TrilhasPage.vue')
const TurmaDashboardPage      = () => import('../pages/TurmaDashboardPage.vue')
const AdminAlunosPage         = () => import('../pages/AdminAlunosPage.vue')
const AdminAlunoDashboardPage = () => import('../pages/AdminAlunoDashboardPage.vue')
const ImportarQuestoesPage    = () => import('../pages/ImportarQuestoesPage.vue')
const NotFoundPage            = () => import('../pages/NotFoundPage.vue')

const routes = [
  { path: '/', redirect: '/dashboard' },
  { path: '/login',    name: 'login',    component: LoginPage,    meta: { guest: true,  transition: 'fade' } },
  { path: '/register', name: 'register', component: RegisterPage, meta: { guest: true,  transition: 'fade' } },

  { path: '/dashboard',     name: 'dashboard', component: DashboardPage, meta: { requiresAuth: true } },
  { path: '/simulados',     name: 'simulados', component: SimuladosPage, meta: { requiresAuth: true } },
  { path: '/simulado/:id',  name: 'prova',     component: ProvaPage,     meta: { requiresAuth: true } },
  { path: '/resultado/:id', name: 'resultado', component: ResultadoPage, meta: { requiresAuth: true } },
  { path: '/ranking',       name: 'ranking',   component: RankingPage,   meta: { requiresAuth: true } },

  { path: '/turmas',          name: 'turmas',         component: TurmaPortal,       meta: { requiresAuth: true } },
  { path: '/trilhas',         name: 'trilhas',         component: TrilhasPage,       meta: { requiresAuth: true } },
  { path: '/turma-dashboard', name: 'turma-dashboard', component: TurmaDashboardPage, meta: { requiresAuth: true } },

  {
    path: '/admin/alunos',
    name: 'admin-alunos',
    component: AdminAlunosPage,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/alunos/:id',
    name: 'admin-aluno-dashboard',
    component: AdminAlunoDashboardPage,
    meta: { requiresAuth: true, requiresAdmin: true },
  },
  {
    path: '/admin/importar',
    name: 'importar',
    component: ImportarQuestoesPage,
    meta: { requiresAuth: true, requiresAdmin: true },
  },

  { path: '/:pathMatch(.*)*', name: 'not-found', component: NotFoundPage },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('access_token')
  const role  = localStorage.getItem('user_role')

  if (to.meta.requiresAuth && !token) {
    next({ name: 'login' })
  } else if (to.meta.guest && token) {
    next({ name: 'dashboard' })
  } else if (to.meta.requiresAdmin && role !== 'admin') {
    next({ name: 'dashboard' })
  } else {
    next()
  }
})

export default router

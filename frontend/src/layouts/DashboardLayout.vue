<template>
  <div class="sl-layout">
    <!-- Sidebar -->
    <SimuslabSidebar
      :collapsed="ui.sidebarCollapsed"
      :navigation="navigation"
      @toggle="ui.toggleSidebar()"
    />

    <!-- Topbar -->
    <SimuslabTopbar
      :username="username"
      :sidebar-width="sidebarWidth"
    >
      <template #right>
        <button class="sl-logout-btn" @click="logout" title="Sair" aria-label="Sair da plataforma">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
        </button>
      </template>
    </SimuslabTopbar>

    <!-- Main content -->
    <main class="sl-main" :style="mainStyle">
      <slot />
    </main>

    <!-- Mobile bottom nav -->
    <nav class="sl-mobile-nav" aria-label="Navegação principal">
      <router-link v-for="item in mobileNav" :key="item.to" :to="item.to" class="sl-mnav-item">
        <svg
          class="sl-mnav-icon"
          width="20"
          height="20"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.75"
          stroke-linecap="round"
          stroke-linejoin="round"
          v-html="item.svg"
        />
        <span class="sl-mnav-label">{{ item.label }}</span>
      </router-link>
    </nav>

    <!-- Toast notifications -->
    <SimuslabToast />
  </div>
</template>

<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUIStore } from '../stores/ui.store.js'
import { icons } from '../utils/icons.js'
import SimuslabSidebar from '../components/layout/SimuslabSidebar.vue'
import SimuslabTopbar  from '../components/layout/SimuslabTopbar.vue'
import SimuslabToast   from '../components/ui/SimuslabToast.vue'

const props = defineProps({
  username: { type: String, default: '' },
  isAdmin:  { type: Boolean, default: false },
})

const ui = useUIStore()
const router = useRouter()
const isMobile = ref(false)

function handleResize() { isMobile.value = window.innerWidth <= 768 }
onMounted(() => { handleResize(); window.addEventListener('resize', handleResize) })
onUnmounted(() => window.removeEventListener('resize', handleResize))

const sidebarWidth = computed(() =>
  ui.sidebarCollapsed ? 'var(--sidebar-width-collapsed)' : 'var(--sidebar-width)'
)

const mainStyle = computed(() => ({
  marginLeft: sidebarWidth.value,
  transition: `margin-left var(--transition-slow)`,
}))

const navigation = computed(() => {
  const groups = [
    {
      id: 'main',
      items: [
        { to: '/dashboard',       icon: 'dashboard',        label: 'Dashboard' },
        { to: '/simulados',       icon: 'simulados',        label: 'Avaliações' },
        { to: '/trilhas',         icon: 'trilhas',          label: 'Trilhas' },
        { to: '/turmas',          icon: 'turmas',           label: 'Minhas Turmas' },
        { to: '/turma-dashboard', icon: 'turma-dashboard',  label: 'Dashboard Turma' },
        { to: '/ranking',         icon: 'ranking',          label: 'Ranking' },
      ],
    },
  ]

  if (props.isAdmin) {
    groups.push({
      id: 'admin',
      label: 'Administração',
      items: [
        { to: '/admin/alunos',   icon: 'gestao-alunos', label: 'Gestão Alunos',    admin: true },
        { to: '/admin/importar', icon: 'importar',      label: 'Importar Questões', admin: true },
      ],
    })
  }

  return groups
})

const mobileNav = computed(() => [
  { to: '/dashboard',       svg: icons.dashboard,       label: 'Início' },
  { to: '/simulados',       svg: icons.simulados,       label: 'Avaliações' },
  { to: '/trilhas',         svg: icons.trilhas,         label: 'Trilhas' },
  { to: '/turma-dashboard', svg: icons['turma-dashboard'], label: 'Turma' },
  { to: '/ranking',         svg: icons.ranking,         label: 'Ranking' },
])

function logout() {
  localStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
.sl-layout {
  min-height: 100vh;
  background: #f8fafc;
  display: flex;
  flex-direction: column;
}

/* ── Main content ── */
.sl-main {
  flex: 1;
  padding: calc(var(--topbar-height) + var(--space-7)) var(--space-7) var(--space-7);
  min-height: 100vh;
  overflow-x: hidden;
}

/* ── Logout button ── */
.sl-logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  color: #94a3b8;
  background: transparent;
  border: 1px solid #e8ecf2;
  cursor: pointer;
  transition: all 0.12s ease;
}
.sl-logout-btn:hover {
  color: #dc2626;
  border-color: #fecaca;
  background: #fef2f2;
}

/* ── Mobile nav ── */
.sl-mobile-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.96);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-top: 1px solid #e8ecf2;
  z-index: var(--z-topbar);
  padding-bottom: env(safe-area-inset-bottom, 0);
}

.sl-mnav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  padding: 8px 4px 6px;
  color: #94a3b8;
  text-decoration: none;
  transition: color 0.12s ease;
}

.sl-mnav-item.router-link-exact-active {
  color: #2563eb;
}

.sl-mnav-icon { flex-shrink: 0; }

.sl-mnav-label {
  font-family: var(--font-body);
  font-size: 0.6rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* ── Responsive ── */
@media (max-width: 768px) {
  .sl-mobile-nav { display: flex; }
  .sl-main {
    margin-left: 0 !important;
    padding-bottom: calc(var(--space-16) + env(safe-area-inset-bottom, 0));
  }
}
</style>

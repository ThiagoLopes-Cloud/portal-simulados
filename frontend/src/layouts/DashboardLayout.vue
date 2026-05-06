<template>
  <div class="dashboard-layout">
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
        <button class="logout-btn" @click="logout" title="Sair">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
            <path d="M6 14H3a1 1 0 0 1-1-1V3a1 1 0 0 1 1-1h3M11 11l3-3-3-3M14 8H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </template>
    </SimuslabTopbar>

    <!-- Main content -->
    <main class="dashboard-main" :style="mainStyle">
      <slot />
    </main>

    <!-- Mobile bottom nav -->
    <nav class="mobile-nav" :class="{ 'mobile-nav--hidden': ui.sidebarCollapsed && !isMobile }">
      <router-link v-for="item in mobileNav" :key="item.to" :to="item.to" class="mnav-item">
        <span class="mnav-icon">{{ item.icon }}</span>
        <span class="mnav-label">{{ item.label }}</span>
      </router-link>
    </nav>

    <!-- Toast notifications -->
    <SimuslabToast />
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUIStore } from '../stores/ui.store.js'
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

onMounted(() => {
  isMobile.value = window.innerWidth <= 768
  window.addEventListener('resize', () => { isMobile.value = window.innerWidth <= 768 })
})

const sidebarWidth = computed(() =>
  ui.sidebarCollapsed
    ? 'var(--sidebar-width-collapsed)'
    : 'var(--sidebar-width)'
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
        { to: '/dashboard',       icon: '◈', label: 'Dashboard' },
        { to: '/simulados',       icon: '◎', label: 'Avaliações' },
        { to: '/trilhas',         icon: '▶', label: 'Trilhas' },
        { to: '/turmas',          icon: '◉', label: 'Minhas Turmas' },
        { to: '/turma-dashboard', icon: '⬟', label: 'Dashboard Turma' },
        { to: '/ranking',         icon: '◆', label: 'Ranking' },
      ],
    },
  ]

  if (props.isAdmin) {
    groups.push({
      id: 'admin',
      label: 'Administração',
      items: [
        { to: '/admin/alunos',   icon: '⬡', label: 'Gestão Alunos',    admin: true },
        { to: '/admin/importar', icon: '⬢', label: 'Importar Questões', admin: true },
      ],
    })
  }

  return groups
})

const mobileNav = computed(() => [
  { to: '/dashboard',       icon: '◈', label: 'Dashboard' },
  { to: '/simulados',       icon: '◎', label: 'Avaliações' },
  { to: '/trilhas',         icon: '▶', label: 'Trilhas' },
  { to: '/turma-dashboard', icon: '⬟', label: 'Batalha' },
  { to: '/ranking',         icon: '◆', label: 'Ranking' },
])

function logout() {
  localStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
.dashboard-layout {
  min-height: 100vh;
  background: #f8fafc;
  display: flex;
  flex-direction: column;
}

/* ── Main content ── */
.dashboard-main {
  flex: 1;
  padding: calc(var(--topbar-height) + var(--space-7)) var(--space-7) var(--space-7);
  min-height: 100vh;
  overflow-x: hidden;
}

/* ── Logout button ── */
.logout-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  color: #94a3b8;
  background: transparent;
  border: 1px solid #e2e8f0;
  cursor: pointer;
  transition: all 0.15s ease;
}
.logout-btn:hover {
  color: #dc2626;
  border-color: #fecaca;
  background: #fef2f2;
}

/* ── Mobile nav ── */
.mobile-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #ffffff;
  border-top: 1px solid #e2e8f0;
  z-index: var(--z-topbar);
  padding-bottom: env(safe-area-inset-bottom, 0);
}

.mnav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 8px 4px;
  color: #94a3b8;
  text-decoration: none;
  font-size: 0.6rem;
  font-family: var(--font-body);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 600;
  transition: color 0.15s ease;
}
.mnav-item.router-link-exact-active { color: #2563eb; }

.mnav-icon { font-size: 1.1rem; }
.mnav-label { font-size: var(--text-2xs); }

/* ── Responsive ── */
@media (max-width: 768px) {
  .mobile-nav { display: flex; }
  .dashboard-main {
    margin-left: 0 !important;
    padding-bottom: calc(var(--space-16) + env(safe-area-inset-bottom, 0));
  }
}

@media (min-width: 769px) and (max-width: 1024px) {
  /* Sidebar auto-collapses at medium screens — ui.store handles it */
}
</style>

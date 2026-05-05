<template>
  <div class="dashboard-layout">
    <!-- Sidebar -->
    <OrbynSidebar
      :collapsed="ui.sidebarCollapsed"
      :navigation="navigation"
      @toggle="ui.toggleSidebar()"
    />

    <!-- Topbar -->
    <OrbynTopbar
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
    </OrbynTopbar>

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
    <OrbynToast />
  </div>
</template>

<script setup>
import { computed, ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUIStore } from '../stores/ui.store.js'
import OrbynSidebar from '../components/layout/OrbynSidebar.vue'
import OrbynTopbar  from '../components/layout/OrbynTopbar.vue'
import OrbynToast   from '../components/ui/OrbynToast.vue'

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
        { to: '/dashboard', icon: '◈', label: 'Dashboard' },
        { to: '/simulados', icon: '◎', label: 'Avaliações' },
        { to: '/turmas',    icon: '◉', label: 'Minhas Turmas' },
        { to: '/ranking',   icon: '◆', label: 'Ranking' },
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
  { to: '/dashboard', icon: '◈', label: 'Dashboard' },
  { to: '/simulados', icon: '◎', label: 'Avaliações' },
  { to: '/turmas',    icon: '◉', label: 'Turmas' },
  { to: '/ranking',   icon: '◆', label: 'Ranking' },
])

function logout() {
  localStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
.dashboard-layout {
  min-height: 100vh;
  background: var(--color-cosmos);
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
  border-radius: var(--radius-md);
  color: var(--color-comet);
  background: transparent;
  border: 1px solid var(--color-border);
  cursor: pointer;
  transition: all var(--transition-fast);
}
.logout-btn:hover {
  color: var(--color-nova);
  border-color: var(--color-nova-border);
  background: var(--color-nova-dim);
}

/* ── Mobile nav ── */
.mobile-nav {
  display: none;
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--color-nebula);
  border-top: 1px solid var(--color-border);
  z-index: var(--z-topbar);
  padding-bottom: env(safe-area-inset-bottom, 0);
}

.mnav-item {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-1);
  padding: var(--space-2) var(--space-1);
  color: var(--color-dust);
  text-decoration: none;
  font-size: var(--text-2xs);
  font-family: var(--font-mono);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: var(--weight-medium);
  transition: color var(--transition-fast);
}
.mnav-item.router-link-exact-active { color: var(--color-orbit); }

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

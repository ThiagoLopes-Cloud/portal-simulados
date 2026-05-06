<template>
  <aside class="simuslab-sidebar" :class="{ 'sidebar--collapsed': collapsed }">
    <!-- Logo -->
    <div class="sidebar-logo">
      <SimuslabLogo :variant="collapsed ? 'icon-only' : 'default'" size="sm" />
    </div>

    <!-- Navigation -->
    <nav class="sidebar-nav" role="navigation">
      <template v-for="group in navigation" :key="group.id">
        <p v-if="group.label && !collapsed" class="nav-section-label">{{ group.label }}</p>
        <hr v-else-if="group.label && collapsed" class="nav-divider-line" />

        <router-link
          v-for="item in group.items"
          :key="item.to"
          :to="item.to"
          class="nav-item"
          :class="{ 'nav-item--admin': item.admin }"
          :title="collapsed ? item.label : undefined"
        >
          <span class="nav-icon">{{ item.icon }}</span>
          <span class="nav-label">{{ item.label }}</span>
        </router-link>
      </template>
    </nav>

    <!-- Footer -->
    <div class="sidebar-footer">
      <button class="collapse-btn" @click="$emit('toggle')" :title="collapsed ? 'Expandir menu' : 'Recolher menu'">
        <span class="collapse-icon" :class="{ 'rotate-180': collapsed }">‹</span>
        <span class="nav-label">Recolher</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import SimuslabLogo from '../ui/SimuslabLogo.vue'

defineProps({
  collapsed: { type: Boolean, default: false },
  navigation: { type: Array, default: () => [] },
})
defineEmits(['toggle'])
</script>

<style scoped>
.simuslab-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: var(--sidebar-width);
  background: #ffffff;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  z-index: var(--z-sidebar);
  transition: width var(--transition-slow);
  overflow: hidden;
}

.sidebar--collapsed { width: var(--sidebar-width-collapsed); }

/* ── Logo ── */
.sidebar-logo {
  padding: var(--space-5) var(--space-4);
  border-bottom: 1px solid #f1f5f9;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  min-height: var(--topbar-height);
}

/* ── Nav ── */
.sidebar-nav {
  flex: 1;
  padding: var(--space-4) var(--space-3);
  overflow-y: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.nav-section-label {
  font-family: var(--font-body);
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #94a3b8;
  font-weight: 600;
  padding: var(--space-4) var(--space-3) var(--space-1);
  white-space: nowrap;
  overflow: hidden;
}

.nav-divider-line {
  border: none;
  border-top: 1px solid #f1f5f9;
  margin: var(--space-3) var(--space-2);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 10px var(--space-3);
  border-radius: 10px;
  color: #475569;
  font-family: var(--font-body);
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.15s ease;
  white-space: nowrap;
  overflow: hidden;
  border: 1px solid transparent;
}

.nav-item:hover {
  color: #1e293b;
  background: #f8fafc;
}

.nav-item.router-link-exact-active {
  color: #1d4ed8;
  background: #eff6ff;
  border-color: #bfdbfe;
  font-weight: 600;
}

.nav-item--admin.router-link-exact-active {
  color: #6d28d9;
  background: #f5f3ff;
  border-color: #ddd6fe;
}

.nav-icon {
  font-size: 1rem;
  flex-shrink: 0;
  width: 20px;
  text-align: center;
  opacity: 0.7;
}

.nav-item.router-link-exact-active .nav-icon { opacity: 1; }

.nav-label {
  overflow: hidden;
  white-space: nowrap;
  transition: opacity var(--transition-slow), width var(--transition-slow);
}

/* ── Collapsed ── */
.sidebar--collapsed .nav-label  { opacity: 0; width: 0; }
.sidebar--collapsed .nav-section-label { opacity: 0; }
.sidebar--collapsed .nav-item { justify-content: center; }

/* ── Footer ── */
.sidebar-footer {
  padding: var(--space-3);
  border-top: 1px solid #f1f5f9;
  flex-shrink: 0;
}

.collapse-btn {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  width: 100%;
  padding: 10px var(--space-3);
  border-radius: 10px;
  color: #94a3b8;
  font-family: var(--font-body);
  font-size: 0.875rem;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
  overflow: hidden;
}
.collapse-btn:hover { color: #475569; background: #f8fafc; }

.collapse-icon {
  font-size: 1.2rem;
  flex-shrink: 0;
  width: 20px;
  text-align: center;
  display: inline-block;
  transition: transform var(--transition-slow);
}
.rotate-180 { transform: rotate(180deg); }
.sidebar--collapsed .collapse-btn { justify-content: center; }
</style>

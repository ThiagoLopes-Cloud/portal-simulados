<template>
  <aside class="orbyn-sidebar" :class="{ 'sidebar--collapsed': collapsed }">
    <!-- Logo -->
    <div class="sidebar-logo">
      <OrbynLogo :variant="collapsed ? 'icon-only' : 'default'" size="sm" />
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
      <!-- Toggle button -->
      <button class="collapse-btn" @click="$emit('toggle')" :title="collapsed ? 'Expandir menu' : 'Recolher menu'">
        <span class="collapse-icon" :class="{ 'rotate-180': collapsed }">‹</span>
        <span class="nav-label">Recolher</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import OrbynLogo from '../ui/OrbynLogo.vue'

defineProps({
  /** Collapsed state */
  collapsed: { type: Boolean, default: false },
  /**
   * Navigation groups:
   * [{ id, label?, items: [{ to, icon, label, admin? }] }]
   */
  navigation: {
    type: Array,
    default: () => [],
  },
})

defineEmits(['toggle'])
</script>

<style scoped>
.orbyn-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: var(--sidebar-width);
  background: var(--color-nebula);
  border-right: 1px solid var(--color-border);
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
  border-bottom: 1px solid var(--color-border);
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
  gap: var(--space-1);
}

.nav-section-label {
  font-family: var(--font-mono);
  font-size: var(--text-2xs);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-dust);
  padding: var(--space-4) var(--space-3) var(--space-1);
  white-space: nowrap;
  overflow: hidden;
}

.nav-divider-line {
  border: none;
  border-top: 1px solid var(--color-border);
  margin: var(--space-3) var(--space-2);
}

.nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  color: var(--color-comet);
  font-family: var(--font-body);
  font-size: var(--text-base);
  font-weight: var(--weight-medium);
  text-decoration: none;
  transition: all var(--transition-normal);
  white-space: nowrap;
  overflow: hidden;
  border: 1px solid transparent;
}

.nav-item:hover {
  color: var(--color-star);
  background: var(--color-surface-hover);
}

.nav-item.router-link-exact-active {
  color: var(--color-orbit);
  background: var(--color-orbit-dim);
  border-color: var(--color-orbit-border);
}

.nav-item--admin.router-link-exact-active {
  color: var(--color-pulsar);
  background: var(--color-pulsar-dim);
  border-color: var(--color-pulsar-border);
}

.nav-icon {
  font-size: 1.1rem;
  flex-shrink: 0;
  width: 20px;
  text-align: center;
}

.nav-label {
  overflow: hidden;
  white-space: nowrap;
  transition: opacity var(--transition-slow), width var(--transition-slow);
}

/* ── Collapsed: hide labels ── */
.sidebar--collapsed .nav-label  { opacity: 0; width: 0; }
.sidebar--collapsed .nav-section-label { opacity: 0; }
.sidebar--collapsed .nav-item { justify-content: center; }

/* ── Footer ── */
.sidebar-footer {
  padding: var(--space-3);
  border-top: 1px solid var(--color-border);
  flex-shrink: 0;
}

.collapse-btn {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  width: 100%;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-md);
  color: var(--color-dust);
  font-family: var(--font-body);
  font-size: var(--text-base);
  background: none;
  border: none;
  cursor: pointer;
  transition: all var(--transition-normal);
  white-space: nowrap;
  overflow: hidden;
}
.collapse-btn:hover { color: var(--color-comet); background: var(--color-surface-hover); }

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

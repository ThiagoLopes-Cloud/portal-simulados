<template>
  <aside class="sl-sidebar" :class="{ 'sl-sidebar--collapsed': collapsed }">
    <!-- Logo -->
    <div class="sl-sidebar-logo">
      <SimuslabLogo :variant="collapsed ? 'icon-only' : 'default'" size="sm" />
    </div>

    <!-- Navigation -->
    <nav class="sl-sidebar-nav" role="navigation" aria-label="Menu principal">
      <template v-for="group in navigation" :key="group.id">
        <p v-if="group.label && !collapsed" class="sl-nav-section">{{ group.label }}</p>
        <hr v-else-if="group.label && collapsed" class="sl-nav-divider" />

        <router-link
          v-for="item in group.items"
          :key="item.to"
          :to="item.to"
          class="sl-nav-item"
          :class="{ 'sl-nav-item--admin': item.admin }"
          :title="collapsed ? item.label : undefined"
        >
          <span class="sl-nav-icon" aria-hidden="true">
            <svg
              width="18"
              height="18"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.75"
              stroke-linecap="round"
              stroke-linejoin="round"
              v-html="getIcon(item.icon)"
            />
          </span>
          <span class="sl-nav-label">{{ item.label }}</span>
        </router-link>
      </template>
    </nav>

    <!-- Footer -->
    <div class="sl-sidebar-footer">
      <button
        class="sl-collapse-btn"
        @click="$emit('toggle')"
        :title="collapsed ? 'Expandir menu' : 'Recolher menu'"
        :aria-label="collapsed ? 'Expandir menu' : 'Recolher menu'"
      >
        <span class="sl-collapse-icon" :class="{ 'sl-collapse-icon--rotated': collapsed }">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="15 18 9 12 15 6"/>
          </svg>
        </span>
        <span class="sl-nav-label">Recolher</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import SimuslabLogo from '../ui/SimuslabLogo.vue'
import { icons } from '../../utils/icons.js'

defineProps({
  collapsed: { type: Boolean, default: false },
  navigation: { type: Array, default: () => [] },
})
defineEmits(['toggle'])

function getIcon(name) {
  return icons[name] ?? icons.dashboard
}
</script>

<style scoped>
.sl-sidebar {
  position: fixed;
  top: 0;
  left: 0;
  height: 100vh;
  width: var(--sidebar-width);
  background: #ffffff;
  border-right: 1px solid #e8ecf2;
  display: flex;
  flex-direction: column;
  z-index: var(--z-sidebar);
  transition: width var(--transition-slow);
  overflow: hidden;
}

.sl-sidebar--collapsed { width: var(--sidebar-width-collapsed); }

/* ── Logo ── */
.sl-sidebar-logo {
  padding: 0 var(--space-4);
  border-bottom: 1px solid #f1f5f9;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  min-height: var(--topbar-height);
}

/* ── Nav ── */
.sl-sidebar-nav {
  flex: 1;
  padding: var(--space-4) var(--space-3);
  overflow-y: auto;
  overflow-x: hidden;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.sl-nav-section {
  font-family: var(--font-body);
  font-size: 0.65rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #b0bac9;
  font-weight: 700;
  padding: var(--space-4) var(--space-2) var(--space-1);
  white-space: nowrap;
  overflow: hidden;
}

.sl-nav-divider {
  border: none;
  border-top: 1px solid #f1f5f9;
  margin: var(--space-3) var(--space-2);
}

.sl-nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 9px var(--space-3);
  border-radius: 9px;
  color: #64748b;
  font-family: var(--font-body);
  font-size: 0.875rem;
  font-weight: 500;
  text-decoration: none;
  transition: background 0.12s ease, color 0.12s ease;
  white-space: nowrap;
  overflow: hidden;
  border: 1px solid transparent;
}

.sl-nav-item:hover {
  color: #1e293b;
  background: #f8fafc;
}

.sl-nav-item.router-link-exact-active {
  color: #1d4ed8;
  background: #eff6ff;
  font-weight: 600;
}

.sl-nav-item--admin.router-link-exact-active {
  color: #6d28d9;
  background: #f5f3ff;
}

/* ── Icon ── */
.sl-nav-icon {
  flex-shrink: 0;
  width: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.65;
}

.sl-nav-item.router-link-exact-active .sl-nav-icon { opacity: 1; }

/* ── Label ── */
.sl-nav-label {
  overflow: hidden;
  white-space: nowrap;
  transition: opacity var(--transition-slow), width var(--transition-slow);
}

/* ── Collapsed state ── */
.sl-sidebar--collapsed .sl-nav-label { opacity: 0; width: 0; }
.sl-sidebar--collapsed .sl-nav-section { opacity: 0; height: 0; padding: 0; }
.sl-sidebar--collapsed .sl-nav-item { justify-content: center; padding: 10px; }
.sl-sidebar--collapsed .sl-nav-item gap { gap: 0; }

/* ── Footer / collapse ── */
.sl-sidebar-footer {
  padding: var(--space-3);
  border-top: 1px solid #f1f5f9;
  flex-shrink: 0;
}

.sl-collapse-btn {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  width: 100%;
  padding: 9px var(--space-3);
  border-radius: 9px;
  color: #94a3b8;
  font-family: var(--font-body);
  font-size: 0.875rem;
  background: none;
  border: none;
  cursor: pointer;
  transition: all 0.12s ease;
  white-space: nowrap;
  overflow: hidden;
}

.sl-collapse-btn:hover { color: #475569; background: #f8fafc; }

.sl-collapse-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform var(--transition-slow);
}
.sl-collapse-icon--rotated { transform: rotate(180deg); }

.sl-sidebar--collapsed .sl-collapse-btn { justify-content: center; }

/* ── Mobile ── */
@media (max-width: 768px) {
  .sl-sidebar { display: none; }
}
</style>

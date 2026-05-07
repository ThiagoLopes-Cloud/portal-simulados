<template>
  <aside class="sl-sidebar" :class="{ 'sl-sidebar--collapsed': collapsed }" aria-label="Navegação lateral">
    <!-- Logo -->
    <div class="sl-sidebar-logo">
      <SimuslabLogo :variant="collapsed ? 'icon-only' : 'default'" size="sm" />
    </div>

    <!-- Navigation -->
    <nav class="sl-sidebar-nav" role="navigation" aria-label="Menu principal">
      <template v-for="group in navigation" :key="group.id">
        <p v-if="group.label && !collapsed" class="sl-nav-section">{{ group.label }}</p>
        <hr v-else-if="group.label && collapsed" class="sl-nav-divider" aria-hidden="true" />

        <router-link
          v-for="item in group.items"
          :key="item.to"
          :to="item.to"
          class="sl-nav-item"
          :class="{ 'sl-nav-item--admin': item.admin }"
          :aria-label="collapsed ? item.label : undefined"
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
        type="button"
        class="sl-collapse-btn"
        :aria-label="collapsed ? 'Expandir menu' : 'Recolher menu'"
        :title="collapsed ? 'Expandir menu' : 'Recolher menu'"
        @click="$emit('toggle')"
      >
        <span class="sl-collapse-icon" :class="{ 'sl-collapse-icon--rotated': collapsed }" aria-hidden="true">
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
  collapsed:  { type: Boolean, default: false },
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
  background: var(--color-bg-panel);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  z-index: var(--z-sidebar);
  transition: width var(--duration-slow) var(--ease-in-out);
  overflow: hidden;
}

.sl-sidebar--collapsed { width: var(--sidebar-width-collapsed); }

/* ── Logo ── */
.sl-sidebar-logo {
  padding: 0 var(--space-4);
  border-bottom: 1px solid var(--color-border);
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
  font-size: var(--text-2xs);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-dust);
  font-weight: var(--weight-bold);
  padding: var(--space-4) var(--space-2) var(--space-1);
  white-space: nowrap;
  overflow: hidden;
}

.sl-nav-divider {
  border: none;
  border-top: 1px solid var(--color-border);
  margin: var(--space-3) var(--space-2);
}

.sl-nav-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: 9px var(--space-3);
  border-radius: var(--radius-md);
  color: var(--color-comet);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  text-decoration: none;
  white-space: nowrap;
  overflow: hidden;
  border: 1px solid transparent;
  transition:
    color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out);
}

.sl-nav-item:hover {
  color: var(--color-star);
  background: var(--color-surface-hover);
}

.sl-nav-item:focus-visible {
  outline: none;
  box-shadow: var(--shadow-focus);
}

.sl-nav-item.router-link-exact-active {
  color: var(--color-orbit);
  background: var(--color-orbit-dim);
  border-color: var(--color-orbit-border);
  font-weight: var(--weight-semibold);
}

.sl-nav-item--admin.router-link-exact-active {
  color: var(--color-pulsar);
  background: var(--color-pulsar-dim);
  border-color: var(--color-pulsar-border);
}

/* ── Icon ── */
.sl-nav-icon {
  flex-shrink: 0;
  width: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0.6;
  transition: opacity var(--duration-fast) var(--ease-out);
}

.sl-nav-item:hover .sl-nav-icon,
.sl-nav-item.router-link-exact-active .sl-nav-icon { opacity: 1; }

/* ── Label ── */
.sl-nav-label {
  overflow: hidden;
  white-space: nowrap;
  transition:
    opacity var(--duration-slow) var(--ease-in-out),
    width var(--duration-slow) var(--ease-in-out);
}

/* ── Collapsed state ── */
.sl-sidebar--collapsed .sl-nav-label   { opacity: 0; width: 0; }
.sl-sidebar--collapsed .sl-nav-section { opacity: 0; height: 0; padding: 0; }
.sl-sidebar--collapsed .sl-nav-item   { justify-content: center; padding: 10px; }

/* ── Footer / collapse ── */
.sl-sidebar-footer {
  padding: var(--space-3);
  border-top: 1px solid var(--color-border);
  flex-shrink: 0;
}

.sl-collapse-btn {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  width: 100%;
  padding: 9px var(--space-3);
  border-radius: var(--radius-md);
  color: var(--color-dust);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  background: none;
  border: none;
  cursor: pointer;
  white-space: nowrap;
  overflow: hidden;
  transition:
    color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out);
}

.sl-collapse-btn:hover { color: var(--color-comet); background: var(--color-surface-hover); }
.sl-collapse-btn:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

.sl-collapse-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform var(--duration-slow) var(--ease-in-out);
}
.sl-collapse-icon--rotated { transform: rotate(180deg); }

.sl-sidebar--collapsed .sl-collapse-btn { justify-content: center; }

/* ── Mobile ── */
@media (max-width: 768px) {
  .sl-sidebar { display: none; }
}
</style>

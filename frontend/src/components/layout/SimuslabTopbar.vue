<template>
  <header class="simuslab-topbar" :style="topbarStyle">
    <!-- Left: logo slot -->
    <div class="topbar-left">
      <slot name="left">
        <SimuslabLogo size="sm" />
      </slot>
    </div>

    <!-- Center: navigation slot -->
    <div class="topbar-center">
      <slot name="center" />
    </div>

    <!-- Right: actions slot -->
    <div class="topbar-right">
      <slot name="right" />

      <!-- User avatar -->
      <div v-if="username" class="topbar-avatar" :title="username">
        {{ initials }}
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'
import SimuslabLogo from '../ui/SimuslabLogo.vue'

const props = defineProps({
  /** Username for avatar initials */
  username: { type: String, default: '' },
  /** Sidebar width to offset topbar left edge */
  sidebarWidth: { type: String, default: 'var(--sidebar-width)' },
})

const initials = computed(() => {
  if (!props.username) return ''
  return props.username
    .split(' ')
    .slice(0, 2)
    .map(w => w[0]?.toUpperCase())
    .join('')
})

const topbarStyle = computed(() => ({
  left: props.sidebarWidth,
  width: `calc(100% - ${props.sidebarWidth})`,
}))
</script>

<style scoped>
.simuslab-topbar {
  position: fixed;
  top: 0;
  right: 0;
  height: var(--topbar-height);
  background: rgba(13, 16, 36, 0.75);
  backdrop-filter: blur(var(--blur-md));
  -webkit-backdrop-filter: blur(var(--blur-md));
  border-bottom: 1px solid var(--color-border);
  z-index: var(--z-topbar);
  display: flex;
  align-items: center;
  padding: 0 var(--space-6);
  gap: var(--space-4);
  transition: left var(--transition-slow), width var(--transition-slow);
}

.topbar-left {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.topbar-center {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
}

.topbar-right {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-shrink: 0;
}

/* ── Avatar ── */
.topbar-avatar {
  width: 34px;
  height: 34px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--color-orbit-dim), var(--color-pulsar-dim));
  border: 1px solid var(--color-orbit-border);
  color: var(--color-orbit);
  font-family: var(--font-display);
  font-weight: var(--weight-bold);
  font-size: var(--text-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: default;
  flex-shrink: 0;
  letter-spacing: 0.02em;
}
</style>

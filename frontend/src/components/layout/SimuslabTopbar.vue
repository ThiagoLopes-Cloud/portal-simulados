<template>
  <header class="simuslab-topbar" :style="topbarStyle">
    <div class="topbar-left">
      <slot name="left" />
    </div>

    <div class="topbar-center">
      <slot name="center" />
    </div>

    <div class="topbar-right">
      <slot name="right" />

      <div v-if="username" class="topbar-user">
        <span class="topbar-username">{{ displayName }}</span>
        <div class="topbar-avatar" :title="username">{{ initials }}</div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  username: { type: String, default: '' },
  sidebarWidth: { type: String, default: 'var(--sidebar-width)' },
})

const initials = computed(() => {
  if (!props.username) return ''
  return props.username.split(' ').slice(0, 2).map(w => w[0]?.toUpperCase()).join('')
})

const displayName = computed(() => {
  if (!props.username) return ''
  const parts = props.username.split(' ')
  return parts[0]
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
  background: rgba(255, 255, 255, 0.92);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid #e2e8f0;
  z-index: var(--z-topbar);
  display: flex;
  align-items: center;
  padding: 0 var(--space-6);
  gap: var(--space-4);
  transition: left var(--transition-slow), width var(--transition-slow);
}

/* ── Mobile: topbar ocupa a largura total (sem sidebar) ── */
@media (max-width: 768px) {
  .simuslab-topbar {
    left: 0 !important;
    width: 100% !important;
  }
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

/* ── User info ── */
.topbar-user {
  display: flex;
  align-items: center;
  gap: var(--space-2);
}

.topbar-username {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  font-weight: 500;
  color: #64748b;
}

/* ── Avatar ── */
.topbar-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: #eff6ff;
  border: 1.5px solid #bfdbfe;
  color: #2563eb;
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: default;
  flex-shrink: 0;
  letter-spacing: 0.02em;
}
</style>

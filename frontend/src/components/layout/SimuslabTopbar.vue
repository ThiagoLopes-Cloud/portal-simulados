<template>
  <header class="sl-topbar" :style="topbarStyle">
    <div class="sl-topbar-left">
      <slot name="left" />
    </div>

    <div class="sl-topbar-center">
      <slot name="center" />
    </div>

    <div class="sl-topbar-right">
      <slot name="right" />

      <div v-if="username" class="sl-topbar-user">
        <div class="sl-user-info">
          <span class="sl-username">{{ displayName }}</span>
          <span class="sl-user-role">{{ roleLabel }}</span>
        </div>
        <button class="sl-avatar" :title="username" aria-label="Menu do usuário">
          {{ initials }}
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  username:     { type: String, default: '' },
  sidebarWidth: { type: String, default: 'var(--sidebar-width)' },
})

const initials = computed(() => {
  if (!props.username) return ''
  return props.username.split(' ').slice(0, 2).map(w => w[0]?.toUpperCase()).join('')
})

const displayName = computed(() => {
  if (!props.username) return ''
  return props.username.split(' ')[0]
})

const roleLabel = computed(() => {
  const role = localStorage.getItem('user_role')
  return role === 'admin' ? 'Administrador' : 'Aluno'
})

const topbarStyle = computed(() => ({
  left: props.sidebarWidth,
  width: `calc(100% - ${props.sidebarWidth})`,
}))
</script>

<style scoped>
.sl-topbar {
  position: fixed;
  top: 0;
  right: 0;
  height: var(--topbar-height);
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid #e8ecf2;
  z-index: var(--z-topbar);
  display: flex;
  align-items: center;
  padding: 0 var(--space-6);
  gap: var(--space-4);
  transition: left var(--transition-slow), width var(--transition-slow);
}

@media (max-width: 768px) {
  .sl-topbar {
    left: 0 !important;
    width: 100% !important;
  }
}

.sl-topbar-left {
  display: flex;
  align-items: center;
  flex-shrink: 0;
}

.sl-topbar-center {
  flex: 1;
  display: flex;
  align-items: center;
}

.sl-topbar-right {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-shrink: 0;
  margin-left: auto;
}

/* ── User section ── */
.sl-topbar-user {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.sl-user-info {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 1px;
}

.sl-username {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  font-weight: 600;
  color: #1e293b;
  line-height: 1;
}

.sl-user-role {
  font-family: var(--font-body);
  font-size: 0.65rem;
  font-weight: 500;
  color: #94a3b8;
  line-height: 1;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

/* ── Avatar ── */
.sl-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  background: #eff6ff;
  border: 1.5px solid #bfdbfe;
  color: #1d4ed8;
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 0.75rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: default;
  flex-shrink: 0;
  letter-spacing: 0.02em;
  transition: all 0.12s ease;
}

.sl-avatar:hover {
  background: #dbeafe;
  border-color: #93c5fd;
}

@media (max-width: 640px) {
  .sl-user-info { display: none; }
}
</style>

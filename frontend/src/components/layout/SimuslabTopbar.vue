<template>
  <header class="sl-topbar" :style="topbarStyle" role="banner">
    <div class="sl-topbar-left">
      <slot name="left" />
    </div>

    <div class="sl-topbar-center">
      <slot name="center" />
    </div>

    <div class="sl-topbar-right">
      <slot name="right" />

      <div v-if="username" class="sl-topbar-user">
        <div class="sl-user-info" aria-hidden="true">
          <span class="sl-username">{{ displayName }}</span>
          <span class="sl-user-role">{{ roleLabel }}</span>
        </div>
        <div class="sl-avatar" :aria-label="`Usuário: ${username}`" role="img">
          {{ initials }}
        </div>
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
  background: rgba(13, 16, 36, 0.9);
  backdrop-filter: blur(var(--blur-md));
  -webkit-backdrop-filter: blur(var(--blur-md));
  border-bottom: 1px solid var(--color-border);
  z-index: var(--z-topbar);
  display: flex;
  align-items: center;
  padding: 0 var(--space-6);
  gap: var(--space-4);
  transition:
    left var(--duration-slow) var(--ease-in-out),
    width var(--duration-slow) var(--ease-in-out);
}

@media (max-width: 768px) {
  .sl-topbar {
    left: 0 !important;
    width: 100% !important;
    padding: 0 var(--space-4);
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
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  color: var(--color-star);
  line-height: 1;
}

.sl-user-role {
  font-family: var(--font-body);
  font-size: var(--text-2xs);
  font-weight: var(--weight-medium);
  color: var(--color-dust);
  line-height: 1;
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
}

/* ── Avatar ── */
.sl-avatar {
  width: 34px;
  height: 34px;
  border-radius: var(--radius-full);
  background: var(--color-orbit-dim);
  border: 1.5px solid var(--color-orbit-border);
  color: var(--color-orbit);
  font-family: var(--font-display);
  font-weight: var(--weight-bold);
  font-size: var(--text-xs);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  letter-spacing: 0.02em;
  transition:
    background-color var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out);
}

.sl-avatar:hover {
  background: var(--color-orbit-glow);
  border-color: var(--color-orbit);
}

@media (max-width: 640px) {
  .sl-user-info { display: none; }
}
</style>

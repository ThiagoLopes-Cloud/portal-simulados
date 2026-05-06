<template>
  <Teleport to="body">
    <div class="toast-container" aria-live="polite" aria-atomic="false">
      <TransitionGroup name="toast" tag="div" class="toast-list">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          class="toast-item"
          :class="`toast--${toast.type}`"
          role="alert"
        >
          <span class="toast-icon">{{ icons[toast.type] }}</span>
          <span class="toast-message">{{ toast.message }}</span>
          <button class="toast-close" @click="removeToast(toast.id)" aria-label="Fechar">×</button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import { useUIStore } from '../../stores/ui.store.js'

const ui = useUIStore()
const { toasts } = storeToRefs(ui)
const { removeToast } = ui

const icons = {
  success: '✓',
  error:   '✕',
  warning: '⚠',
  info:    'ℹ',
}
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: var(--space-5);
  right: var(--space-5);
  z-index: var(--z-toast);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  pointer-events: none;
}

.toast-list { display: contents; }

.toast-item {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  background: var(--color-void);
  backdrop-filter: blur(var(--blur-md));
  -webkit-backdrop-filter: blur(var(--blur-md));
  box-shadow: var(--shadow-lg);
  min-width: 280px;
  max-width: 360px;
  pointer-events: all;
}

/* ── Type variants ── */
.toast--success {
  border-color: var(--color-stellar-border);
  background: rgba(11, 9, 26, 0.92);
}
.toast--success .toast-icon { color: var(--color-stellar); }

.toast--error {
  border-color: var(--color-nova-border);
  background: rgba(11, 9, 26, 0.92);
}
.toast--error .toast-icon { color: var(--color-nova); }

.toast--warning {
  border-color: var(--color-flare-border);
  background: rgba(11, 9, 26, 0.92);
}
.toast--warning .toast-icon { color: var(--color-flare); }

.toast--info {
  border-color: var(--color-orbit-border);
  background: rgba(11, 9, 26, 0.92);
}
.toast--info .toast-icon { color: var(--color-orbit); }

/* ── Parts ── */
.toast-icon {
  font-size: 1rem;
  font-weight: var(--weight-bold);
  flex-shrink: 0;
  width: 20px;
  text-align: center;
}

.toast-message {
  flex: 1;
  font-family: var(--font-body);
  font-size: var(--text-base);
  color: var(--color-star);
  line-height: var(--leading-snug);
}

.toast-close {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  border-radius: var(--radius-sm);
  color: var(--color-comet);
  font-size: 1.1rem;
  line-height: 1;
  cursor: pointer;
  background: none;
  border: none;
  padding: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: color var(--transition-fast);
}
.toast-close:hover { color: var(--color-star); }

/* ── Transitions ── */
.toast-enter-active {
  animation: slideInRight 0.3s cubic-bezier(0.34, 1.56, 0.64, 1) both;
}
.toast-leave-active {
  animation: slideOutRight 0.25s ease-in both;
}
.toast-move {
  transition: transform 0.3s ease;
}
</style>

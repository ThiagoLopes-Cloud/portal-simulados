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
          <span class="toast-icon" aria-hidden="true" v-html="icons[toast.type]" />
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

const svgAttrs = `width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"`

const icons = {
  success: `<svg ${svgAttrs}><polyline points="20 6 9 17 4 12"/></svg>`,
  error:   `<svg ${svgAttrs}><circle cx="12" cy="12" r="10"/><line x1="15" y1="9" x2="9" y2="15"/><line x1="9" y1="9" x2="15" y2="15"/></svg>`,
  warning: `<svg ${svgAttrs}><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>`,
  info:    `<svg ${svgAttrs}><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>`,
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
  flex-shrink: 0;
  width: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toast-message {
  flex: 1;
  font-family: var(--font-body);
  font-size: var(--text-sm);
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
  transition: color var(--duration-fast) var(--ease-out);
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

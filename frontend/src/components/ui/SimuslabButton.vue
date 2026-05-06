<template>
  <component
    :is="as"
    :class="classes"
    :disabled="disabled || loading"
    v-bind="$attrs"
    @click="!disabled && !loading && $emit('click', $event)"
  >
    <span v-if="loading" class="btn-spinner" aria-hidden="true" />
    <slot v-else />
    <span v-if="loading" class="btn-loading-text">
      <slot name="loading">Aguarde...</slot>
    </span>
  </component>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /** 'primary' | 'secondary' | 'ghost' | 'danger' */
  variant: {
    type: String,
    default: 'primary',
    validator: v => ['primary', 'secondary', 'ghost', 'danger'].includes(v),
  },
  /** 'sm' | 'md' | 'lg' */
  size: {
    type: String,
    default: 'md',
    validator: v => ['sm', 'md', 'lg'].includes(v),
  },
  /** Show loading spinner */
  loading: { type: Boolean, default: false },
  /** Disabled state */
  disabled: { type: Boolean, default: false },
  /** Renders as button or anchor */
  as: { type: String, default: 'button' },
  /** Full width */
  block: { type: Boolean, default: false },
})

defineEmits(['click'])

const classes = computed(() => [
  'simuslab-btn',
  `btn--${props.variant}`,
  `btn--${props.size}`,
  { 'btn--loading': props.loading, 'btn--block': props.block },
])
</script>

<style scoped>
.simuslab-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  font-family: var(--font-display);
  font-weight: var(--weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.07em;
  border-radius: var(--radius-lg);
  border: 1px solid transparent;
  cursor: pointer;
  transition: all var(--transition-normal);
  white-space: nowrap;
  text-decoration: none;
  position: relative;
  overflow: hidden;
}

.simuslab-btn:focus-visible {
  outline: 2px solid var(--color-orbit);
  outline-offset: 2px;
}

.simuslab-btn:disabled,
.simuslab-btn.btn--loading {
  opacity: 0.5;
  pointer-events: none;
}

.btn--block { width: 100%; }

/* ── Sizes ── */
.btn--sm {
  padding: var(--space-2) var(--space-4);
  font-size: var(--text-sm);
  gap: var(--space-1);
}

.btn--md {
  padding: var(--space-3) var(--space-6);
  font-size: var(--text-base);
}

.btn--lg {
  padding: var(--space-4) var(--space-8);
  font-size: var(--text-md);
}

/* ── Variants ── */
.btn--primary {
  background: var(--color-orbit);
  color: var(--color-cosmos);
  border-color: var(--color-orbit);
}
.btn--primary:hover {
  transform: translateY(-1px) scale(1.02);
  box-shadow: var(--shadow-orbit);
}
.btn--primary:active { transform: scale(0.98); }

.btn--secondary {
  background: var(--color-orbit-dim);
  color: var(--color-orbit);
  border-color: var(--color-orbit-border);
}
.btn--secondary:hover {
  background: var(--color-orbit-mid);
  box-shadow: 0 0 12px var(--color-orbit-glow);
}

.btn--ghost {
  background: transparent;
  color: var(--color-comet);
  border-color: var(--color-border);
}
.btn--ghost:hover {
  color: var(--color-star);
  background: var(--color-surface-hover);
  border-color: var(--color-border-hover);
}

.btn--danger {
  background: var(--color-nova-dim);
  color: var(--color-nova);
  border-color: var(--color-nova-border);
}
.btn--danger:hover {
  background: rgba(255, 77, 109, 0.15);
  box-shadow: var(--shadow-nova);
}

/* ── Spinner ── */
.btn-spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.25);
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spinnerRing 0.6s linear infinite;
  flex-shrink: 0;
}

.btn--primary .btn-spinner {
  border-color: rgba(8, 9, 26, 0.25);
  border-top-color: var(--color-cosmos);
}

.btn-loading-text { font-size: inherit; }
</style>

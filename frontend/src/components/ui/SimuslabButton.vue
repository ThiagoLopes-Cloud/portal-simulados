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
  variant: {
    type: String,
    default: 'primary',
    validator: v => ['primary', 'secondary', 'ghost', 'danger'].includes(v),
  },
  size: {
    type: String,
    default: 'md',
    validator: v => ['sm', 'md', 'lg'].includes(v),
  },
  loading:  { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  as:       { type: String, default: 'button' },
  block:    { type: Boolean, default: false },
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
  font-family: var(--font-body);
  font-weight: var(--weight-semibold);
  border-radius: var(--btn-radius);
  border: 1px solid transparent;
  cursor: pointer;
  white-space: nowrap;
  text-decoration: none;
  position: relative;
  overflow: hidden;
  letter-spacing: 0;
  text-transform: none;
  transition:
    color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out),
    box-shadow var(--duration-normal) var(--ease-out),
    transform var(--duration-fast) var(--ease-spring);
}

.simuslab-btn:focus-visible {
  outline: none;
  box-shadow: var(--shadow-focus);
}

.simuslab-btn:disabled,
.simuslab-btn.btn--loading {
  opacity: 0.45;
  pointer-events: none;
}

.btn--block { width: 100%; }

/* ── Sizes ── */
.btn--sm {
  height: var(--btn-height-sm);
  padding: 0 var(--space-3);
  font-size: var(--text-xs);
  gap: var(--space-1-5);
}

.btn--md {
  height: var(--btn-height-md);
  padding: 0 var(--space-4);
  font-size: var(--text-sm);
}

.btn--lg {
  height: var(--btn-height-lg);
  padding: 0 var(--space-6);
  font-size: var(--text-base);
}

/* ── Variants ── */
.btn--primary {
  background: var(--color-orbit);
  color: var(--color-cosmos);
  border-color: var(--color-orbit);
  box-shadow: 0 1px 3px var(--color-orbit-glow);
}
.btn--primary:hover {
  background: var(--color-orbit-bright);
  border-color: var(--color-orbit-bright);
  box-shadow: var(--shadow-orbit);
  transform: translateY(-1px);
}
.btn--primary:active {
  transform: translateY(0) scale(0.98);
  box-shadow: none;
}

.btn--secondary {
  background: var(--color-bg-surface);
  color: var(--color-star);
  border-color: var(--color-border);
}
.btn--secondary:hover {
  background: var(--color-bg-elevated);
  border-color: var(--color-border-hover);
}
.btn--secondary:active { transform: scale(0.98); }

.btn--ghost {
  background: transparent;
  color: var(--color-comet);
  border-color: transparent;
}
.btn--ghost:hover {
  color: var(--color-star);
  background: var(--color-surface-hover);
}
.btn--ghost:active { transform: scale(0.98); }

.btn--danger {
  background: var(--color-nova-dim);
  color: var(--color-nova);
  border-color: var(--color-nova-border);
}
.btn--danger:hover {
  background: rgba(255, 77, 109, 0.15);
  border-color: var(--color-nova);
  box-shadow: var(--shadow-nova);
}
.btn--danger:active { transform: scale(0.98); }

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

.btn-loading-text { font-size: inherit; }
</style>

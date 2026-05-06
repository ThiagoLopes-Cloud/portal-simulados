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
  font-family: var(--font-body);
  font-weight: 600;
  border-radius: 10px;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
  text-decoration: none;
  position: relative;
  overflow: hidden;
  letter-spacing: 0;
  text-transform: none;
}

.simuslab-btn:focus-visible {
  outline: 2px solid #2563eb;
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
  padding: 6px 14px;
  font-size: 0.8125rem;
  gap: 5px;
}

.btn--md {
  padding: 9px 20px;
  font-size: 0.875rem;
}

.btn--lg {
  padding: 12px 28px;
  font-size: 1rem;
}

/* ── Variants ── */
.btn--primary {
  background: #2563eb;
  color: #ffffff;
  border-color: #2563eb;
  box-shadow: 0 1px 3px rgba(37, 99, 235, 0.3);
}
.btn--primary:hover {
  background: #1d4ed8;
  border-color: #1d4ed8;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.35);
  transform: translateY(-1px);
}
.btn--primary:active { transform: scale(0.98); }

.btn--secondary {
  background: #ffffff;
  color: #374151;
  border-color: #e2e8f0;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}
.btn--secondary:hover {
  background: #f8fafc;
  border-color: #cbd5e1;
}

.btn--ghost {
  background: transparent;
  color: #64748b;
  border-color: #e2e8f0;
}
.btn--ghost:hover {
  color: #0f172a;
  background: #f8fafc;
  border-color: #cbd5e1;
}

.btn--danger {
  background: #fef2f2;
  color: #b91c1c;
  border-color: #fecaca;
}
.btn--danger:hover {
  background: #fee2e2;
  border-color: #fca5a5;
}

/* ── Spinner ── */
.btn-spinner {
  display: inline-block;
  width: 14px;
  height: 14px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: currentColor;
  border-radius: 50%;
  animation: spinnerRing 0.6s linear infinite;
  flex-shrink: 0;
}

@keyframes spinnerRing { to { transform: rotate(360deg); } }

.btn-loading-text { font-size: inherit; }
</style>

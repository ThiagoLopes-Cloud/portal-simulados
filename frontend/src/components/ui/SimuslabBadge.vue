<template>
  <span class="simuslab-badge" :class="[`badge--${variant}`, `badge--${size}`]">
    <span v-if="dot" class="badge-dot" />
    <slot />
  </span>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'blue',
    validator: v => ['orbit', 'blue', 'pulsar', 'purple', 'nova', 'red', 'stellar', 'green', 'flare', 'amber', 'neutral'].includes(v),
  },
  size: { type: String, default: 'sm', validator: v => ['sm', 'md'].includes(v) },
  dot:  { type: Boolean, default: false },
})
</script>

<style scoped>
.simuslab-badge {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: var(--font-body);
  font-weight: 600;
  border-radius: 999px;
  border: 1px solid transparent;
  line-height: 1;
  white-space: nowrap;
}

/* ── Sizes ── */
.badge--sm { font-size: 0.7rem;  padding: 3px 10px; }
.badge--md { font-size: 0.75rem; padding: 4px 12px; }

/* ── Variants — paleta clean light ── */
.badge--orbit,
.badge--blue {
  background: #eff6ff;
  color: #1d4ed8;
  border-color: #bfdbfe;
}
.badge--pulsar,
.badge--purple {
  background: #f5f3ff;
  color: #6d28d9;
  border-color: #ddd6fe;
}
.badge--nova,
.badge--red {
  background: #fef2f2;
  color: #b91c1c;
  border-color: #fecaca;
}
.badge--stellar,
.badge--green {
  background: #f0fdf4;
  color: #166534;
  border-color: #bbf7d0;
}
.badge--flare,
.badge--amber {
  background: #fffbeb;
  color: #92400e;
  border-color: #fde68a;
}
.badge--neutral {
  background: #f8fafc;
  color: #475569;
  border-color: #e2e8f0;
}

/* ── Dot indicator ── */
.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  animation: simuslabPulse 2s ease-in-out infinite;
}
</style>

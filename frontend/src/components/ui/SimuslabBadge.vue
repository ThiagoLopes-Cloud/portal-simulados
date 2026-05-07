<template>
  <span class="simuslab-badge" :class="[`badge--${variant}`, `badge--${size}`]">
    <span v-if="dot" class="badge-dot" aria-hidden="true" />
    <slot />
  </span>
</template>

<script setup>
defineProps({
  variant: {
    type: String,
    default: 'neutral',
    validator: v => ['orbit', 'blue', 'pulsar', 'purple', 'nova', 'red', 'stellar', 'green', 'flare', 'amber', 'neutral', 'info'].includes(v),
  },
  size: { type: String, default: 'sm', validator: v => ['sm', 'md'].includes(v) },
  dot:  { type: Boolean, default: false },
})
</script>

<style scoped>
.simuslab-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-family: var(--font-body);
  font-size: var(--text-2xs);
  font-weight: var(--weight-semibold);
  border-radius: var(--badge-radius);
  border: 1px solid transparent;
  line-height: 1;
  white-space: nowrap;
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
}

/* ── Sizes ── */
.badge--sm { padding: 3px 10px; }
.badge--md { padding: var(--space-1) var(--space-3); font-size: var(--text-xs); }

/* ── Variants — dark-friendly ── */
.badge--orbit,
.badge--blue {
  background: var(--color-orbit-dim);
  color: var(--color-orbit-bright);
  border-color: var(--color-orbit-border);
}

.badge--pulsar,
.badge--purple {
  background: var(--color-pulsar-dim);
  color: var(--color-pulsar-bright);
  border-color: var(--color-pulsar-border);
}

.badge--nova,
.badge--red {
  background: var(--color-nova-dim);
  color: var(--color-nova);
  border-color: var(--color-nova-border);
}

.badge--stellar,
.badge--green {
  background: var(--color-stellar-dim);
  color: var(--color-stellar-bright);
  border-color: var(--color-stellar-border);
}

.badge--flare,
.badge--amber {
  background: var(--color-flare-dim);
  color: var(--color-flare);
  border-color: var(--color-flare-border);
}

.badge--info {
  background: var(--color-info-dim);
  color: var(--color-info);
  border-color: var(--color-info-border);
}

.badge--neutral {
  background: var(--color-bg-elevated);
  color: var(--color-comet);
  border-color: var(--color-border);
}

/* ── Dot indicator ── */
.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse 2s ease-in-out infinite;
}
</style>

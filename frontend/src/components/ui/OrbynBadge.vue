<template>
  <span class="orbyn-badge" :class="[`badge--${variant}`, `badge--${size}`]">
    <span v-if="dot" class="badge-dot" />
    <slot />
  </span>
</template>

<script setup>
defineProps({
  /** 'orbit' | 'pulsar' | 'nova' | 'stellar' | 'flare' | 'neutral' */
  variant: {
    type: String,
    default: 'orbit',
    validator: v => ['orbit', 'pulsar', 'nova', 'stellar', 'flare', 'neutral'].includes(v),
  },
  /** 'sm' | 'md' */
  size: {
    type: String,
    default: 'sm',
    validator: v => ['sm', 'md'].includes(v),
  },
  /** Show animated dot indicator */
  dot: { type: Boolean, default: false },
})
</script>

<style scoped>
.orbyn-badge {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-family: var(--font-mono);
  font-weight: var(--weight-medium);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  border-radius: var(--radius-full);
  border: 1px solid transparent;
  line-height: 1;
  white-space: nowrap;
}

/* ── Sizes ── */
.badge--sm {
  font-size: var(--text-2xs);
  padding: 3px 8px;
}
.badge--md {
  font-size: var(--text-xs);
  padding: 4px 10px;
}

/* ── Variants ── */
.badge--orbit {
  background: var(--color-orbit-dim);
  color: var(--color-orbit);
  border-color: var(--color-orbit-border);
}
.badge--pulsar {
  background: var(--color-pulsar-dim);
  color: var(--color-pulsar);
  border-color: var(--color-pulsar-border);
}
.badge--nova {
  background: var(--color-nova-dim);
  color: var(--color-nova);
  border-color: var(--color-nova-border);
}
.badge--stellar {
  background: var(--color-stellar-dim);
  color: var(--color-stellar);
  border-color: var(--color-stellar-border);
}
.badge--flare {
  background: var(--color-flare-dim);
  color: var(--color-flare);
  border-color: var(--color-flare-border);
}
.badge--neutral {
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-comet);
  border-color: var(--color-border);
}

/* ── Dot indicator ── */
.badge-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
  animation: orbynPulse 2s ease-in-out infinite;
}
</style>

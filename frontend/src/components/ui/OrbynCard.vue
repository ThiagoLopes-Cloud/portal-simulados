<template>
  <div class="orbyn-card" :class="[`card--${padding}`, accentClass]" :style="accentStyle">
    <div v-if="$slots.header" class="card-header">
      <slot name="header" />
    </div>

    <div class="card-body">
      <slot />
    </div>

    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer" />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /** Padding size: 'sm' | 'md' | 'lg' | 'none' */
  padding: {
    type: String,
    default: 'md',
    validator: v => ['sm', 'md', 'lg', 'none'].includes(v),
  },
  /**
   * Accent color applied as top border gradient.
   * 'orbit' | 'pulsar' | 'nova' | 'stellar' | 'flare' | string (custom CSS)
   */
  accentColor: { type: String, default: '' },
  /** Hover glow effect */
  hoverable: { type: Boolean, default: false },
})

const accentClass = computed(() => props.hoverable ? 'card--hoverable' : '')

const accentGradients = {
  orbit:   'linear-gradient(90deg, var(--color-orbit), var(--color-pulsar))',
  pulsar:  'linear-gradient(90deg, var(--color-pulsar), var(--color-orbit))',
  nova:    'linear-gradient(90deg, var(--color-nova), var(--color-flare))',
  stellar: 'linear-gradient(90deg, var(--color-stellar), var(--color-orbit))',
  flare:   'linear-gradient(90deg, var(--color-flare), var(--color-nova))',
}

const accentStyle = computed(() => {
  if (!props.accentColor) return {}
  const gradient = accentGradients[props.accentColor] || props.accentColor
  return { '--card-accent': gradient }
})
</script>

<style scoped>
.orbyn-card {
  background: var(--color-nebula);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  position: relative;
  overflow: hidden;
  transition: border-color var(--transition-normal), box-shadow var(--transition-normal);
}

/* Accent top bar */
.orbyn-card[style*="--card-accent"]::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--card-accent);
}

/* Hoverable */
.card--hoverable:hover {
  border-color: var(--color-border-hover);
  box-shadow: var(--shadow-md), 0 0 0 1px var(--color-border-hover);
}

/* ── Padding variants ── */
.card--sm  .card-body { padding: var(--space-4); }
.card--md  .card-body { padding: var(--space-5); }
.card--lg  .card-body { padding: var(--space-7); }
.card--none .card-body { padding: 0; }

/* Header / Footer */
.card-header {
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
}
.card-footer {
  padding: var(--space-4) var(--space-5);
  border-top: 1px solid var(--color-border);
}

/* Adjust body padding when header/footer exist */
.card--sm  .card-header,
.card--sm  .card-footer  { padding: var(--space-3) var(--space-4); }
.card--lg  .card-header,
.card--lg  .card-footer  { padding: var(--space-5) var(--space-7); }
</style>

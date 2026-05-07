<template>
  <div class="sl-kpi" :class="`sl-kpi--${accent}`">
    <template v-if="loading">
      <div class="sl-kpi-skeleton-label skel" />
      <div class="sl-kpi-skeleton-value skel" />
      <div class="sl-kpi-skeleton-change skel" />
    </template>

    <template v-else>
      <div class="sl-kpi-header">
        <span class="sl-kpi-label">{{ label }}</span>
        <span v-if="icon" class="sl-kpi-icon" aria-hidden="true">{{ icon }}</span>
      </div>

      <div class="sl-kpi-value">{{ value }}</div>

      <div v-if="change !== undefined" class="sl-kpi-change" :class="`sl-change--${changeDirection}`">
        <span class="sl-change-arrow" aria-hidden="true">{{ changeIcon }}</span>
        <span>{{ Math.abs(change) }}{{ changeUnit }}</span>
        <span v-if="changeSuffix" class="sl-change-suffix">{{ changeSuffix }}</span>
      </div>
      <div v-else class="sl-kpi-spacer" />
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label:        { type: String, required: true },
  value:        { type: [String, Number], default: '—' },
  icon:         { type: String, default: '' },
  loading:      { type: Boolean, default: false },
  change:       { type: Number, default: undefined },
  changeUnit:   { type: String, default: '%' },
  changeSuffix: { type: String, default: '' },
  direction:    { type: String, default: '' },
  accent: {
    type: String,
    default: 'orbit',
    validator: v => ['orbit', 'blue', 'pulsar', 'stellar', 'nova', 'flare'].includes(v),
  },
})

const changeDirection = computed(() => {
  if (props.direction) return props.direction
  if (props.change === undefined) return 'neutral'
  return props.change > 0 ? 'up' : props.change < 0 ? 'down' : 'neutral'
})

const changeIcon = computed(() => ({ up: '↑', down: '↓', neutral: '→' }[changeDirection.value]))
</script>

<style scoped>
.sl-kpi {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
  padding: var(--space-5) var(--space-5) var(--space-4);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: var(--space-1-5);
  transition:
    box-shadow var(--duration-slow) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out),
    transform var(--duration-slow) var(--ease-out);
}

.sl-kpi:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--color-border-hover);
  transform: translateY(-2px);
}

/* ── Accent bar ── */
.sl-kpi::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  border-radius: var(--card-radius) var(--card-radius) 0 0;
}

.sl-kpi--orbit::before,
.sl-kpi--blue::before   { background: linear-gradient(90deg, var(--color-orbit), var(--color-orbit-bright)); }
.sl-kpi--pulsar::before  { background: linear-gradient(90deg, var(--color-pulsar), var(--color-pulsar-bright)); }
.sl-kpi--nova::before    { background: linear-gradient(90deg, var(--color-nova), #FF8099); }
.sl-kpi--stellar::before { background: linear-gradient(90deg, var(--color-stellar), var(--color-stellar-bright)); }
.sl-kpi--flare::before   { background: linear-gradient(90deg, var(--color-flare), #FFD060); }

/* ── Header ── */
.sl-kpi-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: var(--space-1);
}

.sl-kpi-label {
  font-family: var(--font-body);
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-comet);
}

.sl-kpi-icon {
  font-size: var(--text-base);
  opacity: 0.35;
}

/* ── Value ── */
.sl-kpi-value {
  font-family: var(--font-display);
  font-size: var(--text-4xl);
  font-weight: var(--weight-extrabold);
  color: var(--color-star);
  line-height: 1;
  letter-spacing: var(--tracking-tighter);
}

/* ── Change ── */
.sl-kpi-change {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-family: var(--font-body);
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
}

.sl-change--up      { color: var(--color-stellar); }
.sl-change--down    { color: var(--color-nova); }
.sl-change--neutral { color: var(--color-dust); }

.sl-change-arrow  { font-size: var(--text-xs); }
.sl-change-suffix {
  color: var(--color-dust);
  font-size: var(--text-2xs);
  margin-left: var(--space-0-5);
}

.sl-kpi-spacer { height: var(--space-4); }

/* ── Skeletons ── */
.skel {
  border-radius: var(--radius-xs);
  background: var(--color-bg-elevated);
  animation: pulse 1.5s ease-in-out infinite;
}

.sl-kpi-skeleton-label  { height: 10px; width: 45%; margin-top: var(--space-1-5); }
.sl-kpi-skeleton-value  { height: 44px; width: 60%; margin: var(--space-1) 0; }
.sl-kpi-skeleton-change { height: 10px; width: 30%; }
</style>

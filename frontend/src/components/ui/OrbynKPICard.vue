<template>
  <div class="orbyn-kpi" :class="`kpi--${accent}`">
    <!-- Skeleton loading state -->
    <template v-if="loading">
      <div class="kpi-skeleton-value skeleton" />
      <div class="kpi-skeleton-label skeleton" />
    </template>

    <template v-else>
      <div class="kpi-header">
        <span class="kpi-label">{{ label }}</span>
        <span v-if="icon" class="kpi-icon">{{ icon }}</span>
      </div>

      <div class="kpi-value">{{ value }}</div>

      <div v-if="change !== undefined" class="kpi-change" :class="`change--${changeDirection}`">
        <span class="change-icon">{{ changeIcon }}</span>
        <span class="change-text">{{ Math.abs(change) }}{{ changeUnit }}</span>
        <span v-if="changeSuffix" class="change-suffix">{{ changeSuffix }}</span>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  /** Card label / title */
  label:        { type: String, required: true },
  /** Main metric value */
  value:        { type: [String, Number], default: '—' },
  /** Optional icon emoji/char */
  icon:         { type: String, default: '' },
  /** Show skeleton loading */
  loading:      { type: Boolean, default: false },
  /** Change value (positive = up, negative = down) */
  change:       { type: Number, default: undefined },
  /** Unit for change display */
  changeUnit:   { type: String, default: '%' },
  /** Extra text after change value */
  changeSuffix: { type: String, default: '' },
  /** Force direction: 'up' | 'down' | 'neutral' (auto-detected from change) */
  direction:    { type: String, default: '' },
  /** Accent color: 'orbit' | 'pulsar' | 'nova' | 'stellar' | 'flare' */
  accent:       { type: String, default: 'orbit' },
})

const changeDirection = computed(() => {
  if (props.direction) return props.direction
  if (props.change === undefined) return 'neutral'
  if (props.change > 0) return 'up'
  if (props.change < 0) return 'down'
  return 'neutral'
})

const changeIcon = computed(() => {
  if (changeDirection.value === 'up')   return '↑'
  if (changeDirection.value === 'down') return '↓'
  return '→'
})
</script>

<style scoped>
.orbyn-kpi {
  background: var(--color-nebula);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-card);
  padding: var(--space-5);
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  transition: border-color var(--transition-normal), box-shadow var(--transition-normal);
}

/* ── Top accent bar ── */
.orbyn-kpi::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
}
.kpi--orbit::before   { background: linear-gradient(90deg, var(--color-orbit), var(--color-pulsar)); }
.kpi--pulsar::before  { background: linear-gradient(90deg, var(--color-pulsar), var(--color-orbit)); }
.kpi--nova::before    { background: linear-gradient(90deg, var(--color-nova), var(--color-flare)); }
.kpi--stellar::before { background: linear-gradient(90deg, var(--color-stellar), var(--color-orbit)); }
.kpi--flare::before   { background: linear-gradient(90deg, var(--color-flare), var(--color-nova)); }

.orbyn-kpi:hover {
  border-color: var(--color-border-hover);
}

/* ── Header row ── */
.kpi-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.kpi-label {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-comet);
}

.kpi-icon {
  font-size: 1.1rem;
  opacity: 0.7;
}

/* ── Value ── */
.kpi-value {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: var(--weight-extrabold);
  color: var(--color-star);
  line-height: 1;
  letter-spacing: -0.02em;
}

/* ── Change indicator ── */
.kpi-change {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  margin-top: var(--space-1);
}

.change--up      { color: var(--color-stellar); }
.change--down    { color: var(--color-nova); }
.change--neutral { color: var(--color-comet); }

.change-icon { font-weight: var(--weight-bold); }
.change-suffix {
  color: var(--color-dust);
  font-size: var(--text-xs);
  margin-left: var(--space-1);
}

/* ── Skeleton ── */
.kpi-skeleton-value {
  height: 40px;
  width: 70%;
  margin-top: var(--space-3);
}
.kpi-skeleton-label {
  height: 12px;
  width: 45%;
}
</style>

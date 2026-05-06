<template>
  <div class="sl-kpi" :class="`sl-kpi--${accent}`">
    <template v-if="loading">
      <div class="sl-kpi-skeleton-label skeleton-pulse" />
      <div class="sl-kpi-skeleton-value skeleton-pulse" />
      <div class="sl-kpi-skeleton-change skeleton-pulse" />
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
  accent:       { type: String, default: 'blue' },
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
  background: #ffffff;
  border: 1px solid #e8ecf2;
  border-radius: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 4px 16px rgba(0,0,0,0.03);
  padding: 20px 20px 18px;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: 6px;
  transition: box-shadow 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
}

.sl-kpi:hover {
  box-shadow: 0 4px 20px rgba(0,0,0,0.08);
  border-color: #d0d8e8;
  transform: translateY(-1px);
}

/* ── Accent bar ── */
.sl-kpi::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  border-radius: 16px 16px 0 0;
}

.sl-kpi--blue::before,
.sl-kpi--orbit::before   { background: linear-gradient(90deg, #2563eb, #60a5fa); }
.sl-kpi--pulsar::before  { background: linear-gradient(90deg, #7c3aed, #a78bfa); }
.sl-kpi--nova::before    { background: linear-gradient(90deg, #dc2626, #f87171); }
.sl-kpi--stellar::before { background: linear-gradient(90deg, #059669, #34d399); }
.sl-kpi--flare::before   { background: linear-gradient(90deg, #d97706, #fbbf24); }

/* ── Header ── */
.sl-kpi-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: 4px;
}

.sl-kpi-label {
  font-family: var(--font-body);
  font-size: 0.6875rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: #94a3b8;
}

.sl-kpi-icon {
  font-size: 1rem;
  opacity: 0.4;
}

/* ── Value ── */
.sl-kpi-value {
  font-family: var(--font-display);
  font-size: 2.25rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1;
  letter-spacing: -0.03em;
}

/* ── Change ── */
.sl-kpi-change {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-family: var(--font-body);
  font-size: 0.8rem;
  font-weight: 600;
}

.sl-change--up      { color: #059669; }
.sl-change--down    { color: #dc2626; }
.sl-change--neutral { color: #94a3b8; }

.sl-change-arrow { font-size: 0.75rem; }
.sl-change-suffix { color: #94a3b8; font-size: 0.7rem; margin-left: 2px; }

.sl-kpi-spacer { height: 16px; }

/* ── Skeleton ── */
.sl-kpi-skeleton-label {
  height: 10px;
  width: 45%;
  border-radius: 5px;
  background: #f1f5f9;
  margin-top: 6px;
}
.sl-kpi-skeleton-value {
  height: 40px;
  width: 60%;
  border-radius: 8px;
  background: #f1f5f9;
  margin: 4px 0;
}
.sl-kpi-skeleton-change {
  height: 10px;
  width: 30%;
  border-radius: 5px;
  background: #f1f5f9;
}

.skeleton-pulse {
  animation: skeletonPulse 1.5s ease-in-out infinite;
}

@keyframes skeletonPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.45; }
}
</style>

<template>
  <div class="simuslab-kpi" :class="`kpi--${accent}`">
    <template v-if="loading">
      <div class="kpi-skeleton-label skeleton" />
      <div class="kpi-skeleton-value skeleton" />
    </template>

    <template v-else>
      <div class="kpi-header">
        <span class="kpi-label">{{ label }}</span>
        <span v-if="icon" class="kpi-icon">{{ icon }}</span>
      </div>

      <div class="kpi-value">{{ value }}</div>

      <div v-if="change !== undefined" class="kpi-change" :class="`change--${changeDirection}`">
        <span class="change-icon">{{ changeIcon }}</span>
        <span>{{ Math.abs(change) }}{{ changeUnit }}</span>
        <span v-if="changeSuffix" class="change-suffix">{{ changeSuffix }}</span>
      </div>
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
.simuslab-kpi {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.04);
  padding: 20px;
  position: relative;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  gap: 8px;
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

.simuslab-kpi:hover {
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
  border-color: #cbd5e1;
}

/* ── Left accent bar (replaces neon top gradient) ── */
.simuslab-kpi::before {
  content: '';
  position: absolute;
  top: 16px;
  bottom: 16px;
  left: 0;
  width: 3px;
  border-radius: 0 3px 3px 0;
}
.kpi--orbit::before,
.kpi--blue::before   { background: #3b82f6; }
.kpi--pulsar::before { background: #8b5cf6; }
.kpi--nova::before   { background: #ef4444; }
.kpi--stellar::before{ background: #10b981; }
.kpi--flare::before  { background: #f59e0b; }

/* ── Header ── */
.kpi-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.kpi-label {
  font-family: var(--font-body);
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.07em;
  color: #94a3b8;
}

.kpi-icon { font-size: 1rem; opacity: 0.5; }

/* ── Value — tipografia de dados moderna ── */
.kpi-value {
  font-family: var(--font-display);
  font-size: 2.25rem;
  font-weight: 800;
  color: #0f172a;
  line-height: 1;
  letter-spacing: -0.03em;
}

/* ── Change indicator ── */
.kpi-change {
  display: inline-flex;
  align-items: center;
  gap: 3px;
  font-family: var(--font-body);
  font-size: 0.8rem;
  font-weight: 600;
  margin-top: 2px;
}

.change--up      { color: #059669; }
.change--down    { color: #dc2626; }
.change--neutral { color: #94a3b8; }

.change-suffix { color: #94a3b8; font-size: 0.7rem; margin-left: 2px; }

/* ── Skeleton ── */
.kpi-skeleton-value {
  height: 40px;
  width: 65%;
  margin-top: 8px;
  background: #f1f5f9;
  border-radius: 8px;
  animation: shimmer 1.5s infinite;
}
.kpi-skeleton-label {
  height: 10px;
  width: 40%;
  background: #f1f5f9;
  border-radius: 4px;
  animation: shimmer 1.5s infinite;
}
@keyframes shimmer {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.4; }
}
</style>

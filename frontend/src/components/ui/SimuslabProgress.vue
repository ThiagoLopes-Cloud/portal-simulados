<template>
  <div class="sl-progress" :class="[`sl-progress--${size}`, `sl-progress--${color}`]" role="progressbar" :aria-valuenow="clampedValue" aria-valuemin="0" :aria-valuemax="max" :aria-label="label || undefined">
    <div v-if="label || showValue" class="sl-progress-header">
      <span v-if="label" class="sl-progress-label">{{ label }}</span>
      <span v-if="showValue" class="sl-progress-value">{{ clampedValue }}%</span>
    </div>
    <div class="sl-progress-track">
      <div
        class="sl-progress-fill"
        :style="{ width: `${clampedValue}%` }"
      />
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  value:     { type: Number, default: 0 },
  max:       { type: Number, default: 100 },
  color:     { type: String, default: 'orbit', validator: v => ['orbit', 'pulsar', 'stellar', 'nova', 'flare', 'info'].includes(v) },
  size:      { type: String, default: 'md',    validator: v => ['xs', 'sm', 'md', 'lg'].includes(v) },
  label:     { type: String, default: '' },
  showValue: { type: Boolean, default: false },
})

const clampedValue = computed(() => {
  const pct = (props.value / props.max) * 100
  return Math.min(100, Math.max(0, Math.round(pct)))
})
</script>

<style scoped>
.sl-progress { display: flex; flex-direction: column; gap: var(--space-1-5); }

/* ── Header ── */
.sl-progress-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sl-progress-label {
  font-family: var(--font-body);
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  color: var(--color-comet);
}

.sl-progress-value {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  color: var(--color-comet);
}

/* ── Track ── */
.sl-progress-track {
  background: var(--color-bg-elevated);
  border-radius: var(--radius-full);
  overflow: hidden;
}

/* ── Fill ── */
.sl-progress-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width var(--duration-slow) var(--ease-out);
}

/* ── Color variants ── */
.sl-progress--orbit  .sl-progress-fill { background: linear-gradient(90deg, var(--color-orbit), var(--color-orbit-bright)); }
.sl-progress--pulsar .sl-progress-fill { background: linear-gradient(90deg, var(--color-pulsar), var(--color-pulsar-bright)); }
.sl-progress--stellar .sl-progress-fill { background: linear-gradient(90deg, var(--color-stellar), var(--color-stellar-bright)); }
.sl-progress--nova   .sl-progress-fill { background: var(--color-nova); }
.sl-progress--flare  .sl-progress-fill { background: var(--color-flare); }
.sl-progress--info   .sl-progress-fill { background: var(--color-info); }

/* ── Size variants ── */
.sl-progress--xs .sl-progress-track { height: 2px; }
.sl-progress--sm .sl-progress-track { height: 4px; }
.sl-progress--md .sl-progress-track { height: 6px; }
.sl-progress--lg .sl-progress-track { height: 10px; }
</style>

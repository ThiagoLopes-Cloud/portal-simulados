<template>
  <button
    type="button"
    class="sl-option"
    :class="`sl-option--${state}`"
    :aria-pressed="state === 'selected'"
    v-bind="$attrs"
  >
    <span class="sl-option-label" :class="`sl-option-label--${state}`">{{ label }}</span>
    <span class="sl-option-text">{{ text }}</span>
    <span v-if="state === 'correct'" class="sl-option-indicator sl-option-indicator--ok" aria-label="Correta">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
    </span>
    <span v-else-if="state === 'error'" class="sl-option-indicator sl-option-indicator--fail" aria-label="Incorreta">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
    </span>
  </button>
</template>

<script setup>
defineProps({
  label: { type: String, required: true },
  text:  { type: String, required: true },
  state: {
    type: String,
    default: 'default',
    validator: v => ['default', 'selected', 'correct', 'error'].includes(v),
  },
})
</script>

<style scoped>
.sl-option {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  width: 100%;
  min-height: 56px;
  padding: var(--space-4);
  border-radius: var(--radius-md);
  border: 1.5px solid;
  cursor: pointer;
  text-align: left;
  transition: all 0.15s ease;
  font-family: var(--font-body);
  font-size: var(--text-base);
  line-height: var(--leading-snug);
  user-select: none;
}

.sl-option:focus-visible {
  outline: 2px solid var(--color-orbit);
  outline-offset: 2px;
}

.sl-option:disabled {
  opacity: 0.4;
  pointer-events: none;
}

/* ── States ── */
.sl-option--default {
  background: rgba(255, 255, 255, 0.04);
  border-color: var(--color-border);
  color: var(--color-comet);
}
.sl-option--default:hover {
  background: rgba(255, 255, 255, 0.07);
  border-color: var(--color-border-hover);
}

.sl-option--selected {
  background: var(--color-orbit-dim);
  border-color: var(--color-orbit-border);
  color: var(--color-star);
}

.sl-option--correct {
  background: var(--color-stellar-dim);
  border-color: var(--color-stellar-border);
  color: var(--color-star);
}

.sl-option--error {
  background: var(--color-nova-dim);
  border-color: var(--color-nova-border);
  color: var(--color-star);
}

/* ── Label badge ── */
.sl-option-label {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  font-weight: var(--weight-bold);
  font-size: var(--text-xs);
  text-transform: uppercase;
  margin-top: 1px;
  transition: all 0.15s ease;
}

.sl-option-label--default  { background: rgba(255,255,255,0.06); color: var(--color-comet); }
.sl-option-label--selected { background: var(--color-orbit-mid); color: var(--color-orbit); }
.sl-option-label--correct  { background: var(--color-stellar-dim); color: var(--color-stellar); }
.sl-option-label--error    { background: var(--color-nova-dim); color: var(--color-nova); }

/* ── Text ── */
.sl-option-text { flex: 1; }

/* ── Indicator ── */
.sl-option-indicator {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  margin-top: 3px;
}
.sl-option-indicator--ok   { color: var(--color-stellar); }
.sl-option-indicator--fail { color: var(--color-nova); }
</style>

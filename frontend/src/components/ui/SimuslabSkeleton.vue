<template>
  <div
    class="sl-skeleton"
    :class="[`sl-skeleton--${variant}`, { 'sl-skeleton--animated': animated }]"
    :style="computedStyle"
    aria-hidden="true"
  >
    <template v-if="variant === 'text'">
      <div v-for="i in lines" :key="i" class="sl-skeleton-line" :style="lineStyle(i)" />
    </template>
    <template v-else-if="variant === 'card'">
      <div class="sl-skeleton-card-header" />
      <div class="sl-skeleton-card-body">
        <div v-for="i in 3" :key="i" class="sl-skeleton-line" :style="lineStyle(i)" />
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant:  { type: String, default: 'rect', validator: v => ['text', 'rect', 'circle', 'card'].includes(v) },
  width:    { type: String, default: '100%' },
  height:   { type: String, default: '' },
  lines:    { type: Number, default: 3 },
  animated: { type: Boolean, default: true },
})

const defaultHeights = { text: 'auto', rect: '20px', circle: '40px', card: '120px' }

const computedStyle = computed(() => ({
  width:  props.width,
  height: props.height || defaultHeights[props.variant],
  borderRadius: props.variant === 'circle' ? '50%' : undefined,
}))

function lineStyle(i) {
  const widths = ['100%', '85%', '65%', '90%', '50%']
  return { width: widths[(i - 1) % widths.length] }
}
</script>

<style scoped>
.sl-skeleton {
  background: var(--color-bg-elevated);
  border-radius: var(--radius-sm);
  overflow: hidden;
  position: relative;
}

.sl-skeleton--animated::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.04) 50%, transparent 100%);
  animation: shimmer 1.6s ease-in-out infinite;
}

/* ── Text lines ── */
.sl-skeleton--text {
  background: transparent;
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  height: auto;
}
.sl-skeleton--text::after { display: none; }

.sl-skeleton-line {
  height: 12px;
  background: var(--color-bg-elevated);
  border-radius: var(--radius-xs);
  position: relative;
  overflow: hidden;
}
.sl-skeleton-line::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent 0%, rgba(255, 255, 255, 0.04) 50%, transparent 100%);
  animation: shimmer 1.6s ease-in-out infinite;
}

/* ── Card ── */
.sl-skeleton--card {
  height: auto;
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  padding: 0;
}
.sl-skeleton--card::after { display: none; }

.sl-skeleton-card-header {
  height: 48px;
  background: var(--color-bg-elevated);
  border-radius: var(--card-radius) var(--card-radius) 0 0;
  position: relative;
  overflow: hidden;
}
.sl-skeleton-card-header::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent);
  animation: shimmer 1.6s infinite;
}

.sl-skeleton-card-body {
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}
</style>

<template>
  <div class="simuslab-card" :class="[`card--${padding}`, { 'card--hoverable': hoverable }]">
    <div v-if="accentColor" class="card-accent-bar" :class="`accent--${accentColor}`" />

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
defineProps({
  padding:     { type: String, default: 'md', validator: v => ['sm', 'md', 'lg', 'none'].includes(v) },
  accentColor: { type: String, default: '' },
  hoverable:   { type: Boolean, default: false },
})
</script>

<style scoped>
.simuslab-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
  position: relative;
  overflow: hidden;
  transition:
    box-shadow var(--duration-slow) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out),
    transform var(--duration-slow) var(--ease-out);
}

.card--hoverable:hover {
  box-shadow: var(--shadow-lg);
  border-color: var(--color-border-hover);
  transform: translateY(-3px);
}

/* ── Top accent bar ── */
.card-accent-bar {
  height: 3px;
  width: 100%;
}
.accent--orbit   { background: var(--color-orbit); }
.accent--pulsar  { background: var(--color-pulsar); }
.accent--nova    { background: var(--color-nova); }
.accent--stellar { background: var(--color-stellar); }
.accent--flare   { background: var(--color-flare); }

/* ── Padding variants ── */
.card--sm   .card-body { padding: var(--space-4); }
.card--md   .card-body { padding: var(--space-5); }
.card--lg   .card-body { padding: var(--space-7); }
.card--none .card-body { padding: 0; }

/* ── Header / Footer ── */
.card-header {
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
}
.card-footer {
  padding: var(--space-4) var(--space-5);
  border-top: 1px solid var(--color-border);
}
</style>

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
  padding:    { type: String, default: 'md', validator: v => ['sm', 'md', 'lg', 'none'].includes(v) },
  accentColor:{ type: String, default: '' },
  hoverable:  { type: Boolean, default: false },
})
</script>

<style scoped>
.simuslab-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.04);
  position: relative;
  overflow: hidden;
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
}

.card--hoverable:hover {
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.08);
  border-color: #cbd5e1;
}

/* ── Top accent bar (solid, not gradient) ── */
.card-accent-bar {
  height: 3px;
  width: 100%;
}
.accent--orbit   { background: #3b82f6; }
.accent--pulsar  { background: #8b5cf6; }
.accent--nova    { background: #ef4444; }
.accent--stellar { background: #10b981; }
.accent--flare   { background: #f59e0b; }

/* ── Padding variants ── */
.card--sm  .card-body { padding: 16px; }
.card--md  .card-body { padding: 20px; }
.card--lg  .card-body { padding: 28px; }
.card--none .card-body { padding: 0; }

/* ── Header / Footer ── */
.card-header {
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
}
.card-footer {
  padding: 16px 20px;
  border-top: 1px solid #f1f5f9;
}
</style>

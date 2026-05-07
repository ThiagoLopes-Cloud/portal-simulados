<template>
  <div class="sl-tabs" :class="`sl-tabs--${variant}`" role="tablist">
    <button
      v-for="tab in tabs"
      :key="tab.id"
      class="sl-tab"
      :class="{
        'sl-tab--active': modelValue === tab.id,
        [`sl-tab--${tab.color || activeColor}`]: modelValue === tab.id,
      }"
      role="tab"
      :aria-selected="modelValue === tab.id"
      :aria-controls="`tabpanel-${tab.id}`"
      :disabled="tab.disabled"
      @click="!tab.disabled && $emit('update:modelValue', tab.id)"
    >
      <span v-if="tab.icon" class="sl-tab-icon" v-html="tab.icon" />
      <span class="sl-tab-label">{{ tab.label }}</span>
      <span v-if="tab.badge" class="sl-tab-badge" :class="`sl-tab-badge--${tab.color || activeColor}`">
        {{ tab.badge }}
      </span>
    </button>
  </div>
</template>

<script setup>
defineProps({
  modelValue:  { type: String, required: true },
  tabs:        { type: Array,  required: true },
  variant:     { type: String, default: 'underline', validator: v => ['underline', 'pill', 'segment'].includes(v) },
  activeColor: { type: String, default: 'orbit' },
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
/* ── Base ── */
.sl-tabs {
  display: flex;
  gap: var(--space-1);
}

.sl-tab {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1-5);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-dust);
  cursor: pointer;
  transition:
    color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out);
  white-space: nowrap;
  background: none;
  border: none;
}

.sl-tab:disabled { opacity: 0.4; cursor: not-allowed; }
.sl-tab:focus-visible { outline: none; box-shadow: var(--shadow-focus); border-radius: var(--radius-sm); }

.sl-tab-icon { display: flex; align-items: center; flex-shrink: 0; }

/* ── Underline variant ── */
.sl-tabs--underline {
  border-bottom: 1px solid var(--color-border);
}

.sl-tabs--underline .sl-tab {
  padding: var(--space-2-5) var(--space-4);
  border-bottom: 2px solid transparent;
  margin-bottom: -1px;
}

.sl-tabs--underline .sl-tab:hover:not(:disabled) {
  color: var(--color-comet);
}

.sl-tabs--underline .sl-tab--active.sl-tab--orbit   { color: var(--color-orbit);   border-bottom-color: var(--color-orbit); }
.sl-tabs--underline .sl-tab--active.sl-tab--pulsar  { color: var(--color-pulsar);  border-bottom-color: var(--color-pulsar); }
.sl-tabs--underline .sl-tab--active.sl-tab--stellar { color: var(--color-stellar); border-bottom-color: var(--color-stellar); }
.sl-tabs--underline .sl-tab--active.sl-tab--nova    { color: var(--color-nova);    border-bottom-color: var(--color-nova); }
.sl-tabs--underline .sl-tab--active.sl-tab--flare   { color: var(--color-flare);   border-bottom-color: var(--color-flare); }

/* ── Pill variant ── */
.sl-tabs--pill {
  background: var(--color-bg-elevated);
  border-radius: var(--radius-full);
  padding: var(--space-1);
  gap: var(--space-0-5);
}

.sl-tabs--pill .sl-tab {
  padding: var(--space-1-5) var(--space-4);
  border-radius: var(--radius-full);
}

.sl-tabs--pill .sl-tab:hover:not(:disabled):not(.sl-tab--active) {
  color: var(--color-comet);
  background: var(--color-surface-hover);
}

.sl-tabs--pill .sl-tab--active.sl-tab--orbit   { background: var(--color-orbit-dim);   color: var(--color-orbit);   border: 1px solid var(--color-orbit-border); }
.sl-tabs--pill .sl-tab--active.sl-tab--pulsar  { background: var(--color-pulsar-dim);  color: var(--color-pulsar);  border: 1px solid var(--color-pulsar-border); }
.sl-tabs--pill .sl-tab--active.sl-tab--stellar { background: var(--color-stellar-dim); color: var(--color-stellar); border: 1px solid var(--color-stellar-border); }

/* ── Segment variant ── */
.sl-tabs--segment {
  background: var(--color-bg-elevated);
  border-radius: var(--radius-md);
  padding: var(--space-1);
  gap: var(--space-0-5);
}

.sl-tabs--segment .sl-tab {
  flex: 1;
  justify-content: center;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
}

.sl-tabs--segment .sl-tab--active {
  background: var(--color-bg-surface);
  color: var(--color-star);
  box-shadow: var(--shadow-xs);
}

/* ── Badge ── */
.sl-tab-badge {
  padding: 1px var(--space-1-5);
  border-radius: var(--radius-full);
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  line-height: 1.4;
}

.sl-tab-badge--orbit   { background: var(--color-orbit);   color: var(--color-cosmos); }
.sl-tab-badge--pulsar  { background: var(--color-pulsar);  color: var(--color-cosmos); }
.sl-tab-badge--stellar { background: var(--color-stellar); color: var(--color-cosmos); }
.sl-tab-badge--nova    { background: var(--color-nova);    color: #fff; }
.sl-tab-badge--flare   { background: var(--color-flare);   color: var(--color-cosmos); }
</style>

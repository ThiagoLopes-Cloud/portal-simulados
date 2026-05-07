<template>
  <div class="sl-select-wrap" :class="{ 'sl-select-wrap--error': error, 'sl-select-wrap--disabled': disabled }">
    <select
      :id="id"
      class="sl-select"
      :value="modelValue"
      :disabled="disabled"
      :aria-describedby="error ? `${id}-error` : undefined"
      :aria-invalid="error ? 'true' : undefined"
      v-bind="$attrs"
      @change="$emit('update:modelValue', ($event.target as HTMLSelectElement).value)"
    >
      <option v-if="placeholder" value="" disabled :selected="!modelValue">{{ placeholder }}</option>
      <option
        v-for="opt in options"
        :key="opt.value"
        :value="opt.value"
        :disabled="opt.disabled"
      >{{ opt.label }}</option>
    </select>
    <span class="sl-select-chevron" aria-hidden="true">
      <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
    </span>
  </div>
  <p v-if="error" :id="`${id}-error`" class="sl-select-error" role="alert">{{ error }}</p>
</template>

<script setup>
defineOptions({ inheritAttrs: false })

defineProps({
  modelValue:  { type: String, default: '' },
  options:     { type: Array, default: () => [] },
  placeholder: { type: String, default: '' },
  disabled:    { type: Boolean, default: false },
  error:       { type: String, default: '' },
  id:          { type: String, default: () => `sl-select-${Math.random().toString(36).slice(2, 7)}` },
})

defineEmits(['update:modelValue'])
</script>

<style scoped>
.sl-select-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.sl-select {
  width: 100%;
  appearance: none;
  -webkit-appearance: none;
  background: var(--input-bg);
  border: 1px solid var(--input-border);
  border-radius: var(--input-radius);
  color: var(--color-star);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  height: var(--btn-height-md);
  padding: 0 var(--space-9) 0 var(--space-3);
  cursor: pointer;
  transition:
    border-color var(--duration-fast) var(--ease-out),
    box-shadow var(--duration-normal) var(--ease-out);
  outline: none;
}

.sl-select:focus {
  border-color: var(--color-orbit);
  box-shadow: var(--shadow-focus);
}

.sl-select option {
  background: var(--color-bg-surface);
  color: var(--color-star);
}

.sl-select-chevron {
  position: absolute;
  right: var(--space-3);
  color: var(--color-dust);
  pointer-events: none;
  display: flex;
  align-items: center;
  transition: color var(--duration-fast) var(--ease-out);
}

.sl-select-wrap:focus-within .sl-select-chevron { color: var(--color-orbit); }

/* ── Error ── */
.sl-select-wrap--error .sl-select {
  border-color: var(--color-nova);
}
.sl-select-wrap--error .sl-select:focus {
  box-shadow: 0 0 0 3px var(--color-nova-glow);
}

.sl-select-error {
  font-size: var(--text-xs);
  color: var(--color-nova);
  margin-top: var(--space-1);
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

/* ── Disabled ── */
.sl-select-wrap--disabled .sl-select {
  opacity: 0.45;
  cursor: not-allowed;
}
</style>

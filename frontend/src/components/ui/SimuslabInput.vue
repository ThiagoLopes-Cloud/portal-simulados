<template>
  <div class="simuslab-field" :class="{ 'field--error': error, 'field--disabled': disabled }">
    <label v-if="label" :for="inputId" class="field-label">
      {{ label }}
      <span v-if="required" class="field-required" aria-hidden="true">*</span>
    </label>

    <div class="field-wrapper" :class="wrapperClasses">
      <span v-if="$slots.prefix" class="field-affix field-affix--left">
        <slot name="prefix" />
      </span>

      <input
        :id="inputId"
        v-bind="$attrs"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :required="required"
        :aria-invalid="!!error"
        :aria-describedby="error ? `${inputId}-error` : hint ? `${inputId}-hint` : undefined"
        class="field-input"
        @input="$emit('update:modelValue', $event.target.value)"
        @focus="focused = true"
        @blur="focused = false"
      />

      <span v-if="$slots.suffix" class="field-affix field-affix--right">
        <slot name="suffix" />
      </span>
    </div>

    <p v-if="error" :id="`${inputId}-error`" class="field-hint field-hint--error" role="alert">
      {{ error }}
    </p>
    <p v-else-if="hint" :id="`${inputId}-hint`" class="field-hint">{{ hint }}</p>
  </div>
</template>

<script setup>
import { ref, computed, useId } from 'vue'

const props = defineProps({
  modelValue:  { type: [String, Number], default: '' },
  label:       { type: String, default: '' },
  type:        { type: String, default: 'text' },
  placeholder: { type: String, default: '' },
  error:       { type: String, default: '' },
  hint:        { type: String, default: '' },
  disabled:    { type: Boolean, default: false },
  required:    { type: Boolean, default: false },
})

defineEmits(['update:modelValue'])
defineOptions({ inheritAttrs: false })

const focused = ref(false)
const inputId = useId ? useId() : `simuslab-input-${Math.random().toString(36).slice(2)}`

const wrapperClasses = computed(() => ({
  'wrapper--focused':  focused.value,
  'wrapper--error':    !!props.error,
  'wrapper--disabled': props.disabled,
}))
</script>

<style scoped>
.simuslab-field {
  display: flex;
  flex-direction: column;
  gap: var(--space-1-5);
}

/* ── Label ── */
.field-label {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  color: var(--color-comet);
}

.field-required {
  color: var(--color-nova);
  font-size: var(--text-sm);
}

/* ── Input wrapper ── */
.field-wrapper {
  display: flex;
  align-items: center;
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--input-radius);
  transition:
    border-color var(--duration-fast) var(--ease-out),
    box-shadow var(--duration-normal) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out);
}

.field-wrapper:hover:not(.wrapper--disabled):not(.wrapper--focused) {
  border-color: var(--color-border-hover);
  background: var(--color-bg-elevated);
}

.wrapper--focused {
  border-color: var(--color-border-focus);
  box-shadow: var(--shadow-focus);
  background: var(--color-bg-elevated);
}

.wrapper--error {
  border-color: var(--color-nova);
  box-shadow: 0 0 0 3px var(--color-nova-dim);
}

.wrapper--disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

/* ── Input element ── */
.field-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  padding: var(--space-2-5) var(--space-3);
  color: var(--color-star);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  line-height: var(--leading-normal);
  min-width: 0;
}

.field-input::placeholder { color: var(--color-dust); }
.field-input:disabled { cursor: not-allowed; }

/* ── Affixes ── */
.field-affix {
  display: flex;
  align-items: center;
  color: var(--color-dust);
  flex-shrink: 0;
}
.field-affix--left  { padding-left: var(--space-3); }
.field-affix--right { padding-right: var(--space-3); }

/* ── Hint / Error ── */
.field-hint {
  font-size: var(--text-xs);
  color: var(--color-dust);
  line-height: var(--leading-normal);
}
.field-hint--error { color: var(--color-nova); }
</style>

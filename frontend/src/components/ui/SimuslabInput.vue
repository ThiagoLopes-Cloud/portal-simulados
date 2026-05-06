<template>
  <div class="simuslab-field" :class="{ 'field--error': error, 'field--disabled': disabled }">
    <label v-if="label" :for="inputId" class="field-label">{{ label }}</label>

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
        class="field-input"
        @input="$emit('update:modelValue', $event.target.value)"
        @focus="focused = true"
        @blur="focused = false"
      />

      <span v-if="$slots.suffix" class="field-affix field-affix--right">
        <slot name="suffix" />
      </span>
    </div>

    <p v-if="error" class="field-hint field-hint--error">{{ error }}</p>
    <p v-else-if="hint" class="field-hint">{{ hint }}</p>
  </div>
</template>

<script setup>
import { ref, computed, useId } from 'vue'

const props = defineProps({
  /** v-model binding */
  modelValue: { type: [String, Number], default: '' },
  /** Label text above input */
  label:       { type: String, default: '' },
  /** Input type */
  type:        { type: String, default: 'text' },
  /** Placeholder text */
  placeholder: { type: String, default: '' },
  /** Error message (activates error state) */
  error:       { type: String, default: '' },
  /** Helper text below input */
  hint:        { type: String, default: '' },
  /** Disabled state */
  disabled:    { type: Boolean, default: false },
  /** Required field */
  required:    { type: Boolean, default: false },
})

defineEmits(['update:modelValue'])
defineOptions({ inheritAttrs: false })

const focused = ref(false)
const inputId = useId ? useId() : `simuslab-input-${Math.random().toString(36).slice(2)}`

const wrapperClasses = computed(() => ({
  'wrapper--focused': focused.value,
  'wrapper--error':   !!props.error,
  'wrapper--disabled': props.disabled,
}))
</script>

<style scoped>
.simuslab-field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

/* ── Label ── */
.field-label {
  font-family: var(--font-body);
  font-size: 0.875rem;
  font-weight: 500;
  color: #374151;
}

/* ── Input wrapper ── */
.field-wrapper {
  display: flex;
  align-items: center;
  background: #ffffff;
  border: 1px solid #cbd5e1;
  border-radius: 10px;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}

.wrapper--focused {
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15);
}

.wrapper--error {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.12);
}

.wrapper--disabled { opacity: 0.5; cursor: not-allowed; }

/* ── Input element ── */
.field-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  padding: 10px 14px;
  color: #0f172a;
  font-family: var(--font-body);
  font-size: 0.9375rem;
  line-height: 1.5;
  min-width: 0;
}

.field-input::placeholder { color: #94a3b8; }
.field-input:disabled { cursor: not-allowed; }

/* ── Affixes ── */
.field-affix {
  display: flex;
  align-items: center;
  color: #94a3b8;
  flex-shrink: 0;
}
.field-affix--left  { padding-left: 12px; }
.field-affix--right { padding-right: 12px; }

/* ── Hint / Error text ── */
.field-hint {
  font-size: 0.8125rem;
  color: #64748b;
  line-height: 1.4;
}
.field-hint--error { color: #dc2626; }
</style>

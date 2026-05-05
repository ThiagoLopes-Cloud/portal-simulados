<template>
  <div class="orbyn-field" :class="{ 'field--error': error, 'field--disabled': disabled }">
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
const inputId = useId ? useId() : `orbyn-input-${Math.random().toString(36).slice(2)}`

const wrapperClasses = computed(() => ({
  'wrapper--focused': focused.value,
  'wrapper--error':   !!props.error,
  'wrapper--disabled': props.disabled,
}))
</script>

<style scoped>
.orbyn-field {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

/* ── Label ── */
.field-label {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-comet);
}

/* ── Input wrapper ── */
.field-wrapper {
  display: flex;
  align-items: center;
  background: var(--color-void);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  transition: border-color var(--transition-normal), box-shadow var(--transition-normal);
}

.wrapper--focused {
  border-color: var(--color-orbit-border);
  box-shadow: 0 0 0 3px var(--color-orbit-dim);
}

.wrapper--error {
  border-color: var(--color-nova-border);
  box-shadow: 0 0 0 3px var(--color-nova-dim);
}

.wrapper--disabled { opacity: 0.5; cursor: not-allowed; }

/* ── Input element ── */
.field-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  padding: var(--space-3) var(--space-4);
  color: var(--color-star);
  font-family: var(--font-body);
  font-size: var(--text-base);
  line-height: var(--leading-normal);
  min-width: 0;
}

.field-input::placeholder { color: var(--color-dust); }
.field-input:disabled { cursor: not-allowed; }

/* ── Affixes ── */
.field-affix {
  display: flex;
  align-items: center;
  color: var(--color-comet);
  flex-shrink: 0;
}
.field-affix--left  { padding-left: var(--space-3); }
.field-affix--right { padding-right: var(--space-3); }

/* ── Hint / Error text ── */
.field-hint {
  font-size: var(--text-sm);
  color: var(--color-comet);
  line-height: var(--leading-normal);
}
.field-hint--error { color: var(--color-nova); }
</style>

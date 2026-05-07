<template>
  <div class="sl-field" :class="{ 'sl-field--error': error, 'sl-field--success': success, 'sl-field--disabled': disabled }">
    <label v-if="label" :for="inputId" class="sl-field-label">
      {{ label }}
      <span v-if="required" class="sl-field-required" aria-hidden="true">*</span>
    </label>

    <div class="sl-field-control">
      <slot :id="inputId" :aria-invalid="!!error" :aria-describedby="helpId" />

      <div v-if="$slots.suffix" class="sl-field-suffix">
        <slot name="suffix" />
      </div>
    </div>

    <Transition name="msg">
      <p v-if="error" :id="`${inputId}-msg`" class="sl-field-msg sl-field-msg--error" role="alert">
        <svg width="12" height="12" viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.5"/>
          <path d="M8 5v3.5M8 10.5v.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
        </svg>
        {{ error }}
      </p>
      <p v-else-if="hint" :id="`${inputId}-msg`" class="sl-field-msg sl-field-msg--hint">
        {{ hint }}
      </p>
    </Transition>
  </div>
</template>

<script setup>
defineProps({
  label:    { type: String, default: '' },
  error:    { type: String, default: '' },
  hint:     { type: String, default: '' },
  success:  { type: Boolean, default: false },
  required: { type: Boolean, default: false },
  disabled: { type: Boolean, default: false },
  inputId:  { type: String, default: () => `sl-field-${Math.random().toString(36).slice(2, 7)}` },
})

const helpId = (id) => `${id}-msg`
</script>

<style scoped>
.sl-field {
  display: flex;
  flex-direction: column;
  gap: var(--space-1-5);
}

/* ── Label ── */
.sl-field-label {
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  color: var(--color-comet);
  display: flex;
  align-items: center;
  gap: var(--space-1);
}

.sl-field-required { color: var(--color-nova); font-size: var(--text-xs); }

/* ── Control ── */
.sl-field-control {
  position: relative;
  display: flex;
  align-items: center;
}

.sl-field-suffix {
  position: absolute;
  right: var(--space-3);
  display: flex;
  align-items: center;
  color: var(--color-dust);
  pointer-events: none;
}

/* ── Message ── */
.sl-field-msg {
  display: flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--text-xs);
  line-height: var(--leading-normal);
}

.sl-field-msg--error { color: var(--color-nova); }
.sl-field-msg--hint  { color: var(--color-dust); }

/* ── Error state: style slotted input ── */
.sl-field--error :deep(input),
.sl-field--error :deep(select),
.sl-field--error :deep(textarea) {
  border-color: var(--color-nova) !important;
}

.sl-field--error :deep(input:focus),
.sl-field--error :deep(select:focus) {
  box-shadow: 0 0 0 3px var(--color-nova-glow) !important;
}

/* ── Success state ── */
.sl-field--success :deep(input),
.sl-field--success :deep(select),
.sl-field--success :deep(textarea) {
  border-color: var(--color-stellar) !important;
}

/* ── Disabled ── */
.sl-field--disabled .sl-field-label { opacity: 0.5; }

/* ── Transition ── */
.msg-enter-active { transition: opacity var(--duration-fast) var(--ease-out), transform var(--duration-fast) var(--ease-out); }
.msg-leave-active { transition: opacity var(--duration-fast) var(--ease-in); }
.msg-enter-from   { opacity: 0; transform: translateY(-4px); }
.msg-leave-to     { opacity: 0; }
</style>

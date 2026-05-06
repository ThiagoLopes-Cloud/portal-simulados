<template>
  <button
    type="button"
    :class="classes"
    :aria-pressed="state === 'selected'"
    v-bind="$attrs"
  >
    <span :class="labelClasses">{{ label }}</span>
    <span class="flex-1 text-left text-sm leading-snug">{{ text }}</span>
    <span v-if="state === 'correct'" class="shrink-0 text-emerald-600">✓</span>
    <span v-else-if="state === 'error'" class="shrink-0 text-red-500">✗</span>
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: { type: String, required: true },
  text:  { type: String, required: true },
  state: {
    type: String,
    default: 'default',
    validator: (v) => ['default', 'selected', 'correct', 'error'].includes(v),
  },
})

const base =
  'flex items-start gap-3 w-full min-h-[56px] p-4 ' +
  'rounded-simus-sm border transition-all duration-150 ease-out ' +
  'font-body text-simus-text cursor-pointer select-none ' +
  'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-simus-primary/50 ' +
  'disabled:opacity-40 disabled:pointer-events-none'

const stateClasses = {
  default:  'bg-white border-slate-200 active:bg-slate-50',
  selected: 'bg-indigo-50 border-2 border-simus-primary',
  correct:  'bg-emerald-50 border border-emerald-500',
  error:    'bg-red-50 border border-red-400',
}

const labelBase =
  'shrink-0 w-8 h-8 flex items-center justify-center ' +
  'rounded-lg text-xs font-display font-bold uppercase mt-0.5'

const labelState = {
  default:  'bg-slate-100 text-simus-muted',
  selected: 'bg-indigo-100 text-simus-primary',
  correct:  'bg-emerald-100 text-emerald-700',
  error:    'bg-red-100 text-red-600',
}

const classes      = computed(() => `${base} ${stateClasses[props.state]}`)
const labelClasses = computed(() => `${labelBase} ${labelState[props.state]}`)
</script>

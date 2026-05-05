<template>
  <button
    type="button"
    :class="classes"
    :aria-pressed="state === 'selected'"
    v-bind="$attrs"
  >
    <!-- Label (A, B, C…) -->
    <span :class="labelClasses">{{ label }}</span>

    <!-- Texto da alternativa -->
    <span class="flex-1 text-left text-sm leading-snug">{{ text }}</span>

    <!-- Ícone de estado -->
    <span v-if="state === 'correct'" class="shrink-0 text-emerald-400">✓</span>
    <span v-else-if="state === 'error'" class="shrink-0 text-red-400">✗</span>
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
  'flex items-center gap-4 w-full min-h-[56px] px-4 py-3 ' +
  'rounded-xl border transition-all duration-150 ease-out ' +
  'font-body text-slate-50 cursor-pointer ' +
  'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-simus-cyan/60 ' +
  'disabled:opacity-40 disabled:pointer-events-none'

const stateClasses = {
  default:  'border-white/10 bg-white/5 hover:border-white/20 hover:bg-white/10',
  selected: 'border-2 border-simus-cyan bg-simus-cyan/5',
  correct:  'border-emerald-500 bg-emerald-500/10',
  error:    'border-red-500 bg-red-500/10',
}

const labelBase =
  'shrink-0 w-8 h-8 flex items-center justify-center ' +
  'rounded-lg text-xs font-display font-bold uppercase'

const labelState = {
  default:  'bg-white/10 text-slate-300',
  selected: 'bg-simus-cyan/20 text-simus-cyan',
  correct:  'bg-emerald-500/20 text-emerald-400',
  error:    'bg-red-500/20 text-red-400',
}

const classes     = computed(() => `${base} ${stateClasses[props.state]}`)
const labelClasses = computed(() => `${labelBase} ${labelState[props.state]}`)
</script>

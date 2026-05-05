<template>
  <button :class="classes" v-bind="$attrs">
    <slot />
  </button>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  variant: {
    type: String,
    default: 'primary',
    validator: (v) => ['primary', 'secondary', 'ghost'].includes(v),
  },
})

const base =
  'inline-flex items-center justify-center gap-2 px-6 py-3 ' +
  'font-display font-semibold text-sm uppercase tracking-widest ' +
  'rounded-lg transition-all duration-200 ease-out ' +
  'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-simus-cyan/60 ' +
  'disabled:opacity-40 disabled:pointer-events-none'

const variants = {
  primary:
    'bg-simus-cyan text-simus-bg ' +
    'hover:scale-105 hover:shadow-[0_0_15px_rgba(0,229,255,0.3)]',
  secondary:
    'bg-transparent border border-simus-cyan text-simus-cyan ' +
    'hover:bg-simus-cyan/10',
  ghost:
    'bg-transparent text-slate-400 ' +
    'hover:text-slate-50 hover:bg-white/5',
}

const classes = computed(() => `${base} ${variants[props.variant]}`)
</script>

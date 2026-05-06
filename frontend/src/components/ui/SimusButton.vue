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
  'w-full md:w-auto inline-flex items-center justify-center gap-2 ' +
  'min-h-[48px] px-6 py-3 ' +
  'font-display font-semibold text-sm ' +
  'rounded-simus-sm transition-all duration-200 ease-out select-none ' +
  'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-simus-primary/50 ' +
  'active:scale-[0.98] ' +
  'disabled:opacity-40 disabled:pointer-events-none'

const variants = {
  primary:
    'bg-simus-primary text-white ' +
    'md:hover:scale-[1.02] md:hover:shadow-[0_4px_14px_0_rgba(79,70,229,0.39)]',
  secondary:
    'bg-simus-surface text-simus-text border border-slate-200 ' +
    'md:hover:bg-slate-50',
  ghost:
    'bg-transparent text-simus-muted ' +
    'md:hover:text-simus-text md:hover:bg-slate-100',
}

const classes = computed(() => `${base} ${variants[props.variant]}`)
</script>

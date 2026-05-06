<template>
  <svg
    :width="size"
    :height="size"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    :stroke-width="strokeWidth"
    stroke-linecap="round"
    stroke-linejoin="round"
    :aria-hidden="!label"
    :aria-label="label"
    v-html="path"
  />
</template>

<script setup>
import { computed } from 'vue'
import { icons } from '../../utils/icons.js'

const props = defineProps({
  name:        { type: String, required: true },
  size:        { type: [String, Number], default: 16 },
  strokeWidth: { type: [String, Number], default: 1.75 },
  label:       { type: String, default: '' },
})

const path = computed(() => icons[props.name] ?? '')
</script>

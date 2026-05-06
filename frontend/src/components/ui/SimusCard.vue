<template>
  <div
    :class="['w-full bg-simus-surface rounded-simus border border-slate-100 shadow-simus-soft flex flex-col p-4 md:p-6', $attrs.class]"
    v-bind="{ ...$attrs, class: undefined }"
  >
    <slot />
  </div>
</template>

<script setup>
defineOptions({ inheritAttrs: false })
</script>

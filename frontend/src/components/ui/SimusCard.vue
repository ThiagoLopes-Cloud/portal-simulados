<template>
  <div :class="['bg-simus-surface border border-white/5 rounded-simus p-6', $attrs.class]"
       v-bind="{ ...$attrs, class: undefined }">
    <slot />
  </div>
</template>

<script setup>
defineOptions({ inheritAttrs: false })
</script>

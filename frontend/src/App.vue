<template>
  <router-view v-slot="{ Component, route }">
    <Transition :name="route.meta.transition || 'page'" mode="out-in">
      <component :is="Component" :key="route.path" />
    </Transition>
  </router-view>
</template>

<script setup>
</script>

<style>
*, *::before, *::after {
  box-sizing: border-box;
}

html {
  overflow-x: hidden;
  -webkit-text-size-adjust: 100%;
  touch-action: manipulation;
}

/* ── Page transitions ── */
.page-enter-active {
  animation: pageEnter var(--duration-normal) var(--ease-out) both;
}
.page-leave-active {
  animation: pageLeave var(--duration-fast) var(--ease-in) both;
}

@keyframes pageEnter {
  from { opacity: 0; transform: translateY(10px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes pageLeave {
  from { opacity: 1; transform: translateY(0); }
  to   { opacity: 0; transform: translateY(-6px); }
}

/* ── Fade transition (auth pages) ── */
.fade-enter-active,
.fade-leave-active {
  transition: opacity var(--duration-normal) var(--ease-out);
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

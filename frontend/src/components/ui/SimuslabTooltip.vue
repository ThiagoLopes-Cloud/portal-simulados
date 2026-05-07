<template>
  <div class="sl-tooltip-root" @mouseenter="show = true" @mouseleave="show = false" @focusin="show = true" @focusout="show = false">
    <slot />
    <Transition name="tt">
      <div
        v-if="show && content"
        class="sl-tooltip"
        :class="`sl-tooltip--${placement}`"
        role="tooltip"
      >
        {{ content }}
        <div class="sl-tooltip-arrow" />
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from 'vue'

defineProps({
  content:   { type: String, default: '' },
  placement: { type: String, default: 'top', validator: v => ['top', 'bottom', 'left', 'right'].includes(v) },
})

const show = ref(false)
</script>

<style scoped>
.sl-tooltip-root {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.sl-tooltip {
  position: absolute;
  z-index: var(--z-tooltip);
  background: var(--color-horizon);
  color: var(--color-star);
  font-family: var(--font-body);
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  line-height: var(--leading-snug);
  padding: var(--space-1-5) var(--space-3);
  border-radius: var(--radius-sm);
  border: 1px solid var(--color-border-hover);
  box-shadow: var(--shadow-md);
  white-space: nowrap;
  pointer-events: none;
  max-width: 240px;
  text-align: center;
}

/* ── Placement ── */
.sl-tooltip--top {
  bottom: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
}
.sl-tooltip--bottom {
  top: calc(100% + 8px);
  left: 50%;
  transform: translateX(-50%);
}
.sl-tooltip--left {
  right: calc(100% + 8px);
  top: 50%;
  transform: translateY(-50%);
}
.sl-tooltip--right {
  left: calc(100% + 8px);
  top: 50%;
  transform: translateY(-50%);
}

/* ── Arrow ── */
.sl-tooltip-arrow {
  position: absolute;
  width: 6px;
  height: 6px;
  background: var(--color-horizon);
  border: 1px solid var(--color-border-hover);
  transform: rotate(45deg);
}

.sl-tooltip--top    .sl-tooltip-arrow { bottom: -4px; left: 50%; margin-left: -3px; border-top: none; border-left: none; }
.sl-tooltip--bottom .sl-tooltip-arrow { top: -4px;    left: 50%; margin-left: -3px; border-bottom: none; border-right: none; }
.sl-tooltip--left   .sl-tooltip-arrow { right: -4px;  top: 50%;  margin-top: -3px;  border-bottom: none; border-left: none; }
.sl-tooltip--right  .sl-tooltip-arrow { left: -4px;   top: 50%;  margin-top: -3px;  border-top: none; border-right: none; }

/* ── Transition ── */
.tt-enter-active { transition: opacity var(--duration-fast) var(--ease-out), transform var(--duration-fast) var(--ease-out); }
.tt-leave-active { transition: opacity var(--duration-fast) var(--ease-in); }
.tt-enter-from   { opacity: 0; transform: scale(0.9); }
.tt-leave-to     { opacity: 0; }
</style>

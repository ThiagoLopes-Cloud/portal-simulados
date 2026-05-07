<template>
  <div class="sl-accordion">
    <div
      v-for="(item, index) in items"
      :key="item.id ?? index"
      class="sl-accordion-item"
      :class="{ 'sl-accordion-item--open': openItems.has(item.id ?? index) }"
    >
      <button
        class="sl-accordion-trigger"
        :aria-expanded="openItems.has(item.id ?? index)"
        :aria-controls="`sl-acc-panel-${item.id ?? index}`"
        :id="`sl-acc-btn-${item.id ?? index}`"
        @click="toggle(item.id ?? index)"
      >
        <span class="sl-accordion-label">
          <span v-if="item.icon" class="sl-accordion-icon" v-html="item.icon" />
          {{ item.label }}
        </span>
        <svg
          class="sl-accordion-chevron"
          width="16"
          height="16"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
          stroke-linecap="round"
          stroke-linejoin="round"
          aria-hidden="true"
        >
          <polyline points="6 9 12 15 18 9"/>
        </svg>
      </button>

      <Transition
        name="sl-acc"
        @enter="onEnter"
        @after-enter="onAfterEnter"
        @leave="onLeave"
      >
        <div
          v-show="openItems.has(item.id ?? index)"
          :id="`sl-acc-panel-${item.id ?? index}`"
          class="sl-accordion-panel"
          :aria-labelledby="`sl-acc-btn-${item.id ?? index}`"
          role="region"
        >
          <div class="sl-accordion-body">
            <slot :name="`item-${item.id ?? index}`" :item="item">
              {{ item.content }}
            </slot>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  items:    { type: Array,   required: true },
  multiple: { type: Boolean, default: false },
  default:  { type: [String, Number, Array], default: null },
})

const openItems = ref(new Set(
  props.default
    ? (Array.isArray(props.default) ? props.default : [props.default])
    : []
))

function toggle(id) {
  if (openItems.value.has(id)) {
    openItems.value.delete(id)
  } else {
    if (!props.multiple) openItems.value.clear()
    openItems.value.add(id)
  }
  openItems.value = new Set(openItems.value)
}

function onEnter(el) {
  el.style.height = '0'
  el.style.overflow = 'hidden'
  requestAnimationFrame(() => { el.style.height = el.scrollHeight + 'px' })
}
function onAfterEnter(el) {
  el.style.height = ''
  el.style.overflow = ''
}
function onLeave(el) {
  el.style.height = el.scrollHeight + 'px'
  el.style.overflow = 'hidden'
  requestAnimationFrame(() => { el.style.height = '0' })
}
</script>

<style scoped>
.sl-accordion {
  border: 1px solid var(--color-border);
  border-radius: var(--card-radius);
  overflow: hidden;
}

/* ── Item ── */
.sl-accordion-item {
  border-bottom: 1px solid var(--color-border);
}
.sl-accordion-item:last-child { border-bottom: none; }

/* ── Trigger ── */
.sl-accordion-trigger {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  background: transparent;
  border: none;
  cursor: pointer;
  text-align: left;
  transition: background-color var(--duration-fast) var(--ease-out);
}

.sl-accordion-trigger:hover { background: var(--color-surface-hover); }
.sl-accordion-trigger:focus-visible { outline: none; box-shadow: inset 0 0 0 2px var(--color-orbit); }

.sl-accordion-label {
  display: flex;
  align-items: center;
  gap: var(--space-2-5);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-star);
}

.sl-accordion-icon {
  display: flex;
  align-items: center;
  color: var(--color-orbit);
  flex-shrink: 0;
}

/* ── Chevron ── */
.sl-accordion-chevron {
  color: var(--color-dust);
  flex-shrink: 0;
  transition: transform var(--duration-normal) var(--ease-out), color var(--duration-fast) var(--ease-out);
}

.sl-accordion-item--open .sl-accordion-chevron {
  transform: rotate(180deg);
  color: var(--color-orbit);
}

/* ── Panel ── */
.sl-accordion-panel {
  transition: height var(--duration-normal) var(--ease-in-out);
}

.sl-accordion-body {
  padding: var(--space-1) var(--space-5) var(--space-4);
  font-size: var(--text-sm);
  color: var(--color-comet);
  line-height: var(--leading-relaxed);
}

/* ── Transition ── */
.sl-acc-enter-active,
.sl-acc-leave-active { transition: height var(--duration-normal) var(--ease-in-out), opacity var(--duration-fast) var(--ease-out); }
.sl-acc-enter-from,
.sl-acc-leave-to     { opacity: 0; }
</style>

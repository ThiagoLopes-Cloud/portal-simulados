<template>
  <div class="sl-dropdown" ref="rootRef">
    <!-- Trigger -->
    <div class="sl-dropdown-trigger" @click="toggle" @keydown.enter.space.prevent="toggle">
      <slot name="trigger" :open="isOpen">
        <button
          class="sl-dropdown-btn"
          type="button"
          :aria-expanded="isOpen"
          :aria-haspopup="true"
        >
          {{ label }}
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" :class="['sl-dropdown-caret', { 'sl-dropdown-caret--open': isOpen }]" aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>
        </button>
      </slot>
    </div>

    <!-- Menu -->
    <Transition name="sl-dropdown">
      <div
        v-if="isOpen"
        class="sl-dropdown-menu"
        :class="`sl-dropdown-menu--${align}`"
        role="menu"
        :style="menuStyle"
        @click.stop
      >
        <slot>
          <div
            v-for="(item, i) in items"
            :key="i"
          >
            <div v-if="item.separator" class="sl-dropdown-sep" role="separator" />
            <button
              v-else
              class="sl-dropdown-item"
              :class="[
                item.variant ? `sl-dropdown-item--${item.variant}` : '',
                { 'sl-dropdown-item--disabled': item.disabled }
              ]"
              role="menuitem"
              :disabled="item.disabled"
              @click="handleItem(item)"
            >
              <span v-if="item.icon" class="sl-dropdown-item-icon" v-html="item.icon" />
              <span class="sl-dropdown-item-label">{{ item.label }}</span>
              <span v-if="item.badge" class="sl-dropdown-item-badge">{{ item.badge }}</span>
            </button>
          </div>
        </slot>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  label:   { type: String,  default: 'Menu' },
  items:   { type: Array,   default: () => [] },
  align:   { type: String,  default: 'left', validator: v => ['left', 'right'].includes(v) },
  width:   { type: String,  default: '200px' },
})

const emit = defineEmits(['select'])

const isOpen   = ref(false)
const rootRef  = ref(null)

const menuStyle = computed(() => ({ width: props.width }))

function toggle() { isOpen.value = !isOpen.value }
function close()  { isOpen.value = false }

function handleItem(item) {
  if (item.disabled) return
  emit('select', item)
  if (item.action) item.action()
  close()
}

function handleOutsideClick(e) {
  if (rootRef.value && !rootRef.value.contains(e.target)) close()
}

function handleEsc(e) {
  if (e.key === 'Escape') close()
}

onMounted(() => {
  document.addEventListener('click', handleOutsideClick)
  document.addEventListener('keydown', handleEsc)
})
onUnmounted(() => {
  document.removeEventListener('click', handleOutsideClick)
  document.removeEventListener('keydown', handleEsc)
})
</script>

<style scoped>
.sl-dropdown {
  position: relative;
  display: inline-block;
}

/* ── Default trigger button ── */
.sl-dropdown-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  height: var(--btn-height-md);
  padding: 0 var(--space-4);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-comet);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--btn-radius);
  cursor: pointer;
  transition:
    color var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out);
}
.sl-dropdown-btn:hover {
  color: var(--color-star);
  border-color: var(--color-border-hover);
}
.sl-dropdown-btn:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

.sl-dropdown-caret {
  color: var(--color-dust);
  transition: transform var(--duration-normal) var(--ease-out);
  flex-shrink: 0;
}
.sl-dropdown-caret--open { transform: rotate(180deg); }

/* ── Menu ── */
.sl-dropdown-menu {
  position: absolute;
  top: calc(100% + var(--space-1-5));
  z-index: var(--z-dropdown);
  min-width: 160px;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-hover);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  padding: var(--space-1-5);
  overflow: hidden;
}

.sl-dropdown-menu--left  { left: 0; }
.sl-dropdown-menu--right { right: 0; }

/* ── Item ── */
.sl-dropdown-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: var(--space-2-5);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  color: var(--color-comet);
  background: none;
  border: none;
  cursor: pointer;
  text-align: left;
  transition: background-color var(--duration-fast) var(--ease-out), color var(--duration-fast) var(--ease-out);
}
.sl-dropdown-item:hover:not(:disabled) {
  background: var(--color-surface-hover);
  color: var(--color-star);
}
.sl-dropdown-item:focus-visible { outline: none; background: var(--color-surface-hover); }

.sl-dropdown-item--danger { color: var(--color-nova); }
.sl-dropdown-item--danger:hover { background: var(--color-nova-dim); }

.sl-dropdown-item--disabled { opacity: 0.4; cursor: not-allowed; }

.sl-dropdown-item-icon {
  display: flex;
  align-items: center;
  flex-shrink: 0;
  color: var(--color-dust);
}

.sl-dropdown-item-label { flex: 1; }

.sl-dropdown-item-badge {
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  padding: 1px var(--space-1-5);
  border-radius: var(--radius-full);
  background: var(--color-orbit-dim);
  color: var(--color-orbit);
}

/* ── Separator ── */
.sl-dropdown-sep {
  height: 1px;
  background: var(--color-border);
  margin: var(--space-1-5) 0;
}

/* ── Transition ── */
.sl-dropdown-enter-active { transition: opacity var(--duration-fast) var(--ease-out), transform var(--duration-fast) var(--ease-out); }
.sl-dropdown-leave-active { transition: opacity var(--duration-fast) var(--ease-in); }
.sl-dropdown-enter-from   { opacity: 0; transform: translateY(-6px) scale(0.97); }
.sl-dropdown-leave-to     { opacity: 0; transform: translateY(-4px); }
</style>

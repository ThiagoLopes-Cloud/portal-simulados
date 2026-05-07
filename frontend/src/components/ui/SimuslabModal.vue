<template>
  <Teleport to="body">
    <Transition name="modal">
      <div
        v-if="modelValue"
        class="modal-overlay"
        role="dialog"
        aria-modal="true"
        :aria-labelledby="title ? 'modal-title' : undefined"
        @click.self="closeOnOverlay && close()"
      >
        <div class="modal-panel" :class="`modal--${size}`">
          <!-- Header -->
          <div class="modal-header">
            <slot name="header">
              <h3 id="modal-title" class="modal-title">{{ title }}</h3>
            </slot>
            <button class="modal-close" type="button" @click="close" aria-label="Fechar modal">
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                <path d="M12 4L4 12M4 4L12 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <!-- Body -->
          <div class="modal-body">
            <slot />
          </div>

          <!-- Footer -->
          <div v-if="$slots.footer" class="modal-footer">
            <slot name="footer" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { onMounted, onUnmounted, watch } from 'vue'

const props = defineProps({
  modelValue:     { type: Boolean, default: false },
  title:          { type: String, default: '' },
  size: {
    type: String,
    default: 'md',
    validator: v => ['sm', 'md', 'lg', 'xl'].includes(v),
  },
  closeOnOverlay: { type: Boolean, default: true },
})

const emit = defineEmits(['update:modelValue', 'close'])

function close() {
  emit('update:modelValue', false)
  emit('close')
}

function handleEsc(e) {
  if (e.key === 'Escape' && props.modelValue) close()
}

watch(() => props.modelValue, open => {
  document.body.style.overflow = open ? 'hidden' : ''
})

onMounted(() => document.addEventListener('keydown', handleEsc))
onUnmounted(() => {
  document.removeEventListener('keydown', handleEsc)
  document.body.style.overflow = ''
})
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  z-index: var(--z-modal);
  background: var(--color-bg-overlay);
  backdrop-filter: blur(var(--blur-sm));
  -webkit-backdrop-filter: blur(var(--blur-sm));
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-5);
}

.modal-panel {
  background: var(--modal-bg);
  border: 1px solid var(--color-border-hover);
  border-radius: var(--modal-radius);
  box-shadow: var(--shadow-xl);
  display: flex;
  flex-direction: column;
  max-height: 90vh;
  overflow: hidden;
  width: 100%;
}

/* ── Sizes ── */
.modal--sm { max-width: 360px; }
.modal--md { max-width: 520px; }
.modal--lg { max-width: 720px; }
.modal--xl { max-width: 960px; }

/* Mobile: fullscreen */
@media (max-width: 480px) {
  .modal-overlay { padding: 0; align-items: flex-end; }
  .modal-panel {
    border-radius: var(--radius-xl) var(--radius-xl) 0 0;
    max-height: 92vh;
    max-width: 100%;
  }
}

/* ── Sections ── */
.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--color-border);
  flex-shrink: 0;
}

.modal-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  margin: 0;
  line-height: var(--leading-snug);
}

.modal-close {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  color: var(--color-dust);
  background: transparent;
  border: 1px solid transparent;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition:
    color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out);
}
.modal-close:hover {
  color: var(--color-star);
  background: var(--color-surface-hover);
  border-color: var(--color-border);
}
.modal-close:focus-visible {
  outline: none;
  box-shadow: var(--shadow-focus);
}

.modal-body {
  padding: var(--space-6);
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  padding: var(--space-4) var(--space-6);
  border-top: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: var(--space-3);
  flex-shrink: 0;
}

/* ── Transitions ── */
.modal-enter-active {
  animation: fadeIn var(--duration-normal) var(--ease-out) both;
}
.modal-enter-active .modal-panel {
  animation: scaleIn var(--duration-slow) var(--ease-spring) both;
}
.modal-leave-active {
  animation: fadeIn var(--duration-fast) var(--ease-in) reverse both;
}
.modal-leave-active .modal-panel {
  animation: scaleIn var(--duration-fast) var(--ease-in) reverse both;
}
</style>

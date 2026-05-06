<template>
  <div class="simuslab-logo" :class="[`logo--${size}`, `logo--${variant}`]">
    <!-- Icon mark -->
    <div class="logo-icon">
      <svg :width="iconSize" :height="iconSize" viewBox="0 0 32 32" fill="none" aria-hidden="true">
        <!-- Outer ring -->
        <circle cx="16" cy="16" r="14" stroke="#bfdbfe" stroke-width="1.5" />
        <!-- Middle ring -->
        <circle cx="16" cy="16" r="9" stroke="#93c5fd" stroke-width="1.5" />
        <!-- Core -->
        <circle cx="16" cy="16" r="4" fill="#2563eb" />
        <!-- Orbit dot -->
        <circle cx="16" cy="2" r="2.5" fill="#2563eb" />
      </svg>
    </div>

    <!-- Wordmark -->
    <span v-if="variant !== 'icon-only'" class="logo-wordmark">
      <span class="logo-simus">SIMUS</span><span class="logo-lab">LAB</span>
    </span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  size: {
    type: String,
    default: 'md',
    validator: v => ['sm', 'md', 'lg'].includes(v),
  },
  variant: {
    type: String,
    default: 'default',
    validator: v => ['default', 'icon-only', 'light'].includes(v),
  },
})

const iconSize = computed(() => ({ sm: 24, md: 32, lg: 44 }[props.size]))
</script>

<style scoped>
.simuslab-logo {
  display: inline-flex;
  align-items: center;
  gap: 9px;
  user-select: none;
}

.logo-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* ── Wordmark ── */
.logo-wordmark {
  font-family: var(--font-display);
  font-weight: 900;
  line-height: 1;
  letter-spacing: -0.03em;
}

.logo-simus { color: #2563eb; }
.logo-lab   { color: #0f172a; }

/* ── Light variant (for dark backgrounds) ── */
.logo--light .logo-lab { color: #f8fafc; }

/* ── Sizes ── */
.logo--sm .logo-wordmark { font-size: 1rem; }
.logo--md .logo-wordmark { font-size: 1.25rem; }
.logo--lg .logo-wordmark { font-size: 1.75rem; }
</style>

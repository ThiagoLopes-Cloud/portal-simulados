<template>
  <div class="simuslab-logo" :class="[`logo--${size}`, `logo--${variant}`]">
    <!-- Icon mark -->
    <div class="logo-icon">
      <svg :width="iconSize" :height="iconSize" viewBox="0 0 32 32" fill="none" aria-hidden="true">
        <circle cx="16" cy="16" r="14" class="logo-ring-outer" stroke-width="1.5" />
        <circle cx="16" cy="16" r="9"  class="logo-ring-mid"   stroke-width="1.5" />
        <circle cx="16" cy="16" r="4"  class="logo-core" />
        <circle cx="16" cy="2"  r="2.5" class="logo-dot" />
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

/* ── SVG rings ── */
.logo-ring-outer { stroke: var(--color-orbit); opacity: 0.35; }
.logo-ring-mid   { stroke: var(--color-orbit); opacity: 0.65; }
.logo-core       { fill: var(--color-orbit); }
.logo-dot        { fill: var(--color-orbit); }

/* ── Wordmark ── */
.logo-wordmark {
  font-family: var(--font-display);
  font-weight: 900;
  line-height: 1;
  letter-spacing: -0.03em;
}

.logo-simus { color: var(--color-orbit); }
.logo-lab   { color: var(--color-star); }

/* ── Sizes ── */
.logo--sm .logo-wordmark { font-size: 1rem; }
.logo--md .logo-wordmark { font-size: 1.25rem; }
.logo--lg .logo-wordmark { font-size: 1.75rem; }
</style>

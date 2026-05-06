<template>
  <div class="simuslab-logo" :class="[`logo--${size}`, `logo--${variant}`]">
    <!-- Orbital icon -->
    <div class="logo-icon">
      <div class="logo-core" />
      <div class="logo-ring logo-ring--inner" />
      <div class="logo-ring logo-ring--outer">
        <div class="logo-particle logo-particle--primary" />
      </div>
      <div class="logo-ring logo-ring--outermost">
        <div class="logo-particle logo-particle--secondary" />
      </div>
    </div>

    <!-- Wordmark -->
    <span v-if="variant !== 'icon-only'" class="logo-wordmark">
      <span class="logo-word-orbit">ORB</span><span class="logo-word-yn">YN</span>
    </span>
  </div>
</template>

<script setup>
defineProps({
  /** Visual size: 'sm' | 'md' | 'lg' */
  size: {
    type: String,
    default: 'md',
    validator: v => ['sm', 'md', 'lg'].includes(v),
  },
  /** Variant: 'default' | 'icon-only' | 'light' */
  variant: {
    type: String,
    default: 'default',
    validator: v => ['default', 'icon-only', 'light'].includes(v),
  },
})
</script>

<style scoped>
.simuslab-logo {
  display: inline-flex;
  align-items: center;
  gap: 10px;
  user-select: none;
}

/* ── Icon container ── */
.logo-icon {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

/* ── Core dot ── */
.logo-core {
  position: absolute;
  background: var(--color-orbit);
  border-radius: 50%;
  box-shadow: 0 0 8px var(--color-orbit);
  z-index: 2;
}

/* ── Rings ── */
.logo-ring {
  position: absolute;
  border-radius: 50%;
  border: 1px solid transparent;
}

.logo-ring--inner {
  border-color: rgba(0, 229, 255, 0.35);
}

.logo-ring--outer {
  border-color: rgba(0, 229, 255, 0.2);
  animation: orbitSpin 3.5s linear infinite;
}

.logo-ring--outermost {
  border-color: rgba(124, 110, 255, 0.15);
  animation: orbitSpinReverse 6s linear infinite;
}

/* ── Particles ── */
.logo-particle {
  position: absolute;
  border-radius: 50%;
  top: 0;
  left: 50%;
  transform: translate(-50%, -50%);
}

.logo-particle--primary {
  background: var(--color-orbit);
  box-shadow: 0 0 6px var(--color-orbit), 0 0 12px var(--color-orbit-glow);
}

.logo-particle--secondary {
  background: var(--color-pulsar);
  box-shadow: 0 0 6px var(--color-pulsar);
}

/* ── Wordmark ── */
.logo-wordmark {
  font-family: var(--font-display);
  font-weight: var(--weight-extrabold);
  letter-spacing: -0.02em;
  line-height: 1;
}

.logo-word-orbit { color: var(--color-orbit); }
.logo-word-yn    { color: var(--color-star); }

/* ── Variant: light ── */
.logo--light .logo-word-yn { color: rgba(240, 242, 255, 0.85); }

/* ── Sizes ── */
.logo--sm .logo-icon  { width: 24px; height: 24px; }
.logo--sm .logo-core  { width: 5px; height: 5px; }
.logo--sm .logo-ring--inner      { width: 12px; height: 12px; }
.logo--sm .logo-ring--outer      { width: 18px; height: 18px; }
.logo--sm .logo-ring--outermost  { width: 23px; height: 23px; }
.logo--sm .logo-particle--primary   { width: 3px; height: 3px; }
.logo--sm .logo-particle--secondary { width: 2.5px; height: 2.5px; }
.logo--sm .logo-wordmark { font-size: 1rem; }

.logo--md .logo-icon  { width: 36px; height: 36px; }
.logo--md .logo-core  { width: 7px; height: 7px; }
.logo--md .logo-ring--inner      { width: 18px; height: 18px; }
.logo--md .logo-ring--outer      { width: 28px; height: 28px; }
.logo--md .logo-ring--outermost  { width: 35px; height: 35px; }
.logo--md .logo-particle--primary   { width: 4.5px; height: 4.5px; }
.logo--md .logo-particle--secondary { width: 3.5px; height: 3.5px; }
.logo--md .logo-wordmark { font-size: 1.25rem; }

.logo--lg .logo-icon  { width: 54px; height: 54px; }
.logo--lg .logo-core  { width: 10px; height: 10px; }
.logo--lg .logo-ring--inner      { width: 26px; height: 26px; }
.logo--lg .logo-ring--outer      { width: 40px; height: 40px; }
.logo--lg .logo-ring--outermost  { width: 53px; height: 53px; }
.logo--lg .logo-particle--primary   { width: 6px; height: 6px; }
.logo--lg .logo-particle--secondary { width: 5px; height: 5px; }
.logo--lg .logo-wordmark { font-size: 1.75rem; }
</style>

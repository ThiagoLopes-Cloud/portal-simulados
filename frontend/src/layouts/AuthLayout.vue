<template>
  <div class="auth-layout">
    <!-- ── Left panel: brand / star field ── -->
    <div class="auth-brand starfield" aria-hidden="true">
      <!-- Decorative glows -->
      <div class="glow-blob glow-blob--top" />
      <div class="glow-blob glow-blob--bottom" />

      <div class="auth-brand-content">
        <OrbynLogo size="lg" class="mb-10" />

        <h1 class="brand-headline">
          O futuro da<br />sua aprovação<br />começa aqui.
        </h1>

        <p class="brand-sub">
          Utilize dados precisos e simulações realistas para mapear seus
          pontos cegos, otimizar seu tempo e garantir sua vaga.
        </p>

        <!-- Abstract chart decoration -->
        <div class="brand-chart" aria-hidden="true">
          <div class="chart-bar" style="height:30%" />
          <div class="chart-bar" style="height:52%" />
          <div class="chart-bar" style="height:73%" />
          <div class="chart-bar chart-bar--accent" style="height:100%" />
        </div>
      </div>
    </div>

    <!-- ── Right panel: form slot ── -->
    <div class="auth-form-panel">
      <div class="auth-form-inner">
        <slot />
      </div>
    </div>
  </div>
</template>

<script setup>
import OrbynLogo from '../components/ui/OrbynLogo.vue'
</script>

<style scoped>
.auth-layout {
  display: flex;
  min-height: 100vh;
  background: var(--color-cosmos);
}

/* ── Brand panel ── */
.auth-brand {
  flex: 1.2;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-16);
  border-right: 1px solid var(--color-border);
  overflow: hidden;
}

/* Glow decorations */
.glow-blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  pointer-events: none;
}
.glow-blob--top {
  width: 400px;
  height: 400px;
  background: var(--color-orbit-glow);
  top: -100px;
  right: -80px;
  opacity: 0.4;
}
.glow-blob--bottom {
  width: 300px;
  height: 300px;
  background: var(--color-pulsar-glow);
  bottom: -60px;
  left: -60px;
  opacity: 0.3;
}

.auth-brand-content {
  position: relative;
  z-index: 1;
  max-width: 440px;
}

.brand-headline {
  font-family: var(--font-display);
  font-size: var(--text-4xl);
  font-weight: var(--weight-extrabold);
  color: var(--color-star);
  line-height: var(--leading-tight);
  letter-spacing: -0.02em;
  margin-bottom: var(--space-6);
}

.brand-sub {
  font-family: var(--font-body);
  font-size: var(--text-md);
  color: var(--color-comet);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-12);
}

/* Abstract chart */
.brand-chart {
  display: flex;
  align-items: flex-end;
  gap: var(--space-3);
  height: 96px;
}

.chart-bar {
  width: 36px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
  border: 1px solid var(--color-border);
}
.chart-bar--accent {
  background: var(--color-orbit);
  box-shadow: 0 0 20px var(--color-orbit-glow), 0 -4px 24px var(--color-orbit-glow);
  border-color: var(--color-orbit);
}

/* ── Form panel ── */
.auth-form-panel {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-10) var(--space-8);
}

.auth-form-inner {
  width: 100%;
  max-width: 380px;
}

/* ── Mobile: stack vertically ── */
@media (max-width: 768px) {
  .auth-layout { flex-direction: column; }
  .auth-brand  { display: none; }
  .auth-form-panel {
    flex: 1;
    padding: var(--space-8) var(--space-5);
  }
}
</style>

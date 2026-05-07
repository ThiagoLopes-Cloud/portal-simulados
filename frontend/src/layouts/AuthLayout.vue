<template>
  <div class="auth-shell">

    <!-- ══ LADO A — Painel de Marca (desktop) ══ -->
    <aside class="brand-panel" aria-hidden="true">
      <div class="brand-dot-grid" />
      <div class="brand-glow brand-glow--tr" />
      <div class="brand-glow brand-glow--bl" />

      <div class="brand-content">
        <!-- Logo -->
        <SimuslabLogo size="lg" variant="light" />

        <!-- Headline -->
        <div class="brand-headline-block">
          <h1 class="brand-headline">
            Desbloqueie seu<br />potencial acadêmico<br />com inteligência<br />baseada em dados.
          </h1>
          <p class="brand-sub">
            Simulações cronometradas, mapas de acerto por matéria e planos de estudo adaptativos — tudo calibrado para a sua aprovação.
          </p>
        </div>

        <!-- Métricas -->
        <div class="stats-strip">
          <div class="stat">
            <span class="stat-value">94%</span>
            <span class="stat-label">taxa de aprovação</span>
          </div>
          <div class="stat-sep" aria-hidden="true" />
          <div class="stat">
            <span class="stat-value">12k+</span>
            <span class="stat-label">questões no banco</span>
          </div>
          <div class="stat-sep" aria-hidden="true" />
          <div class="stat">
            <span class="stat-value">3.200</span>
            <span class="stat-label">alunos ativos</span>
          </div>
        </div>

        <!-- Depoimento -->
        <div class="testimonial">
          <svg class="quote-icon" width="24" height="18" viewBox="0 0 24 18" fill="none" aria-hidden="true">
            <path d="M0 18V10.8C0 4.836 3.552 1.26 10.656 0L11.52 1.8C8.64 2.508 6.696 3.78 5.688 5.616c-.408.756-.6 1.476-.576 2.16H8.16V18H0zm13.44 0V10.8C13.44 4.836 16.992 1.26 24.096 0L24.96 1.8c-2.88.708-4.824 1.98-5.832 3.816-.408.756-.6 1.476-.576 2.16H21.6V18H13.44z" fill="rgba(255,255,255,0.1)"/>
          </svg>
          <p class="testimonial-body">
            Após 3 semanas no SIMUSLAB, meu desempenho em Raciocínio Lógico saltou de 42% para 78%. O sistema identifica exatamente onde você está errando.
          </p>
          <div class="testimonial-author">
            <div class="author-avatar" aria-hidden="true">MR</div>
            <div>
              <p class="author-name">Maria R.</p>
              <p class="author-role">Aprovada no Concurso SERPRO 2024</p>
            </div>
          </div>
        </div>
      </div>
    </aside>

    <!-- ══ LADO B — Painel do Formulário ══ -->
    <main class="form-panel">
      <header class="mobile-topbar">
        <SimuslabLogo size="md" />
      </header>

      <div class="form-inner">
        <slot />
      </div>

      <footer class="form-footer">
        <span>© 2026 SIMUSLAB</span>
        <span aria-hidden="true">·</span>
        <a href="#">Privacidade</a>
        <span aria-hidden="true">·</span>
        <a href="#">Suporte</a>
      </footer>
    </main>

  </div>
</template>

<script setup>
import SimuslabLogo from '../components/ui/SimuslabLogo.vue'
</script>

<style scoped>
/* ══ Shell ══ */
.auth-shell {
  display: flex;
  min-height: 100vh;
  background: var(--color-bg-base);
}

/* ══ Brand Panel ══ */
.brand-panel {
  flex: 0 0 520px;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 56px 52px;
  overflow: hidden;
  background: var(--color-bg-panel);
  border-right: 1px solid var(--color-border);
}

/* Dot grid background */
.brand-dot-grid {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, rgba(255, 255, 255, 0.06) 1px, transparent 1px);
  background-size: 28px 28px;
  pointer-events: none;
}

/* Glow blobs — usa cores do DS */
.brand-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(72px);
  pointer-events: none;
}
.brand-glow--tr {
  width: 360px;
  height: 360px;
  background: var(--color-orbit-glow);
  top: -80px;
  right: -60px;
}
.brand-glow--bl {
  width: 280px;
  height: 280px;
  background: var(--color-pulsar-glow);
  bottom: -40px;
  left: -40px;
}

.brand-content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  gap: var(--space-9);
}

/* Headline */
.brand-headline-block {
  display: flex;
  flex-direction: column;
  gap: var(--space-3-5);
}

.brand-headline {
  font-family: var(--font-display);
  font-size: 2.1rem;
  font-weight: var(--weight-extrabold);
  color: var(--color-star);
  line-height: var(--leading-tight);
  letter-spacing: var(--tracking-tight);
}

.brand-sub {
  font-size: var(--text-base);
  color: var(--color-comet);
  line-height: var(--leading-relaxed);
}

/* Stats */
.stats-strip {
  display: flex;
  align-items: center;
  gap: var(--space-5);
  padding: var(--space-4) var(--space-5);
  background: var(--color-surface-hover);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
}
.stat {
  display: flex;
  flex-direction: column;
  gap: 2px;
  flex: 1;
  align-items: center;
}
.stat-value {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: var(--weight-extrabold);
  color: var(--color-star);
  letter-spacing: var(--tracking-tight);
  line-height: 1;
}
.stat-label {
  font-size: var(--text-2xs);
  color: var(--color-dust);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  font-weight: var(--weight-semibold);
  text-align: center;
}
.stat-sep {
  width: 1px;
  height: 32px;
  background: var(--color-border);
  flex-shrink: 0;
}

/* Testimonial */
.testimonial {
  padding: var(--space-5);
  background: var(--color-surface-hover);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  gap: var(--space-3-5);
}
.quote-icon { flex-shrink: 0; }

.testimonial-body {
  font-size: var(--text-sm);
  color: var(--color-comet);
  line-height: var(--leading-relaxed);
  font-style: italic;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}
.author-avatar {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
  background: linear-gradient(135deg, var(--color-orbit), var(--color-pulsar));
  color: var(--color-cosmos);
  font-size: var(--text-xs);
  font-weight: var(--weight-bold);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.author-name {
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-star);
}
.author-role {
  font-size: var(--text-xs);
  color: var(--color-dust);
  margin-top: 2px;
}

/* ══ Form Panel ══ */
.form-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--color-bg-base);
  min-height: 100vh;
  border-left: 1px solid var(--color-border);
}

.mobile-topbar {
  display: none;
  padding: var(--space-5) var(--space-6);
  border-bottom: 1px solid var(--color-border);
}

.form-inner {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--space-12) var(--space-10);
}

.form-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-6);
  font-size: var(--text-xs);
  color: var(--color-dust);
  border-top: 1px solid var(--color-border);
}
.form-footer a {
  color: var(--color-dust);
  text-decoration: none;
  transition: color var(--duration-fast) var(--ease-out);
}
.form-footer a:hover { color: var(--color-comet); }

/* ══ Responsive ══ */
@media (max-width: 900px) {
  .brand-panel { flex: 0 0 380px; padding: var(--space-10) var(--space-8); }
  .brand-headline { font-size: 1.7rem; }
}

@media (max-width: 768px) {
  .auth-shell { background: var(--color-bg-base); }
  .brand-panel { display: none; }
  .mobile-topbar { display: flex; }
  .form-inner { padding: var(--space-8) var(--space-6); align-items: flex-start; }
}
</style>

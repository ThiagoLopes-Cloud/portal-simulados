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
          <div class="stat-sep" />
          <div class="stat">
            <span class="stat-value">12k+</span>
            <span class="stat-label">questões no banco</span>
          </div>
          <div class="stat-sep" />
          <div class="stat">
            <span class="stat-value">3.200</span>
            <span class="stat-label">alunos ativos</span>
          </div>
        </div>

        <!-- Depoimento -->
        <div class="testimonial">
          <svg class="quote-icon" width="24" height="18" viewBox="0 0 24 18" fill="none">
            <path d="M0 18V10.8C0 4.836 3.552 1.26 10.656 0L11.52 1.8C8.64 2.508 6.696 3.78 5.688 5.616c-.408.756-.6 1.476-.576 2.16H8.16V18H0zm13.44 0V10.8C13.44 4.836 16.992 1.26 24.096 0L24.96 1.8c-2.88.708-4.824 1.98-5.832 3.816-.408.756-.6 1.476-.576 2.16H21.6V18H13.44z" fill="rgba(148,163,184,0.3)"/>
          </svg>
          <p class="testimonial-body">
            Após 3 semanas no SIMUSLAB, meu desempenho em Raciocínio Lógico saltou de 42% para 78%. O sistema identifica exatamente onde você está errando.
          </p>
          <div class="testimonial-author">
            <div class="author-avatar">MR</div>
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
      <!-- Cabeçalho mobile (logo só aparece aqui quando o painel esquerdo some) -->
      <header class="mobile-topbar">
        <SimuslabLogo size="md" />
      </header>

      <div class="form-inner">
        <slot />
      </div>

      <footer class="form-footer">
        <span>© 2025 SIMUSLAB</span>
        <span>·</span>
        <a href="#">Privacidade</a>
        <span>·</span>
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
  background: #0f172a;
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
  background: #0f172a;
  border-right: 1px solid rgba(255, 255, 255, 0.06);
}

/* Dot grid background */
.brand-dot-grid {
  position: absolute;
  inset: 0;
  background-image: radial-gradient(circle, rgba(255, 255, 255, 0.07) 1px, transparent 1px);
  background-size: 28px 28px;
  pointer-events: none;
}

/* Glow blobs */
.brand-glow {
  position: absolute;
  border-radius: 50%;
  filter: blur(72px);
  pointer-events: none;
}
.brand-glow--tr {
  width: 360px;
  height: 360px;
  background: rgba(37, 99, 235, 0.22);
  top: -80px;
  right: -60px;
}
.brand-glow--bl {
  width: 280px;
  height: 280px;
  background: rgba(99, 102, 241, 0.15);
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
  gap: 36px;
}

/* Headline */
.brand-headline-block { display: flex; flex-direction: column; gap: 14px; }

.brand-headline {
  font-family: var(--font-display);
  font-size: 2.1rem;
  font-weight: 800;
  color: #f8fafc;
  line-height: 1.18;
  letter-spacing: -0.025em;
}

.brand-sub {
  font-size: 0.9375rem;
  color: #64748b;
  line-height: 1.65;
}

/* Stats */
.stats-strip {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 18px 20px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 14px;
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
  font-size: 1.5rem;
  font-weight: 800;
  color: #f1f5f9;
  letter-spacing: -0.02em;
  line-height: 1;
}
.stat-label {
  font-size: 0.65rem;
  color: #475569;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 600;
  text-align: center;
}
.stat-sep {
  width: 1px;
  height: 32px;
  background: rgba(255, 255, 255, 0.08);
  flex-shrink: 0;
}

/* Testimonial */
.testimonial {
  padding: 22px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.07);
  border-radius: 14px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.quote-icon { flex-shrink: 0; }

.testimonial-body {
  font-size: 0.875rem;
  color: #94a3b8;
  line-height: 1.65;
  font-style: italic;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 12px;
}
.author-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #1d4ed8, #4f46e5);
  color: #ffffff;
  font-size: 0.7rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.author-name {
  font-size: 0.875rem;
  font-weight: 600;
  color: #f1f5f9;
}
.author-role {
  font-size: 0.7rem;
  color: #475569;
  margin-top: 2px;
}

/* ══ Form Panel ══ */
.form-panel {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #ffffff;
  min-height: 100vh;
}

.mobile-topbar {
  display: none;
  padding: 20px 24px;
  border-bottom: 1px solid #f1f5f9;
}

.form-inner {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 48px 40px;
}

.form-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px 24px;
  font-size: 0.75rem;
  color: #94a3b8;
  border-top: 1px solid #f1f5f9;
}
.form-footer a {
  color: #94a3b8;
  text-decoration: none;
}
.form-footer a:hover {
  color: #475569;
}

/* ══ Responsive ══ */
@media (max-width: 900px) {
  .brand-panel { flex: 0 0 380px; padding: 40px 32px; }
  .brand-headline { font-size: 1.7rem; }
}

@media (max-width: 768px) {
  .auth-shell { background: #ffffff; }
  .brand-panel { display: none; }
  .mobile-topbar { display: flex; }
  .form-inner { padding: 32px 24px; align-items: flex-start; }
}
</style>

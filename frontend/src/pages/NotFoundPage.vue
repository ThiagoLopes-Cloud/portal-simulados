<template>
  <div class="nf-layout starfield">
    <div class="nf-content">
      <OrbynLogo size="md" class="mb-10" />
      <div class="nf-code">404</div>
      <h1 class="nf-title">Rota não encontrada.</h1>
      <p class="nf-sub">Esta coordenada não existe no laboratório. Pode ser que a URL esteja incorreta ou que a página tenha sido removida.</p>
      <div class="nf-actions">
        <OrbynButton variant="primary" size="md" @click="$router.push('/dashboard')">
          Voltar ao Dashboard
        </OrbynButton>
        <OrbynButton variant="ghost" size="md" @click="$router.go(-1)">
          Página Anterior
        </OrbynButton>
      </div>
    </div>
    <div class="nf-glow-top" />
    <div class="nf-glow-bottom" />
  </div>
</template>

<script setup>
import OrbynLogo from '../components/ui/OrbynLogo.vue'
import OrbynButton from '../components/ui/OrbynButton.vue'
</script>

<style scoped>
.nf-layout {
  min-height: 100vh;
  background: var(--color-cosmos);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}
.nf-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: var(--space-8);
  max-width: 520px;
}
.mb-10 { margin-bottom: var(--space-10); }
.nf-code {
  font-family: var(--font-mono);
  font-size: 7rem;
  font-weight: var(--weight-extrabold);
  color: var(--color-orbit);
  line-height: 1;
  margin-bottom: var(--space-6);
  text-shadow: 0 0 60px rgba(0,229,255,0.3), 0 0 120px rgba(0,229,255,0.1);
  letter-spacing: -0.04em;
}
.nf-title {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: var(--weight-extrabold);
  color: var(--color-star);
  margin-bottom: var(--space-4);
  line-height: var(--leading-tight);
}
.nf-sub {
  font-size: var(--text-base);
  color: var(--color-comet);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--space-10);
}
.nf-actions { display: flex; gap: var(--space-3); flex-wrap: wrap; justify-content: center; }

.nf-glow-top {
  position: absolute;
  width: 500px; height: 500px;
  background: rgba(0,229,255,0.04);
  border-radius: 50%;
  filter: blur(80px);
  top: -150px; right: -100px;
  pointer-events: none;
}
.nf-glow-bottom {
  position: absolute;
  width: 400px; height: 400px;
  background: rgba(124,110,255,0.04);
  border-radius: 50%;
  filter: blur(80px);
  bottom: -100px; left: -80px;
  pointer-events: none;
}
</style>

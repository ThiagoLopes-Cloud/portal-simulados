<template>
  <button
    type="button"
    class="trilha-card"
    @click="$emit('click')"
  >
    <!-- Header com gradiente da cor da trilha -->
    <div
      class="trilha-header"
      :style="{ background: `linear-gradient(135deg, ${trilha.cor}1A 0%, ${trilha.cor}33 100%)` }"
    >
      <span class="trilha-emoji" aria-hidden="true">{{ trilha.icone }}</span>

      <span v-if="trilha.percentual_progresso === 100" class="trilha-badge trilha-badge--done">
        <svg width="9" height="9" viewBox="0 0 12 12" fill="none" aria-hidden="true">
          <path d="M2 6l3 3 5-5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Completo
      </span>
      <span v-else-if="trilha.aulas_concluidas > 0" class="trilha-badge trilha-badge--progress">
        Em progresso
      </span>
      <span v-else class="trilha-badge trilha-badge--new">
        Novo
      </span>

      <h3 class="trilha-title">{{ trilha.nome }}</h3>
    </div>

    <!-- Body -->
    <div class="trilha-body">
      <div class="trilha-meta">
        <span class="trilha-meta-item">
          <svg width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true">
            <rect x="2" y="2" width="5" height="5" rx="1" fill="currentColor"/>
            <rect x="9" y="2" width="5" height="5" rx="1" fill="currentColor"/>
            <rect x="2" y="9" width="5" height="5" rx="1" fill="currentColor"/>
            <rect x="9" y="9" width="5" height="5" rx="1" fill="currentColor" opacity=".4"/>
          </svg>
          {{ trilha.total_modulos }} módulos
        </span>
        <span class="trilha-meta-sep" aria-hidden="true">·</span>
        <span class="trilha-meta-item">
          <svg width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true">
            <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
            <path d="M6 5.5l5 2.5-5 2.5V5.5z" fill="currentColor"/>
          </svg>
          {{ trilha.total_aulas }} aulas
        </span>
        <span v-if="trilha.aulas_concluidas > 0" class="trilha-meta-sep" aria-hidden="true">·</span>
        <span v-if="trilha.aulas_concluidas > 0" class="trilha-meta-count">
          {{ trilha.aulas_concluidas }}/{{ trilha.total_aulas }}
        </span>
      </div>

      <!-- Barra de progresso -->
      <div class="trilha-progress">
        <div class="trilha-progress-track" role="progressbar" :aria-valuenow="trilha.percentual_progresso" aria-valuemin="0" aria-valuemax="100">
          <div
            class="trilha-progress-fill"
            :style="{
              width: `${trilha.percentual_progresso}%`,
              background: trilha.percentual_progresso === 100
                ? 'var(--color-stellar)'
                : `linear-gradient(90deg, ${trilha.cor}, ${trilha.cor}cc)`
            }"
          />
        </div>
        <div class="trilha-progress-labels">
          <span class="trilha-percent">{{ trilha.percentual_progresso }}%</span>
          <span v-if="trilha.percentual_progresso < 100" class="trilha-remaining">
            {{ trilha.total_aulas - trilha.aulas_concluidas }} restantes
          </span>
        </div>
      </div>

      <!-- CTA -->
      <div class="trilha-cta" aria-hidden="true">
        <span class="trilha-cta-text">
          {{ trilha.percentual_progresso === 0 ? 'Começar trilha' : trilha.percentual_progresso === 100 ? 'Revisar trilha' : 'Continuar' }}
        </span>
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <polyline points="9 18 15 12 9 6"/>
        </svg>
      </div>
    </div>
  </button>
</template>

<script setup>
defineProps({
  trilha: { type: Object, required: true },
})
defineEmits(['click'])
</script>

<style scoped>
.trilha-card {
  position: relative;
  width: 100%;
  text-align: left;
  border-radius: var(--radius-xl);
  overflow: hidden;
  border: 1px solid var(--color-border);
  background: var(--color-bg-surface);
  box-shadow: var(--card-shadow);
  cursor: pointer;
  display: flex;
  flex-direction: column;
  transition:
    box-shadow var(--duration-normal) var(--ease-out),
    transform var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out);
}
.trilha-card:hover {
  box-shadow: var(--shadow-xl);
  transform: translateY(-3px);
  border-color: var(--color-border-hover);
}
.trilha-card:hover .trilha-cta { color: var(--color-orbit); }
.trilha-card:active { transform: scale(0.98) translateY(0); }
.trilha-card:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

/* ── Header ── */
.trilha-header {
  position: relative;
  height: 120px;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: var(--space-4);
}

.trilha-emoji {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  font-size: 2.5rem;
  opacity: 0.55;
  user-select: none;
  line-height: 1;
  transition: opacity var(--duration-normal) var(--ease-out), transform var(--duration-normal) var(--ease-out);
}
.trilha-card:hover .trilha-emoji { opacity: 0.8; transform: scale(1.08) rotate(-4deg); }

.trilha-badge {
  position: absolute;
  top: var(--space-3);
  left: var(--space-3);
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-family: var(--font-display);
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  padding: 2px var(--space-2);
  border-radius: var(--radius-full);
  letter-spacing: var(--tracking-wide);
  text-transform: uppercase;
}
.trilha-badge--done     { background: var(--color-stellar-dim); color: var(--color-stellar); border: 1px solid var(--color-stellar-border); }
.trilha-badge--progress { background: var(--color-orbit-dim);   color: var(--color-orbit);   border: 1px solid var(--color-orbit-border); }
.trilha-badge--new      { background: var(--color-pulsar-dim);  color: var(--color-pulsar);  border: 1px solid var(--color-pulsar-border); }

.trilha-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  line-height: var(--leading-tight);
  padding-right: 3rem;
  margin: 0;
}

/* ── Body ── */
.trilha-body {
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  flex: 1;
}

.trilha-meta {
  display: flex;
  align-items: center;
  gap: var(--space-2-5);
  font-size: var(--text-xs);
  color: var(--color-dust);
  flex-wrap: wrap;
}
.trilha-meta-item {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
}
.trilha-meta-sep { color: var(--color-border); }
.trilha-meta-count {
  font-weight: var(--weight-semibold);
  color: var(--color-orbit);
}

/* ── Progress ── */
.trilha-progress { display: flex; flex-direction: column; gap: var(--space-1-5); }

.trilha-progress-track {
  height: 6px;
  width: 100%;
  background: var(--color-bg-elevated);
  border-radius: var(--radius-full);
  overflow: hidden;
}
.trilha-progress-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width var(--duration-slow) var(--ease-out);
}

.trilha-progress-labels {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.trilha-percent {
  font-size: var(--text-xs);
  color: var(--color-dust);
}
.trilha-remaining {
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  color: var(--color-orbit);
}

/* ── CTA ── */
.trilha-cta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-top: var(--space-1);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-comet);
  margin-top: auto;
  transition: color var(--duration-fast) var(--ease-out);
  border-top: 1px solid var(--color-border);
}
.trilha-cta-text { line-height: 1; }
</style>

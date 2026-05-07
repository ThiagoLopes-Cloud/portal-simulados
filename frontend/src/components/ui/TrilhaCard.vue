<template>
  <button
    type="button"
    class="trilha-card"
    @click="$emit('click')"
  >
    <!-- Header com gradiente da cor da trilha -->
    <div
      class="trilha-header"
      :style="{ background: `linear-gradient(135deg, ${trilha.cor}22 0%, ${trilha.cor}44 100%)` }"
    >
      <span class="trilha-emoji" aria-hidden="true">{{ trilha.icone }}</span>

      <span v-if="trilha.percentual_progresso === 100" class="trilha-badge trilha-badge--done">
        COMPLETO ✓
      </span>
      <span v-else-if="trilha.aulas_concluidas > 0" class="trilha-badge trilha-badge--progress">
        EM PROGRESSO
      </span>

      <h3 class="trilha-title">{{ trilha.nome }}</h3>
    </div>

    <!-- Body -->
    <div class="trilha-body">
      <div class="trilha-meta">
        <span class="trilha-meta-item">
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true">
            <rect x="2" y="2" width="5" height="5" rx="1" fill="currentColor"/>
            <rect x="9" y="2" width="5" height="5" rx="1" fill="currentColor"/>
            <rect x="2" y="9" width="5" height="5" rx="1" fill="currentColor"/>
            <rect x="9" y="9" width="5" height="5" rx="1" fill="currentColor" opacity=".4"/>
          </svg>
          {{ trilha.total_modulos }} módulos
        </span>
        <span class="trilha-meta-sep" aria-hidden="true">·</span>
        <span class="trilha-meta-item">
          <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true">
            <circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/>
            <path d="M6 5.5l5 2.5-5 2.5V5.5z" fill="currentColor"/>
          </svg>
          {{ trilha.total_aulas }} aulas
        </span>
        <span class="trilha-meta-sep" aria-hidden="true">·</span>
        <span class="trilha-meta-count">{{ trilha.aulas_concluidas }}/{{ trilha.total_aulas }}</span>
      </div>

      <div class="trilha-progress">
        <div class="trilha-progress-track">
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
          <span class="trilha-percent">{{ trilha.percentual_progresso }}% concluído</span>
          <span v-if="trilha.percentual_progresso < 100" class="trilha-remaining">
            +{{ trilha.total_aulas - trilha.aulas_concluidas }} restantes
          </span>
        </div>
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
  background: var(--card-bg);
  box-shadow: var(--card-shadow);
  cursor: pointer;
  transition:
    box-shadow var(--duration-normal) var(--ease-out),
    transform var(--duration-fast) var(--ease-spring),
    border-color var(--duration-fast) var(--ease-out);
}
.trilha-card:hover {
  box-shadow: var(--shadow-xl);
  transform: translateY(-2px);
  border-color: var(--color-border-hover);
}
.trilha-card:active { transform: scale(0.98); }
.trilha-card:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

/* ── Header ── */
.trilha-header {
  position: relative;
  height: 112px;
  display: flex;
  align-items: flex-end;
  padding: var(--space-4);
}

.trilha-emoji {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  font-size: 2.25rem;
  opacity: 0.6;
  user-select: none;
  line-height: 1;
}

.trilha-badge {
  position: absolute;
  top: var(--space-3);
  left: var(--space-3);
  font-family: var(--font-display);
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  padding: 2px var(--space-2);
  border-radius: var(--radius-full);
  letter-spacing: var(--tracking-wide);
}
.trilha-badge--done     { background: var(--color-stellar); color: var(--color-cosmos); }
.trilha-badge--progress { background: var(--color-orbit);   color: var(--color-cosmos); }

.trilha-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  line-height: var(--leading-tight);
  padding-right: var(--space-12, 48px);
  margin: 0;
}

/* ── Body ── */
.trilha-body {
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.trilha-meta {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  font-family: var(--font-body);
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
.trilha-progress { display: flex; flex-direction: column; gap: var(--space-1); }

.trilha-progress-track {
  height: 8px;
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
  font-size: 11px;
  color: var(--color-dust);
}
.trilha-remaining {
  font-size: 11px;
  font-weight: var(--weight-semibold);
  color: var(--color-orbit);
}
</style>

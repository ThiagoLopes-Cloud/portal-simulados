<template>
  <a
    :href="material.url || '#'"
    :target="material.url ? '_blank' : undefined"
    rel="noopener noreferrer"
    class="material-card"
    :class="`material-card--${tipo}`"
  >
    <!-- Ícone por tipo -->
    <div class="material-icon" aria-hidden="true">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" v-html="icon" />
    </div>

    <!-- Conteúdo -->
    <div class="material-content">
      <p class="material-title">{{ material.titulo }}</p>
      <div class="material-meta">
        <span class="material-badge">{{ material.tipo }}</span>
        <span v-if="material.tamanho_kb" class="material-size">{{ formatSize(material.tamanho_kb) }}</span>
      </div>
    </div>

    <!-- Seta -->
    <svg class="material-arrow" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
      <path d="M6 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </a>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  material: { type: Object, required: true },
})

const ICONS = {
  PDF:       `<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>`,
  VIDEO:     `<polygon points="5 3 19 12 5 21 5 3"/>`,
  LINK:      `<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>`,
  EXERCICIO: `<path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>`,
}

const tipo = computed(() => (props.material.tipo || 'LINK').toUpperCase())
const icon = computed(() => ICONS[tipo.value] || ICONS.LINK)

function formatSize(kb) {
  if (kb >= 1024) return `${(kb / 1024).toFixed(1)} MB`
  return `${kb} KB`
}
</script>

<style scoped>
.material-card {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  background: var(--color-bg-surface);
  text-decoration: none;
  transition:
    border-color var(--duration-fast) var(--ease-out),
    box-shadow var(--duration-fast) var(--ease-out),
    transform var(--duration-fast) var(--ease-out);
}
.material-card:hover {
  border-color: var(--color-orbit-border);
  box-shadow: var(--shadow-md);
}
.material-card:active { transform: scale(0.98); }
.material-card:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

/* ── Type-specific icon containers ── */
.material-icon {
  flex-shrink: 0;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.material-card--PDF    .material-icon { background: var(--color-nova-dim);   color: var(--color-nova); }
.material-card--VIDEO  .material-icon { background: var(--color-pulsar-dim); color: var(--color-pulsar); }
.material-card--LINK   .material-icon { background: var(--color-orbit-dim);  color: var(--color-orbit); }
.material-card--EXERCICIO .material-icon { background: var(--color-flare-dim);  color: var(--color-flare); }

/* ── Content ── */
.material-content { flex: 1; min-width: 0; }

.material-title {
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-star);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.material-meta {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-top: var(--space-0-5);
}

.material-badge {
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  padding: 1px var(--space-1-5);
  border-radius: var(--radius-sm);
}

.material-card--PDF    .material-badge { background: var(--color-nova-dim);   color: var(--color-nova); }
.material-card--VIDEO  .material-badge { background: var(--color-pulsar-dim); color: var(--color-pulsar); }
.material-card--LINK   .material-badge { background: var(--color-orbit-dim);  color: var(--color-orbit); }
.material-card--EXERCICIO .material-badge { background: var(--color-flare-dim);  color: var(--color-flare); }

.material-size {
  font-size: var(--text-2xs);
  color: var(--color-dust);
}

/* ── Arrow ── */
.material-arrow {
  flex-shrink: 0;
  color: var(--color-border);
  transition: color var(--duration-fast) var(--ease-out);
}
.material-card:hover .material-arrow { color: var(--color-orbit); }
</style>

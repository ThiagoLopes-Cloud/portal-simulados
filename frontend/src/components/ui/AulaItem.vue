<template>
  <div class="aula-item" :class="{ 'aula-item--done': aula.is_completed }">
    <!-- Botão de conclusão -->
    <button
      type="button"
      class="aula-check"
      :class="{ 'aula-check--done': aula.is_completed }"
      :aria-label="aula.is_completed ? 'Marcar como não concluída' : 'Marcar como concluída'"
      :disabled="loading"
      @click="toggleConcluir"
    >
      <svg v-if="aula.is_completed" width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true">
        <path d="M2 6l3 3 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <svg v-else-if="loading" width="12" height="12" viewBox="0 0 12 12" fill="none" aria-hidden="true" class="aula-spinner">
        <circle cx="6" cy="6" r="4" stroke="currentColor" stroke-width="2" stroke-dasharray="12" stroke-dashoffset="4"/>
      </svg>
    </button>

    <!-- Info da aula -->
    <div class="aula-info">
      <p class="aula-title" :class="{ 'aula-title--done': aula.is_completed }">
        {{ aula.titulo }}
      </p>
      <div class="aula-meta">
        <span v-if="aula.duracao_minutos" class="aula-meta-item">
          <svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden="true">
            <circle cx="6" cy="6" r="5" stroke="currentColor" stroke-width="1.2"/>
            <path d="M6 3v3l2 1" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
          </svg>
          {{ aula.duracao_minutos }}min
        </span>
        <span v-if="aula.materiais?.length" class="aula-meta-item aula-meta-item--primary">
          <svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden="true">
            <path d="M2 2h8v8H2z" stroke="currentColor" stroke-width="1.2" rx="1"/>
            <path d="M4 5h4M4 7h3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/>
          </svg>
          {{ aula.materiais.length }} material{{ aula.materiais.length > 1 ? 'is' : '' }}
        </span>
      </div>
    </div>

    <!-- Link do vídeo -->
    <a
      v-if="aula.video_url"
      :href="aula.video_url"
      target="_blank"
      rel="noopener noreferrer"
      class="aula-play"
      :aria-label="`Assistir aula: ${aula.titulo}`"
      @click.stop
    >
      <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor" aria-hidden="true">
        <path d="M6 4l6 4-6 4V4z"/>
      </svg>
    </a>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { aulasService } from '../../services/aulasService.js'

const props = defineProps({
  aula: { type: Object, required: true },
})
const emit = defineEmits(['concluida'])

const loading = ref(false)

async function toggleConcluir() {
  if (props.aula.is_completed || loading.value) return
  loading.value = true
  try {
    const { data } = await aulasService.concluirAula(props.aula.id)
    emit('concluida', { aulaId: props.aula.id, ...data })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.aula-item {
  display: flex;
  align-items: flex-start;
  gap: var(--space-3);
  padding: var(--space-3);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  background: var(--color-bg-surface);
  transition:
    border-color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out);
}
.aula-item:hover { border-color: var(--color-orbit-border); }
.aula-item--done {
  border-color: var(--color-stellar-border);
  background: var(--color-stellar-dim);
}

/* ── Check button ── */
.aula-check {
  flex-shrink: 0;
  margin-top: 2px;
  width: 22px;
  height: 22px;
  border-radius: var(--radius-full);
  border: 2px solid var(--color-border);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: transparent;
  transition:
    border-color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out),
    color var(--duration-fast) var(--ease-out);
}
.aula-check:hover:not(:disabled) { border-color: var(--color-orbit); }
.aula-check:focus-visible { outline: none; box-shadow: var(--shadow-focus); }
.aula-check:disabled { opacity: 0.6; cursor: not-allowed; }
.aula-check--done {
  border-color: var(--color-stellar);
  background: var(--color-stellar);
  color: #fff;
}

@keyframes spin { to { transform: rotate(360deg); } }
.aula-spinner { animation: spin 0.8s linear infinite; color: var(--color-orbit); }

/* ── Info ── */
.aula-info { flex: 1; min-width: 0; }

.aula-title {
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  color: var(--color-star);
  line-height: var(--leading-snug);
}
.aula-title--done {
  color: var(--color-dust);
  text-decoration: line-through;
}

.aula-meta {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-top: var(--space-1);
}
.aula-meta-item {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-size: 11px;
  color: var(--color-dust);
}
.aula-meta-item--primary { color: var(--color-orbit); }

/* ── Play button ── */
.aula-play {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  background: var(--color-orbit-dim);
  color: var(--color-orbit);
  display: flex;
  align-items: center;
  justify-content: center;
  text-decoration: none;
  transition:
    background-color var(--duration-fast) var(--ease-out),
    color var(--duration-fast) var(--ease-out);
}
.aula-play:hover { background: var(--color-orbit); color: var(--color-cosmos); }
.aula-play:focus-visible { outline: none; box-shadow: var(--shadow-focus); }
</style>

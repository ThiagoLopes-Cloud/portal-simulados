<template>
  <div
    class="group flex items-start gap-3 p-3 rounded-xl border transition-all duration-200"
    :class="aula.is_completed
      ? 'border-emerald-200 bg-emerald-50'
      : 'border-slate-100 bg-white hover:border-simus-primary/30 hover:bg-indigo-50/40'"
  >
    <!-- Botão de conclusão -->
    <button
      type="button"
      class="shrink-0 mt-0.5 w-6 h-6 rounded-full border-2 flex items-center justify-center transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-simus-primary/50"
      :class="aula.is_completed
        ? 'border-emerald-500 bg-emerald-500 text-white'
        : 'border-slate-300 bg-white hover:border-simus-primary'"
      :aria-label="aula.is_completed ? 'Marcar como não concluída' : 'Marcar como concluída'"
      :disabled="loading"
      @click="toggleConcluir"
    >
      <svg v-if="aula.is_completed" class="w-3 h-3" fill="none" viewBox="0 0 12 12">
        <path d="M2 6l3 3 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      <svg v-else-if="loading" class="w-3 h-3 animate-spin" fill="none" viewBox="0 0 12 12">
        <circle cx="6" cy="6" r="4" stroke="currentColor" stroke-width="2" stroke-dasharray="12" stroke-dashoffset="4"/>
      </svg>
    </button>

    <!-- Info da aula -->
    <div class="flex-1 min-w-0">
      <p
        class="text-sm font-body font-medium leading-snug"
        :class="aula.is_completed ? 'text-simus-muted line-through' : 'text-simus-text'"
      >
        {{ aula.titulo }}
      </p>
      <div class="flex items-center gap-2 mt-1">
        <span v-if="aula.duracao_minutos" class="text-[11px] text-simus-muted flex items-center gap-1">
          <svg class="w-3 h-3" fill="none" viewBox="0 0 12 12"><circle cx="6" cy="6" r="5" stroke="currentColor" stroke-width="1.2"/><path d="M6 3v3l2 1" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
          {{ aula.duracao_minutos }}min
        </span>
        <span v-if="aula.materiais?.length" class="text-[11px] text-simus-primary flex items-center gap-1">
          <svg class="w-3 h-3" fill="none" viewBox="0 0 12 12"><path d="M2 2h8v8H2z" stroke="currentColor" stroke-width="1.2" rx="1"/><path d="M4 5h4M4 7h3" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>
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
      class="shrink-0 w-8 h-8 rounded-lg bg-simus-primary/10 flex items-center justify-center text-simus-primary hover:bg-simus-primary hover:text-white transition-colors duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-simus-primary/50"
      :aria-label="`Assistir aula: ${aula.titulo}`"
      @click.stop
    >
      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 16 16">
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
    // SUGESTÃO: disparar confete aqui quando data.modulo_completo === true
    // import confetti from 'canvas-confetti'; confetti({ particleCount: 120, spread: 70 })
    // SUGESTÃO: exibir toast "+10 XP ⚡" quando data.xp_ganho > 0
  } finally {
    loading.value = false
  }
}
</script>

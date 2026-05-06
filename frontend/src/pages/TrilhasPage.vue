<template>
  <DashboardLayout :username="username" :is-admin="isAdmin">

    <!-- Header -->
    <section class="px-4 pt-6 pb-4 md:px-8 md:pt-8">
      <div class="flex items-start justify-between gap-4">
        <div>
          <h1 class="font-display font-bold text-2xl md:text-3xl text-simus-text">
            Trilhas de Evolução
          </h1>
          <p class="text-simus-muted text-sm mt-1 font-body">
            Aprenda no seu ritmo. Cada aula concluída te aproxima do resultado.
          </p>
        </div>
        <!-- XP total badge -->
        <div v-if="totalConcluidas > 0"
          class="shrink-0 flex flex-col items-center justify-center w-16 h-16 rounded-2xl bg-simus-primary/10 border border-simus-primary/20">
          <span class="text-lg font-display font-bold text-simus-primary">{{ totalConcluidas }}</span>
          <span class="text-[10px] text-simus-muted uppercase tracking-wider">aulas</span>
        </div>
      </div>

      <!-- Barra de progresso geral -->
      <div v-if="totalAulas > 0" class="mt-5 space-y-1.5">
        <div class="flex justify-between text-xs text-simus-muted font-body">
          <span>Progresso geral</span>
          <span class="font-semibold text-simus-text">{{ totalConcluidas }}/{{ totalAulas }} aulas concluídas</span>
        </div>
        <div class="h-2.5 w-full bg-slate-100 rounded-full overflow-hidden">
          <div
            class="h-full rounded-full bg-gradient-to-r from-simus-primary to-indigo-400 transition-all duration-1000"
            :style="{ width: `${percentualGeral}%` }"
          />
        </div>
      </div>
    </section>

    <!-- Loading state -->
    <div v-if="carregando" class="px-4 md:px-8 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 pb-24">
      <div v-for="i in 6" :key="i" class="h-48 rounded-2xl bg-slate-100 animate-pulse" />
    </div>

    <!-- Empty state -->
    <div v-else-if="!trilhas.length" class="flex flex-col items-center justify-center py-20 px-4 text-center">
      <div class="w-14 h-14 rounded-2xl bg-indigo-50 flex items-center justify-center mb-4 text-indigo-400">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>
        </svg>
      </div>
      <p class="font-display font-semibold text-simus-text text-lg">Nenhuma trilha disponível ainda</p>
      <p class="text-simus-muted text-sm mt-1">O professor está preparando o conteúdo para você.</p>
    </div>

    <!-- Grid de trilhas (Netflix-style) -->
    <section v-else class="px-4 md:px-8 pb-24">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <TrilhaCard
          v-for="trilha in trilhas"
          :key="trilha.id"
          :trilha="trilha"
          @click="abrirTrilha(trilha)"
        />
      </div>
    </section>

    <!-- Bottom Sheet / Modal de detalhe da Trilha -->
    <Transition name="sheet">
      <div
        v-if="trilhaSelecionada"
        class="fixed inset-0 z-40 flex flex-col justify-end md:items-center md:justify-center"
        @click.self="fecharTrilha"
      >
        <!-- Overlay -->
        <div class="absolute inset-0 bg-black/40 backdrop-blur-sm" @click="fecharTrilha" />

        <!-- Painel -->
        <div
          class="relative z-10 w-full md:max-w-2xl bg-white rounded-t-3xl md:rounded-2xl max-h-[85vh] flex flex-col shadow-2xl"
        >
          <!-- Handle bar (mobile) -->
          <div class="flex justify-center pt-3 pb-1 md:hidden">
            <div class="w-10 h-1.5 rounded-full bg-slate-200" />
          </div>

          <!-- Header do painel -->
          <div
            class="flex items-center gap-3 px-5 py-4 border-b border-slate-100"
            :style="{ background: `linear-gradient(135deg, ${trilhaSelecionada.cor}11, ${trilhaSelecionada.cor}22)` }"
          >
            <span class="text-3xl">{{ trilhaSelecionada.icone }}</span>
            <div class="flex-1 min-w-0">
              <h2 class="font-display font-bold text-lg text-simus-text truncate">{{ trilhaSelecionada.nome }}</h2>
              <p class="text-xs text-simus-muted">{{ trilhaSelecionada.percentual_progresso }}% completo</p>
            </div>
            <button
              class="w-8 h-8 rounded-full bg-slate-100 flex items-center justify-center text-simus-muted hover:bg-slate-200 transition-colors"
              @click="fecharTrilha"
              aria-label="Fechar"
            >
              <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
                <path d="M12 4L4 12M4 4l8 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <!-- Lista de módulos e aulas -->
          <div class="flex-1 overflow-y-auto px-5 py-4 space-y-5">
            <div v-if="carregandoDetalhe" class="space-y-3">
              <div v-for="i in 4" :key="i" class="h-12 rounded-xl bg-slate-100 animate-pulse" />
            </div>

            <template v-else-if="trilhaDetalhe">
              <div v-for="modulo in trilhaDetalhe.modulos" :key="modulo.id" class="space-y-2">
                <!-- Cabeçalho do módulo -->
                <div class="flex items-center justify-between">
                  <h3 class="font-display font-semibold text-sm text-simus-text">{{ modulo.nome }}</h3>
                  <span class="text-xs text-simus-muted">
                    {{ modulo.aulas_concluidas }}/{{ modulo.total_aulas }}
                  </span>
                </div>

                <!-- Aulas do módulo -->
                <div class="space-y-1.5">
                  <AulaItem
                    v-for="aula in modulo.aulas"
                    :key="aula.id"
                    :aula="aula"
                    @concluida="onAulaConcluida($event, modulo)"
                  />
                </div>

                <!-- Materiais do módulo -->
                <div v-if="modulo.materiais?.length" class="mt-3 space-y-1.5">
                  <p class="text-[11px] font-bold uppercase tracking-widest text-simus-muted px-1">Arsenal do Módulo</p>
                  <MaterialCard
                    v-for="mat in modulo.materiais"
                    :key="mat.id"
                    :material="mat"
                  />
                </div>
              </div>
            </template>
          </div>
        </div>
      </div>
    </Transition>

  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import TrilhaCard from '../components/ui/TrilhaCard.vue'
import AulaItem from '../components/ui/AulaItem.vue'
import MaterialCard from '../components/ui/MaterialCard.vue'
import { aulasService } from '../services/aulasService.js'

const username = localStorage.getItem('username') || ''
const isAdmin = localStorage.getItem('user_role') === 'admin'

const trilhas = ref([])
const carregando = ref(true)
const trilhaSelecionada = ref(null)
const trilhaDetalhe = ref(null)
const carregandoDetalhe = ref(false)

const totalAulas = computed(() => trilhas.value.reduce((acc, t) => acc + (t.total_aulas || 0), 0))
const totalConcluidas = computed(() => trilhas.value.reduce((acc, t) => acc + (t.aulas_concluidas || 0), 0))
const percentualGeral = computed(() =>
  totalAulas.value > 0 ? Math.round((totalConcluidas.value / totalAulas.value) * 100) : 0
)

onMounted(async () => {
  try {
    const { data } = await aulasService.listarTrilhas()
    trilhas.value = data
  } catch (e) {
    console.error(e)
  } finally {
    carregando.value = false
  }
})

async function abrirTrilha(trilha) {
  trilhaSelecionada.value = trilha
  carregandoDetalhe.value = true
  trilhaDetalhe.value = null
  try {
    const { data } = await aulasService.detalharTrilha(trilha.id)
    trilhaDetalhe.value = data
  } catch (e) {
    console.error(e)
  } finally {
    carregandoDetalhe.value = false
  }
}

function fecharTrilha() {
  trilhaSelecionada.value = null
  trilhaDetalhe.value = null
}

function onAulaConcluida({ aulaId, modulo_completo, xp_ganho }, modulo) {
  // Atualiza estado local sem re-fetch
  if (trilhaDetalhe.value) {
    for (const mod of trilhaDetalhe.value.modulos) {
      const aula = mod.aulas.find((a) => a.id === aulaId)
      if (aula) {
        aula.is_completed = true
        mod.aulas_concluidas = (mod.aulas_concluidas || 0) + 1
        break
      }
    }
    // Atualiza progresso na lista
    const trilha = trilhas.value.find((t) => t.id === trilhaSelecionada.value.id)
    if (trilha) {
      trilha.aulas_concluidas = (trilha.aulas_concluidas || 0) + 1
      trilha.percentual_progresso = Math.round(
        (trilha.aulas_concluidas / trilha.total_aulas) * 100
      )
      trilhaSelecionada.value = { ...trilha }
    }
  }
  // SUGESTÃO: se modulo_completo, disparar confete
  // import confetti from 'canvas-confetti'; if (modulo_completo) confetti({ particleCount: 150, spread: 80, origin: { y: 0.6 } })
}
</script>

<style scoped>
.sheet-enter-active, .sheet-leave-active { transition: opacity 0.25s ease; }
.sheet-enter-from, .sheet-leave-to { opacity: 0; }
.sheet-enter-active .relative.z-10,
.sheet-leave-active .relative.z-10 { transition: transform 0.3s cubic-bezier(0.32, 0.72, 0, 1); }
.sheet-enter-from .relative.z-10,
.sheet-leave-to .relative.z-10 { transform: translateY(100%); }
@media (min-width: 768px) {
  .sheet-enter-from .relative.z-10,
  .sheet-leave-to .relative.z-10 { transform: scale(0.95) translateY(20px); }
}
</style>

<template>
  <DashboardLayout :username="username" :is-admin="isAdmin">

    <!-- Header -->
    <header class="trilhas-header">
      <div class="trilhas-header-left">
        <h1 class="trilhas-title">Trilhas de Evolução</h1>
        <p class="trilhas-sub">Aprenda no seu ritmo. Cada aula concluída te aproxima do resultado.</p>
      </div>
      <div v-if="totalConcluidas > 0" class="trilhas-xp-badge" aria-label="Aulas concluídas">
        <span class="trilhas-xp-value">{{ totalConcluidas }}</span>
        <span class="trilhas-xp-label">aulas</span>
      </div>
    </header>

    <!-- Barra de progresso geral -->
    <SimuslabProgress
      v-if="totalAulas > 0"
      :value="totalConcluidas"
      :max="totalAulas"
      label="Progresso geral"
      show-value
      color="orbit"
      size="md"
      class="trilhas-progress-wrap"
    />

    <!-- Loading state -->
    <div v-if="carregando" class="trilhas-grid">
      <SimuslabSkeleton v-for="i in 6" :key="i" variant="rect" height="140px" />
    </div>

    <!-- Empty state -->
    <SimuslabEmptyState
      v-else-if="!trilhas.length"
      icon="book"
      title="Nenhuma trilha disponível ainda"
      description="O professor está preparando o conteúdo para você."
      color="orbit"
      card
    />

    <!-- Grid de trilhas -->
    <section v-else class="trilhas-grid">
      <TrilhaCard
        v-for="trilha in trilhas"
        :key="trilha.id"
        :trilha="trilha"
        @click="abrirTrilha(trilha)"
      />
    </section>

    <!-- Bottom Sheet / Modal de detalhe da Trilha -->
    <Transition name="sheet">
      <div
        v-if="trilhaSelecionada"
        class="sheet-backdrop"
        @click.self="fecharTrilha"
      >
        <div class="sheet-overlay" @click="fecharTrilha" />

        <!-- Painel -->
        <div class="sheet-panel" role="dialog" :aria-label="trilhaSelecionada.nome">
          <!-- Handle bar (mobile) -->
          <div class="sheet-handle" aria-hidden="true">
            <div class="sheet-handle-bar" />
          </div>

          <!-- Header do painel -->
          <div
            class="sheet-header"
            :style="{ background: `linear-gradient(135deg, ${trilhaSelecionada.cor}11, ${trilhaSelecionada.cor}22)` }"
          >
            <span class="sheet-emoji" aria-hidden="true">{{ trilhaSelecionada.icone }}</span>
            <div class="sheet-header-info">
              <h2 class="sheet-title">{{ trilhaSelecionada.nome }}</h2>
              <p class="sheet-sub">{{ trilhaSelecionada.percentual_progresso }}% completo</p>
            </div>
            <button class="sheet-close" @click="fecharTrilha" aria-label="Fechar">
              <svg width="14" height="14" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                <path d="M12 4L4 12M4 4l8 8" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
              </svg>
            </button>
          </div>

          <!-- Lista de módulos e aulas -->
          <div class="sheet-body">
            <div v-if="carregandoDetalhe" class="sheet-loading">
              <SimuslabSkeleton v-for="i in 4" :key="i" variant="rect" height="52px" />
            </div>

            <template v-else-if="trilhaDetalhe">
              <div v-for="modulo in trilhaDetalhe.modulos" :key="modulo.id" class="modulo-block">
                <div class="modulo-header">
                  <h3 class="modulo-title">{{ modulo.nome }}</h3>
                  <span class="modulo-count">{{ modulo.aulas_concluidas }}/{{ modulo.total_aulas }}</span>
                </div>

                <div class="modulo-aulas">
                  <AulaItem
                    v-for="aula in modulo.aulas"
                    :key="aula.id"
                    :aula="aula"
                    @concluida="onAulaConcluida($event, modulo)"
                  />
                </div>

                <div v-if="modulo.materiais?.length" class="modulo-materiais">
                  <p class="materiais-label">Arsenal do Módulo</p>
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
import DashboardLayout    from '../layouts/DashboardLayout.vue'
import TrilhaCard         from '../components/ui/TrilhaCard.vue'
import AulaItem           from '../components/ui/AulaItem.vue'
import MaterialCard       from '../components/ui/MaterialCard.vue'
import SimuslabProgress   from '../components/ui/SimuslabProgress.vue'
import SimuslabSkeleton   from '../components/ui/SimuslabSkeleton.vue'
import SimuslabEmptyState from '../components/ui/SimuslabEmptyState.vue'
import { aulasService }   from '../services/aulasService.js'

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

function onAulaConcluida({ aulaId, modulo_completo }, modulo) {
  if (trilhaDetalhe.value) {
    for (const mod of trilhaDetalhe.value.modulos) {
      const aula = mod.aulas.find((a) => a.id === aulaId)
      if (aula) {
        aula.is_completed = true
        mod.aulas_concluidas = (mod.aulas_concluidas || 0) + 1
        break
      }
    }
    const trilha = trilhas.value.find((t) => t.id === trilhaSelecionada.value.id)
    if (trilha) {
      trilha.aulas_concluidas = (trilha.aulas_concluidas || 0) + 1
      trilha.percentual_progresso = Math.round(
        (trilha.aulas_concluidas / trilha.total_aulas) * 100
      )
      trilhaSelecionada.value = { ...trilha }
    }
  }
}
</script>

<style scoped>
/* ── Header ── */
.trilhas-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  margin-bottom: var(--space-5);
}
.trilhas-title {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  margin-bottom: var(--space-1);
}
.trilhas-sub { font-size: var(--text-sm); color: var(--color-comet); }

.trilhas-xp-badge {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: var(--radius-xl);
  background: var(--color-orbit-dim);
  border: 1px solid var(--color-orbit-border);
}
.trilhas-xp-value {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  color: var(--color-orbit);
  line-height: 1;
}
.trilhas-xp-label {
  font-size: var(--text-2xs);
  color: var(--color-comet);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
}

/* ── Global progress ── */
.trilhas-progress-wrap {
  margin-bottom: var(--space-6);
  display: flex;
  flex-direction: column;
  gap: var(--space-1-5);
}
/* progress bar → SimuslabProgress */

/* ── Grid ── */
.trilhas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-4);
  padding-bottom: var(--space-12, 48px);
}

/* skeleton + empty state → SimuslabSkeleton / SimuslabEmptyState */

/* ── Sheet ── */
.sheet-backdrop {
  position: fixed;
  inset: 0;
  z-index: var(--z-modal, 200);
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}
@media (min-width: 768px) {
  .sheet-backdrop { align-items: center; justify-content: center; }
}

.sheet-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  -webkit-backdrop-filter: blur(4px);
}

.sheet-panel {
  position: relative;
  z-index: 1;
  width: 100%;
  background: var(--color-bg-surface);
  border-radius: var(--radius-2xl, 24px) var(--radius-2xl, 24px) 0 0;
  max-height: 85vh;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-xl);
  border: 1px solid var(--color-border);
}
@media (min-width: 768px) {
  .sheet-panel {
    max-width: 640px;
    border-radius: var(--radius-xl);
    max-height: 80vh;
  }
}

.sheet-handle {
  display: flex;
  justify-content: center;
  padding: var(--space-3) var(--space-4) var(--space-1);
}
@media (min-width: 768px) { .sheet-handle { display: none; } }
.sheet-handle-bar {
  width: 40px;
  height: 5px;
  border-radius: var(--radius-full);
  background: var(--color-border);
}

.sheet-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4) var(--space-5);
  border-bottom: 1px solid var(--color-border);
}
.sheet-emoji { font-size: 1.875rem; line-height: 1; }
.sheet-header-info { flex: 1; min-width: 0; }
.sheet-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin: 0;
}
.sheet-sub { font-size: var(--text-xs); color: var(--color-comet); margin-top: 2px; }

.sheet-close {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background: var(--color-bg-elevated);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-comet);
  cursor: pointer;
  flex-shrink: 0;
  transition: background-color var(--duration-fast) var(--ease-out), color var(--duration-fast) var(--ease-out);
}
.sheet-close:hover { background: var(--color-surface-hover); color: var(--color-star); }
.sheet-close:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

.sheet-body {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.sheet-loading { display: flex; flex-direction: column; gap: var(--space-3); }

/* ── Module ── */
.modulo-block { display: flex; flex-direction: column; gap: var(--space-2); }

.modulo-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding-bottom: var(--space-1);
}
.modulo-title {
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-star);
  margin: 0;
}
.modulo-count { font-size: var(--text-xs); color: var(--color-dust); }

.modulo-aulas { display: flex; flex-direction: column; gap: var(--space-1-5); }

.modulo-materiais {
  margin-top: var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-1-5);
}
.materiais-label {
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-widest, 0.12em);
  color: var(--color-dust);
  padding: 0 var(--space-1);
}

/* ── Sheet transition ── */
.sheet-enter-active { transition: opacity var(--duration-normal) var(--ease-out); }
.sheet-leave-active { transition: opacity var(--duration-fast) var(--ease-in-out); }
.sheet-enter-from, .sheet-leave-to { opacity: 0; }

.sheet-enter-active .sheet-panel,
.sheet-leave-active .sheet-panel { transition: transform var(--duration-normal) cubic-bezier(0.32, 0.72, 0, 1); }
.sheet-enter-from .sheet-panel,
.sheet-leave-to .sheet-panel { transform: translateY(100%); }
@media (min-width: 768px) {
  .sheet-enter-from .sheet-panel,
  .sheet-leave-to .sheet-panel { transform: scale(0.95) translateY(20px); }
}
</style>

<template>
  <DashboardLayout :username="username" :is-admin="isAdmin">

    <!-- Loading -->
    <div v-if="loading" class="td-loading">
      <SimuslabSkeleton variant="rect" height="56px" />
      <div class="td-layout">
        <div style="display:flex;flex-direction:column;gap:var(--space-4)">
          <SimuslabSkeleton variant="rect" style="aspect-ratio:16/9;width:100%" />
          <SimuslabSkeleton variant="rect" height="80px" />
        </div>
        <div style="display:flex;flex-direction:column;gap:var(--space-3)">
          <SimuslabSkeleton v-for="i in 5" :key="i" variant="rect" height="48px" />
        </div>
      </div>
    </div>

    <!-- Error -->
    <SimuslabEmptyState
      v-else-if="error"
      icon="error"
      title="Trilha não encontrada"
      description="Verifique se o link está correto ou volte para a lista de trilhas."
      color="nova"
      card
    >
      <template #action>
        <button class="td-back-btn" @click="$router.push('/trilhas')">← Voltar para Trilhas</button>
      </template>
    </SimuslabEmptyState>

    <template v-else-if="trilha">

      <!-- Breadcrumb -->
      <nav class="td-breadcrumb" aria-label="Navegação">
        <button class="td-back-btn" @click="$router.push('/trilhas')" aria-label="Voltar para trilhas">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="15 18 9 12 15 6"/></svg>
          Trilhas
        </button>
        <span class="td-breadcrumb-sep" aria-hidden="true">/</span>
        <span class="td-breadcrumb-current">{{ trilha.nome }}</span>
      </nav>

      <!-- Hero strip -->
      <div class="td-hero" :style="{ '--trilha-cor': trilha.cor || 'var(--color-orbit)' }">
        <span class="td-hero-icon" aria-hidden="true">{{ trilha.icone }}</span>
        <div class="td-hero-info">
          <h1 class="td-hero-title">{{ trilha.nome }}</h1>
          <div class="td-hero-meta">
            <span class="td-hero-stat">
              <svg width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true"><circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/><path d="M6 5.5l5 2.5-5 2.5V5.5z" fill="currentColor"/></svg>
              {{ totalAulas }} aulas
            </span>
            <span class="td-hero-sep" aria-hidden="true">·</span>
            <span class="td-hero-stat">
              <svg width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true"><rect x="2" y="2" width="5" height="5" rx="1" fill="currentColor"/><rect x="9" y="2" width="5" height="5" rx="1" fill="currentColor"/><rect x="2" y="9" width="5" height="5" rx="1" fill="currentColor"/><rect x="9" y="9" width="5" height="5" rx="1" fill="currentColor" opacity=".4"/></svg>
              {{ trilha.modulos?.length || 0 }} módulos
            </span>
            <span v-if="tempoTotalMin > 0" class="td-hero-sep" aria-hidden="true">·</span>
            <span v-if="tempoTotalMin > 0" class="td-hero-stat">
              <svg width="13" height="13" viewBox="0 0 16 16" fill="none" aria-hidden="true"><circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/><path d="M8 4v4l2.5 1.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>
              {{ tempoFormatado }}
            </span>
          </div>
        </div>
        <div class="td-hero-progress">
          <span class="td-hero-pct">{{ progressPercent }}%</span>
          <div class="td-hero-bar" role="progressbar" :aria-valuenow="progressPercent" aria-valuemin="0" aria-valuemax="100">
            <div class="td-hero-bar-fill" :style="{ width: `${progressPercent}%` }" />
          </div>
          <span class="td-hero-pct-label">{{ aulasConcluidas }}/{{ totalAulas }} concluídas</span>
        </div>
      </div>

      <!-- Content layout -->
      <div class="td-layout">

        <!-- ── Main (video + controles) ── -->
        <main class="td-main">

          <!-- Video player -->
          <SimuslabVideoPlayer
            v-if="aulaAtual"
            :url="aulaAtual.video_url"
            :title="aulaAtual.titulo"
            :duration="aulaAtual.duracao_minutos"
            :aula-id="aulaAtual.id"
            :watched="isWatched(aulaAtual.id)"
            :accent="trilha.cor || '#00E5FF'"
            @play="onPlay"
          />
          <div v-else class="td-no-aula">
            <SimuslabEmptyState icon="done" title="Trilha concluída!" description="Você completou todas as aulas desta trilha." color="stellar" />
          </div>

          <!-- Aula info + navegação -->
          <div v-if="aulaAtual" class="td-aula-info">
            <div class="td-aula-header">
              <div class="td-aula-header-text">
                <h2 class="td-aula-title">{{ aulaAtual.titulo }}</h2>
                <p class="td-aula-meta">
                  {{ moduloDoAtual?.nome }}
                  <span v-if="aulaAtual.duracao_minutos"> · {{ aulaAtual.duracao_minutos }}min</span>
                </p>
              </div>

              <!-- Marcar concluída -->
              <button
                class="td-conclude-btn"
                :class="{ 'td-conclude-btn--done': aulaAtual.is_completed, 'td-conclude-btn--loading': concluding }"
                :disabled="aulaAtual.is_completed || concluding"
                @click="marcarConcluida"
                :aria-label="aulaAtual.is_completed ? 'Aula concluída' : 'Marcar como concluída'"
              >
                <svg v-if="aulaAtual.is_completed" width="14" height="14" viewBox="0 0 12 12" fill="none" aria-hidden="true">
                  <path d="M2 6l3 3 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span v-else-if="concluding" class="td-spinner" aria-hidden="true" />
                <svg v-else width="14" height="14" viewBox="0 0 12 12" fill="none" aria-hidden="true">
                  <circle cx="6" cy="6" r="5" stroke="currentColor" stroke-width="1.5"/>
                  <path d="M2 6l3 3 5-5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                {{ aulaAtual.is_completed ? 'Concluída' : concluding ? 'Salvando…' : 'Marcar como concluída' }}
              </button>
            </div>

            <!-- Prev / Next navigation -->
            <div class="td-nav-btns">
              <button
                class="td-nav-btn"
                :disabled="!aulaPrev"
                @click="selecionarAula(aulaPrev)"
                :aria-label="aulaPrev ? `Aula anterior: ${aulaPrev.titulo}` : 'Sem aula anterior'"
              >
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><polyline points="15 18 9 12 15 6"/></svg>
                <span class="td-nav-btn-text">
                  <span class="td-nav-btn-label">Anterior</span>
                  <span class="td-nav-btn-name">{{ aulaPrev?.titulo || '—' }}</span>
                </span>
              </button>
              <button
                class="td-nav-btn td-nav-btn--next"
                :disabled="!aulaNext"
                @click="selecionarAula(aulaNext)"
                :aria-label="aulaNext ? `Próxima aula: ${aulaNext.titulo}` : 'Sem próxima aula'"
              >
                <span class="td-nav-btn-text">
                  <span class="td-nav-btn-label">Próxima</span>
                  <span class="td-nav-btn-name">{{ aulaNext?.titulo || 'Trilha completa' }}</span>
                </span>
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><polyline points="9 18 15 12 9 6"/></svg>
              </button>
            </div>
          </div>

          <!-- XP gain toast -->
          <Transition name="xp-pop">
            <div v-if="xpToast.show" class="td-xp-toast" role="status" aria-live="polite">
              <span class="td-xp-toast-gain">+{{ xpToast.gained }} XP</span>
              <span v-if="xpToast.leveled" class="td-xp-toast-level">Nível {{ xpToast.newLevel }}!</span>
            </div>
          </Transition>

        </main>

        <!-- ── Sidebar ── -->
        <aside class="td-sidebar" :class="{ 'td-sidebar--open': sidebarOpen }">

          <!-- Mobile toggle button -->
          <button class="td-sidebar-toggle" @click="sidebarOpen = !sidebarOpen" :aria-expanded="sidebarOpen">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true">
              <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
            </svg>
            {{ sidebarOpen ? 'Ocultar conteúdo' : 'Ver conteúdo da trilha' }}
            <span class="td-sidebar-toggle-count">{{ aulasConcluidas }}/{{ totalAulas }}</span>
          </button>

          <div class="td-sidebar-content">

            <!-- XP widget -->
            <div class="td-xp-widget">
              <div class="td-xp-header">
                <span class="td-xp-level">Nível {{ userLevel }}</span>
                <span class="td-xp-total">{{ xpData.xp }} XP</span>
              </div>
              <div class="td-xp-bar" role="progressbar" :aria-valuenow="xpBarPercent" aria-valuemin="0" aria-valuemax="100">
                <div class="td-xp-bar-fill" :style="{ width: `${xpBarPercent}%` }" />
              </div>
              <p class="td-xp-hint">{{ xpToNext }} XP para nível {{ userLevel + 1 }}</p>
            </div>

            <!-- Modules tree -->
            <div class="td-modules" role="list">
              <div
                v-for="modulo in trilha.modulos"
                :key="modulo.id"
                class="td-module"
                role="listitem"
              >
                <button
                  class="td-module-header"
                  :class="{ 'td-module-header--done': moduloConcluido(modulo) }"
                  :aria-expanded="!collapsedModules[modulo.id]"
                  @click="toggleModule(modulo.id)"
                >
                  <div class="td-module-check" :class="{ 'td-module-check--done': moduloConcluido(modulo) }">
                    <svg v-if="moduloConcluido(modulo)" width="10" height="10" viewBox="0 0 12 12" fill="none" aria-hidden="true">
                      <path d="M2 6l3 3 5-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </div>
                  <span class="td-module-name">{{ modulo.nome }}</span>
                  <span class="td-module-count">{{ modulo.aulas_concluidas }}/{{ modulo.total_aulas }}</span>
                  <svg
                    width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                    stroke-width="2.5" stroke-linecap="round" aria-hidden="true"
                    :class="['td-module-caret', { 'td-module-caret--open': !collapsedModules[modulo.id] }]"
                  ><polyline points="6 9 12 15 18 9"/></svg>
                </button>

                <div v-show="!collapsedModules[modulo.id]" class="td-module-aulas">
                  <button
                    v-for="aula in modulo.aulas"
                    :key="aula.id"
                    class="td-aula-btn"
                    :class="{
                      'td-aula-btn--active': aulaAtual?.id === aula.id,
                      'td-aula-btn--done':   aula.is_completed,
                    }"
                    @click="selecionarAula(aula)"
                    :aria-current="aulaAtual?.id === aula.id ? 'step' : undefined"
                  >
                    <span class="td-aula-btn-check" aria-hidden="true">
                      <svg v-if="aula.is_completed" width="9" height="9" viewBox="0 0 12 12" fill="none">
                        <path d="M2 6l3 3 5-5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      <span v-else-if="aulaAtual?.id === aula.id" class="td-aula-btn-dot" />
                    </span>
                    <span class="td-aula-btn-name">{{ aula.titulo }}</span>
                    <span v-if="aula.duracao_minutos" class="td-aula-btn-dur">{{ aula.duracao_minutos }}m</span>
                  </button>
                </div>
              </div>
            </div>

          </div>
        </aside>

      </div>
    </template>

  </DashboardLayout>
</template>

<script setup>
import { ref, computed, reactive, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import DashboardLayout       from '../layouts/DashboardLayout.vue'
import SimuslabVideoPlayer   from '../components/ui/SimuslabVideoPlayer.vue'
import SimuslabSkeleton      from '../components/ui/SimuslabSkeleton.vue'
import SimuslabEmptyState    from '../components/ui/SimuslabEmptyState.vue'
import { aulasService }      from '../services/aulasService.js'
import {
  getXPData, getLevelFromXP, getNextLevelXP, getCurrentLevelXP,
  addAulaXP, getLastViewedAula, setLastViewedAula,
} from '../utils/gamification.js'

const route  = useRoute()
const router = useRouter()

const username = localStorage.getItem('username') || ''
const isAdmin  = localStorage.getItem('user_role') === 'admin'

const trilha        = ref(null)
const loading       = ref(true)
const error         = ref(false)
const aulaAtual     = ref(null)
const concluding    = ref(false)
const sidebarOpen   = ref(false)
const watchedSet    = reactive(new Set())
const collapsedModules = reactive({})

const xpData = ref(getXPData())
const xpToast = reactive({ show: false, gained: 0, leveled: false, newLevel: 1 })

// ── XP ──────────────────────────────────────────────────────────
const userLevel   = computed(() => getLevelFromXP(xpData.value.xp))
const nextLevelXP = computed(() => getNextLevelXP(userLevel.value))
const curLevelXP  = computed(() => getCurrentLevelXP(userLevel.value))
const xpInLevel   = computed(() => xpData.value.xp - curLevelXP.value)
const xpLevelRange = computed(() => nextLevelXP.value - curLevelXP.value)
const xpBarPercent = computed(() => Math.round((xpInLevel.value / xpLevelRange.value) * 100))
const xpToNext     = computed(() => nextLevelXP.value - xpData.value.xp)

// ── Computed from trilha data ────────────────────────────────────
const todasAulas = computed(() => {
  if (!trilha.value) return []
  return trilha.value.modulos.flatMap((m) => m.aulas)
})

const totalAulas     = computed(() => todasAulas.value.length)
const aulasConcluidas = computed(() => todasAulas.value.filter((a) => a.is_completed).length)
const progressPercent = computed(() =>
  totalAulas.value > 0 ? Math.round((aulasConcluidas.value / totalAulas.value) * 100) : 0
)

const tempoTotalMin = computed(() =>
  todasAulas.value.reduce((s, a) => s + (a.duracao_minutos || 0), 0)
)
const tempoFormatado = computed(() => {
  const h = Math.floor(tempoTotalMin.value / 60)
  const m = tempoTotalMin.value % 60
  return h > 0 ? `${h}h${m > 0 ? ` ${m}min` : ''}` : `${m}min`
})

const moduloDoAtual = computed(() => {
  if (!aulaAtual.value || !trilha.value) return null
  return trilha.value.modulos.find((m) => m.aulas.some((a) => a.id === aulaAtual.value.id))
})

const aulaIndex = computed(() => todasAulas.value.findIndex((a) => a.id === aulaAtual.value?.id))
const aulaPrev  = computed(() => aulaIndex.value > 0 ? todasAulas.value[aulaIndex.value - 1] : null)
const aulaNext  = computed(() => aulaIndex.value < todasAulas.value.length - 1 ? todasAulas.value[aulaIndex.value + 1] : null)

// ── Helpers ──────────────────────────────────────────────────────
function isWatched(aulaId) { return watchedSet.has(aulaId) }
function moduloConcluido(modulo) {
  return modulo.total_aulas > 0 && modulo.aulas_concluidas >= modulo.total_aulas
}

function toggleModule(id) {
  collapsedModules[id] = !collapsedModules[id]
}

function selecionarAula(aula) {
  if (!aula) return
  aulaAtual.value = aula
  setLastViewedAula(route.params.id, aula.id)
  sidebarOpen.value = false
}

function primeiraAulaNaoConcluida() {
  return todasAulas.value.find((a) => !a.is_completed) ?? todasAulas.value[0] ?? null
}

function onPlay(aulaId) {
  watchedSet.add(aulaId)
}

// ── Marcar concluída ─────────────────────────────────────────────
async function marcarConcluida() {
  if (!aulaAtual.value || aulaAtual.value.is_completed || concluding.value) return
  concluding.value = true
  try {
    await aulasService.concluirAula(aulaAtual.value.id)
    aulaAtual.value.is_completed = true

    // update modulo counter
    const mod = moduloDoAtual.value
    if (mod) mod.aulas_concluidas = (mod.aulas_concluidas || 0) + 1

    // XP
    const result = addAulaXP(aulaAtual.value.id)
    xpData.value = result.data
    if (result.gained > 0) {
      Object.assign(xpToast, { show: true, gained: result.gained, leveled: result.leveled, newLevel: result.newLevel })
      setTimeout(() => { xpToast.show = false }, 2800)
    }

    // auto-advance
    if (aulaNext.value) {
      setTimeout(() => selecionarAula(aulaNext.value), 1200)
    }
  } catch (e) {
    console.error(e)
  } finally {
    concluding.value = false
  }
}

// ── Load ─────────────────────────────────────────────────────────
onMounted(async () => {
  try {
    const { data } = await aulasService.detalharTrilha(route.params.id)
    trilha.value = data

    // Expand all modules by default
    data.modulos?.forEach((m) => { collapsedModules[m.id] = false })

    // Select aula: last viewed > first uncompleted > first
    const lastId = getLastViewedAula(route.params.id)
    const found  = lastId ? todasAulas.value.find((a) => a.id === lastId) : null
    aulaAtual.value = found ?? primeiraAulaNaoConcluida()
  } catch {
    error.value = true
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
/* ── Loading ── */
.td-loading {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

/* ── Back button ── */
.td-back-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1-5);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  color: var(--color-comet);
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
  transition: color var(--duration-fast) var(--ease-out);
}
.td-back-btn:hover { color: var(--color-star); }
.td-back-btn:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

/* ── Breadcrumb ── */
.td-breadcrumb {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
}
.td-breadcrumb-sep  { color: var(--color-border-hover); font-size: var(--text-sm); }
.td-breadcrumb-current {
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-star);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 280px;
}

/* ── Hero ── */
.td-hero {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4) var(--space-5);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-left: 3px solid var(--trilha-cor);
  border-radius: var(--radius-xl);
  margin-bottom: var(--space-5);
  flex-wrap: wrap;
  gap: var(--space-3);
}

.td-hero-icon {
  font-size: 2rem;
  line-height: 1;
  flex-shrink: 0;
}

.td-hero-info { flex: 1; min-width: 180px; }

.td-hero-title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  margin: 0 0 var(--space-1);
  line-height: var(--leading-tight);
}

.td-hero-meta {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-2);
}
.td-hero-stat {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--text-xs);
  color: var(--color-comet);
}
.td-hero-sep { color: var(--color-border-hover); font-size: var(--text-xs); }

.td-hero-progress {
  display: flex;
  flex-direction: column;
  gap: var(--space-1-5);
  min-width: 120px;
}
.td-hero-pct {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: var(--weight-bold);
  color: var(--trilha-cor);
  line-height: 1;
}
.td-hero-bar {
  height: 6px;
  background: var(--color-bg-elevated);
  border-radius: var(--radius-full);
  overflow: hidden;
}
.td-hero-bar-fill {
  height: 100%;
  background: var(--trilha-cor);
  border-radius: var(--radius-full);
  transition: width var(--duration-slow) var(--ease-out);
}
.td-hero-pct-label {
  font-size: var(--text-2xs);
  color: var(--color-comet);
  white-space: nowrap;
}

/* ── Layout ── */
.td-layout {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: var(--space-5);
  align-items: start;
}

@media (max-width: 1024px) {
  .td-layout { grid-template-columns: 1fr 260px; }
}

@media (max-width: 768px) {
  .td-layout { grid-template-columns: 1fr; }
}

/* ── Main ── */
.td-main {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  min-width: 0;
}

.td-no-aula { padding: var(--space-8) 0; }

/* ── Aula info ── */
.td-aula-info {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
}

.td-aula-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
}

.td-aula-header-text { flex: 1; min-width: 0; }

.td-aula-title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  margin: 0 0 var(--space-1);
  line-height: var(--leading-tight);
}

.td-aula-meta {
  font-size: var(--text-sm);
  color: var(--color-comet);
  margin: 0;
}

/* ── Conclude button ── */
.td-conclude-btn {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  height: var(--btn-height-md);
  padding: 0 var(--space-4);
  border-radius: var(--btn-radius);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  cursor: pointer;
  flex-shrink: 0;
  transition:
    background-color var(--duration-fast) var(--ease-out),
    color var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out);
  background: var(--color-orbit-dim);
  border: 1px solid var(--color-orbit-border);
  color: var(--color-orbit);
}
.td-conclude-btn:hover:not(:disabled) {
  background: var(--color-orbit);
  color: var(--color-cosmos);
  border-color: var(--color-orbit);
}
.td-conclude-btn--done {
  background: var(--color-stellar-dim);
  border-color: var(--color-stellar-border);
  color: var(--color-stellar);
  cursor: default;
}
.td-conclude-btn:disabled { opacity: 0.65; cursor: not-allowed; }
.td-conclude-btn:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

@keyframes spin { to { transform: rotate(360deg); } }
.td-spinner {
  width: 13px;
  height: 13px;
  border: 2px solid currentColor;
  border-top-color: transparent;
  border-radius: var(--radius-full);
  animation: spin 0.7s linear infinite;
  flex-shrink: 0;
}

/* ── Nav buttons ── */
.td-nav-btns {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3);
}

.td-nav-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2-5);
  padding: var(--space-3) var(--space-4);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  cursor: pointer;
  font-family: var(--font-body);
  text-align: left;
  transition:
    border-color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out);
  color: var(--color-comet);
  min-width: 0;
}
.td-nav-btn:hover:not(:disabled) {
  border-color: var(--color-border-hover);
  background: var(--color-bg-elevated);
  color: var(--color-star);
}
.td-nav-btn:disabled { opacity: 0.35; cursor: not-allowed; }
.td-nav-btn:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

.td-nav-btn--next {
  justify-content: flex-end;
  text-align: right;
}

.td-nav-btn-text {
  display: flex;
  flex-direction: column;
  gap: 2px;
  min-width: 0;
  flex: 1;
}
.td-nav-btn--next .td-nav-btn-text { align-items: flex-end; }

.td-nav-btn-label {
  font-size: var(--text-2xs);
  font-weight: var(--weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--color-dust);
}
.td-nav-btn-name {
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 160px;
}

/* ── XP Toast ── */
.td-xp-toast {
  position: fixed;
  bottom: var(--space-8);
  right: var(--space-6);
  z-index: 300;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: var(--space-1);
  pointer-events: none;
}

.td-xp-toast-gain {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: var(--weight-bold);
  color: var(--color-orbit);
  text-shadow: 0 0 20px var(--color-orbit-glow);
  line-height: 1;
}
.td-xp-toast-level {
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-gold);
  background: rgba(255, 215, 0, 0.12);
  border: 1px solid rgba(255, 215, 0, 0.3);
  border-radius: var(--radius-full);
  padding: 2px var(--space-3);
}

.xp-pop-enter-active { transition: opacity 0.3s ease, transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1); }
.xp-pop-leave-active { transition: opacity 0.5s ease, transform 0.5s ease; }
.xp-pop-enter-from  { opacity: 0; transform: translateY(16px) scale(0.8); }
.xp-pop-leave-to    { opacity: 0; transform: translateY(-20px) scale(1.1); }

/* ── Sidebar ── */
.td-sidebar {
  position: sticky;
  top: calc(var(--topbar-height, 60px) + var(--space-4));
  max-height: calc(100vh - var(--topbar-height, 60px) - var(--space-8));
  display: flex;
  flex-direction: column;
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
}

.td-sidebar-toggle {
  display: none;
  align-items: center;
  gap: var(--space-2);
  width: 100%;
  padding: var(--space-3) var(--space-4);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-comet);
  cursor: pointer;
  text-align: left;
}
.td-sidebar-toggle-count {
  margin-left: auto;
  font-size: var(--text-xs);
  font-weight: var(--weight-bold);
  color: var(--color-orbit);
}
.td-sidebar-toggle:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

@media (max-width: 768px) {
  .td-sidebar {
    position: static;
    max-height: none;
    overflow: visible;
    background: none;
    border: none;
    border-radius: 0;
    padding: 0;
  }
  .td-sidebar-toggle { display: flex; }
  .td-sidebar-content {
    display: none;
    background: var(--color-bg-surface);
    border: 1px solid var(--color-border);
    border-radius: var(--radius-xl);
    overflow: hidden;
    margin-top: var(--space-2);
  }
  .td-sidebar--open .td-sidebar-content { display: block; }
}

.td-sidebar-content {
  flex: 1;
  overflow-y: auto;
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

/* ── XP Widget ── */
.td-xp-widget {
  padding: var(--space-3) var(--space-4);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
}
.td-xp-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: var(--space-2);
}
.td-xp-level {
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: var(--weight-bold);
  color: var(--color-orbit);
}
.td-xp-total {
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  color: var(--color-comet);
}
.td-xp-bar {
  height: 6px;
  background: var(--color-bg-base);
  border-radius: var(--radius-full);
  overflow: hidden;
  margin-bottom: var(--space-1-5);
}
.td-xp-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-orbit), var(--color-pulsar));
  border-radius: var(--radius-full);
  transition: width var(--duration-slow) var(--ease-out);
}
.td-xp-hint {
  font-size: var(--text-2xs);
  color: var(--color-dust);
  margin: 0;
}

/* ── Modules ── */
.td-modules {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.td-module {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}

.td-module-header {
  width: 100%;
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2-5) var(--space-3);
  background: var(--color-bg-elevated);
  border: none;
  cursor: pointer;
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-comet);
  text-align: left;
  transition: color var(--duration-fast) var(--ease-out);
}
.td-module-header:hover { color: var(--color-star); }
.td-module-header--done { color: var(--color-stellar); }
.td-module-header:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

.td-module-check {
  width: 16px;
  height: 16px;
  border-radius: var(--radius-full);
  border: 1.5px solid var(--color-border-hover);
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: transparent;
}
.td-module-check--done {
  background: var(--color-stellar);
  border-color: var(--color-stellar);
  color: #fff;
}

.td-module-name { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.td-module-count {
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  color: var(--color-dust);
  flex-shrink: 0;
}

.td-module-caret {
  color: var(--color-dust);
  flex-shrink: 0;
  transition: transform var(--duration-fast) var(--ease-out);
}
.td-module-caret--open { transform: rotate(180deg); }

/* ── Aula buttons ── */
.td-module-aulas {
  display: flex;
  flex-direction: column;
  padding: var(--space-1);
}

.td-aula-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) var(--space-2-5);
  border-radius: var(--radius-md);
  background: none;
  border: none;
  cursor: pointer;
  font-family: var(--font-body);
  font-size: var(--text-xs);
  color: var(--color-comet);
  text-align: left;
  width: 100%;
  transition:
    background-color var(--duration-fast) var(--ease-out),
    color var(--duration-fast) var(--ease-out);
}
.td-aula-btn:hover { background: var(--color-surface-hover); color: var(--color-star); }
.td-aula-btn:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

.td-aula-btn--active {
  background: var(--color-orbit-dim);
  color: var(--color-orbit);
  font-weight: var(--weight-semibold);
}
.td-aula-btn--done { color: var(--color-dust); }
.td-aula-btn--done.td-aula-btn--active { background: var(--color-stellar-dim); color: var(--color-stellar); }

.td-aula-btn-check {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-stellar);
}

.td-aula-btn-dot {
  display: block;
  width: 6px;
  height: 6px;
  border-radius: var(--radius-full);
  background: var(--color-orbit);
}

.td-aula-btn-name {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.td-aula-btn-dur {
  font-size: 10px;
  color: var(--color-dust);
  flex-shrink: 0;
  white-space: nowrap;
}
</style>

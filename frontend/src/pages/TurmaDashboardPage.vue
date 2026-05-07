<template>
  <DashboardLayout :username="username" :is-admin="isAdmin">

    <!-- Header -->
    <header class="turma-header">
      <div class="turma-header-left">
        <h1 class="turma-title">Dashboard de Batalha</h1>
        <p class="turma-sub">Inteligência coletiva da sua turma em tempo real.</p>
      </div>

      <select
        v-model="turmaSelecionadaId"
        class="turma-select"
        @change="carregarDashboard"
      >
        <option value="" disabled>Selecione a turma</option>
        <option v-for="t in turmas" :key="t.id" :value="t.id">{{ t.nome }}</option>
      </select>
    </header>

    <!-- Loading skeleton -->
    <div v-if="carregando" class="turma-skeletons">
      <div class="sk-grid sk-grid--3">
        <div v-for="i in 3" :key="i" class="sk-block sk-block--sm" />
      </div>
      <div class="sk-grid sk-grid--2">
        <div class="sk-block sk-block--lg" />
        <div class="sk-block sk-block--lg" />
      </div>
    </div>

    <!-- Sem turma selecionada -->
    <div v-else-if="!dados" class="turma-empty">
      <div class="turma-empty-icon">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
          <circle cx="9" cy="7" r="4"/>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
          <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>
      </div>
      <p class="turma-empty-title">Selecione uma turma</p>
      <p class="turma-empty-sub">Escolha a turma acima para ver o desempenho coletivo.</p>
    </div>

    <!-- Dashboard completo -->
    <template v-else>

      <!-- Microcopy motivacional -->
      <div class="turma-microcopy">
        <p class="turma-microcopy-text">{{ microcopy }}</p>
      </div>

      <!-- KPI Cards -->
      <section class="kpi-grid">
        <div class="kpi-card">
          <span class="kpi-label">Média da Turma</span>
          <span class="kpi-value" :class="scoreColorClass(dados.media_score)">
            {{ dados.media_score.toFixed(1) }}<span class="kpi-unit">%</span>
          </span>
        </div>
        <div class="kpi-card">
          <span class="kpi-label">Simulados/Semana</span>
          <span class="kpi-value kpi-value--orbit">{{ dados.simulados_semana }}</span>
        </div>
        <div class="kpi-card kpi-card--span2">
          <span class="kpi-label">Questões/Semana</span>
          <span class="kpi-value kpi-value--stellar">{{ dados.questoes_semana }}</span>
        </div>
      </section>

      <!-- Gráficos -->
      <section class="chart-grid">
        <div class="chart-card">
          <h2 class="chart-title">Radar de Desempenho por Disciplina</h2>
          <div class="chart-wrap">
            <Radar v-if="radarData.labels.length" :data="radarData" :options="radarOptions" />
            <div v-else class="chart-empty">Sem dados suficientes ainda.</div>
          </div>
        </div>

        <div class="chart-card">
          <h2 class="chart-title">Produtividade Semanal (simulados realizados)</h2>
          <div class="chart-wrap">
            <Bar v-if="barData.labels.length" :data="barData" :options="barOptions" />
            <div v-else class="chart-empty">Sem atividade registrada ainda.</div>
          </div>
        </div>
      </section>

      <!-- Pódio: Top 3 Alunos -->
      <section class="podio-section">
        <h2 class="podio-heading">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" class="podio-trophy" aria-hidden="true">
            <circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>
          </svg>
          Top Performers — {{ dados.turma.nome }}
        </h2>

        <div v-if="!dados.top_alunos.length" class="podio-empty">
          Nenhum resultado registrado ainda.
        </div>

        <!-- Pódio visual -->
        <div v-else class="podio-visual">
          <!-- 2º lugar -->
          <div v-if="dados.top_alunos[1]" class="podio-slot">
            <div class="podio-avatar podio-avatar--silver">{{ initials(dados.top_alunos[1]) }}</div>
            <div class="podio-bar podio-bar--silver">
              <span class="podio-pos">2º</span>
              <span class="podio-score">{{ formatScore(dados.top_alunos[1].media) }}%</span>
            </div>
          </div>

          <!-- 1º lugar -->
          <div v-if="dados.top_alunos[0]" class="podio-slot podio-slot--first">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="var(--color-gold)" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
              <path d="M2 16l3-10 4.5 5.5L12 3l2.5 8.5L19 6l3 10H2z"/><rect x="2" y="16" width="20" height="2" rx="1"/>
            </svg>
            <div class="podio-avatar podio-avatar--gold">{{ initials(dados.top_alunos[0]) }}</div>
            <div class="podio-bar podio-bar--gold">
              <span class="podio-pos">1º</span>
              <span class="podio-score podio-score--gold">{{ formatScore(dados.top_alunos[0].media) }}%</span>
            </div>
          </div>

          <!-- 3º lugar -->
          <div v-if="dados.top_alunos[2]" class="podio-slot">
            <div class="podio-avatar podio-avatar--bronze">{{ initials(dados.top_alunos[2]) }}</div>
            <div class="podio-bar podio-bar--bronze">
              <span class="podio-pos">3º</span>
              <span class="podio-score">{{ formatScore(dados.top_alunos[2].media) }}%</span>
            </div>
          </div>
        </div>

        <!-- Lista expandida -->
        <div v-if="dados.top_alunos.length" class="rank-list">
          <div
            v-for="(aluno, idx) in dados.top_alunos"
            :key="aluno['aluno__id']"
            class="rank-row"
            :class="{ 'rank-row--first': idx === 0 }"
          >
            <span class="rank-pos" :class="['rank-pos--orbit', 'rank-pos--dust', 'rank-pos--flare'][idx] || 'rank-pos--dust'">
              {{ idx + 1 }}
            </span>
            <div class="rank-avatar">{{ initials(aluno) }}</div>
            <span class="rank-name">{{ displayName(aluno) }}</span>
            <span class="rank-score" :class="scoreColorClass(aluno.media)">{{ formatScore(aluno.media) }}%</span>
            <span class="rank-count">{{ aluno.total_simulados }} sim.</span>
          </div>
        </div>
      </section>

    </template>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import {
  Chart as ChartJS,
  RadialLinearScale, PointElement, LineElement, Filler,
  CategoryScale, LinearScale, BarElement,
  Tooltip, Legend,
} from 'chart.js'
import { Radar, Bar } from 'vue-chartjs'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import { escolasService } from '../services/aulasService.js'

ChartJS.register(
  RadialLinearScale, PointElement, LineElement, Filler,
  CategoryScale, LinearScale, BarElement,
  Tooltip, Legend,
)

const username = localStorage.getItem('username') || ''
const isAdmin = localStorage.getItem('user_role') === 'admin'

const turmas = ref([])
const turmaSelecionadaId = ref('')
const dados = ref(null)
const carregando = ref(false)

onMounted(async () => {
  try {
    const { data } = await escolasService.listarTurmas()
    turmas.value = data
    if (data.length === 1) {
      turmaSelecionadaId.value = data[0].id
      await carregarDashboard()
    }
  } catch (e) {
    console.error(e)
  }
})

async function carregarDashboard() {
  if (!turmaSelecionadaId.value) return
  carregando.value = true
  dados.value = null
  try {
    const { data } = await escolasService.dashboardTurma(turmaSelecionadaId.value)
    dados.value = data
  } catch (e) {
    console.error(e)
  } finally {
    carregando.value = false
  }
}

// DS token hex values for Chart.js (can't use CSS vars in Chart.js)
const DS = {
  orbit:     '#00E5FF',
  orbitDim:  'rgba(0, 229, 255, 0.08)',
  orbitLine: 'rgba(0, 229, 255, 0.7)',
  orbitBar:  'rgba(0, 229, 255, 0.6)',
  grid:      'rgba(255, 255, 255, 0.06)',
  tick:      'rgba(255, 255, 255, 0.35)',
  label:     'rgba(255, 255, 255, 0.55)',
}

const radarData = computed(() => {
  const items = dados.value?.radar_data || []
  return {
    labels: items.map((i) => i.materia),
    datasets: [{
      label: 'Acertos (%)',
      data: items.map((i) => i.percentual),
      backgroundColor: DS.orbitDim,
      borderColor: DS.orbitLine,
      borderWidth: 2,
      pointBackgroundColor: DS.orbit,
      pointRadius: 4,
    }],
  }
})

const radarOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    r: {
      min: 0, max: 100,
      ticks: { stepSize: 25, font: { size: 10 }, color: DS.tick },
      grid: { color: DS.grid },
      pointLabels: { font: { size: 11, family: 'DM Sans' }, color: DS.label },
    },
  },
  plugins: { legend: { display: false } },
}

const barData = computed(() => {
  const items = dados.value?.weekly_data || []
  return {
    labels: items.map((i) => i.semana),
    datasets: [{
      label: 'Simulados',
      data: items.map((i) => i.simulados),
      backgroundColor: DS.orbitBar,
      borderRadius: 8,
      borderSkipped: false,
    }],
  }
})

const barOptions = {
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: {
      beginAtZero: true,
      ticks: { stepSize: 1, font: { size: 10 }, color: DS.tick },
      grid: { color: DS.grid },
    },
    x: {
      ticks: { font: { size: 10 }, color: DS.tick },
      grid: { display: false },
    },
  },
  plugins: { legend: { display: false } },
}

const microcopy = computed(() => {
  if (!dados.value) return ''
  const { questoes_semana, simulados_semana, media_score, turma } = dados.value
  if (questoes_semana > 200)
    return `🔥 ${turma.nome} está on fire! ${questoes_semana} questões resolvidas essa semana. Incrível!`
  if (simulados_semana > 5)
    return `⚡ Que semana produtiva! ${turma.nome} completou ${simulados_semana} simulados. Continue assim!`
  if (media_score >= 70)
    return `💪 ${turma.nome} está acima da média com ${media_score.toFixed(0)}% — a aprovação está chegando!`
  if (media_score >= 50)
    return `📈 ${turma.nome} está evoluindo! Com foco nos pontos fracos vocês chegam lá.`
  return `🎯 Todo expert já foi iniciante. ${turma.nome}, a jornada começa agora!`
})

function scoreColorClass(score) {
  if (score >= 70) return 'score--stellar'
  if (score >= 50) return 'score--flare'
  return 'score--nova'
}
function formatScore(v) { return Number(v).toFixed(1) }
function initials(aluno) {
  const name = aluno['aluno__first_name'] || aluno['aluno__username'] || '?'
  return name.slice(0, 2).toUpperCase()
}
function displayName(aluno) {
  return aluno['aluno__first_name'] || aluno['aluno__username']
}
</script>

<style scoped>
/* ── Header ── */
.turma-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}
@media (min-width: 640px) {
  .turma-header { flex-direction: row; align-items: center; justify-content: space-between; }
}
.turma-title {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  margin-bottom: var(--space-1);
}
.turma-sub { font-size: var(--text-sm); color: var(--color-comet); }

.turma-select {
  width: 100%;
  max-width: 224px;
  height: var(--btn-height-md);
  padding: 0 var(--space-3);
  border-radius: var(--input-radius);
  border: 1px solid var(--color-border);
  background: var(--color-bg-surface);
  color: var(--color-star);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  outline: none;
  cursor: pointer;
  transition: border-color var(--duration-fast) var(--ease-out), box-shadow var(--duration-fast) var(--ease-out);
  -webkit-appearance: none;
}
.turma-select:focus { border-color: var(--color-orbit); box-shadow: var(--shadow-focus); }

/* ── Skeleton ── */
.turma-skeletons { display: flex; flex-direction: column; gap: var(--space-4); margin-bottom: var(--space-6); }
.sk-grid { display: grid; gap: var(--space-3); }
.sk-grid--3 { grid-template-columns: repeat(3, 1fr); }
.sk-grid--2 { grid-template-columns: repeat(2, 1fr); }
.sk-block { background: var(--color-bg-elevated); border-radius: var(--radius-xl); animation: pulse 1.5s ease-in-out infinite; }
.sk-block--sm { height: 96px; }
.sk-block--lg { height: 288px; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

@media (max-width: 640px) {
  .sk-grid--3 { grid-template-columns: repeat(2, 1fr); }
  .sk-grid--2 { grid-template-columns: 1fr; }
}

/* ── Empty state ── */
.turma-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--space-12, 48px) var(--space-4);
  text-align: center;
}
.turma-empty-icon {
  width: 56px;
  height: 56px;
  border-radius: var(--radius-xl);
  background: var(--color-orbit-dim);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-orbit);
  margin-bottom: var(--space-4);
}
.turma-empty-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--weight-semibold);
  color: var(--color-star);
}
.turma-empty-sub { font-size: var(--text-sm); color: var(--color-comet); margin-top: var(--space-1); }

/* ── Microcopy ── */
.turma-microcopy {
  margin-bottom: var(--space-4);
  padding: var(--space-4);
  border-radius: var(--radius-xl);
  background: linear-gradient(135deg, var(--color-orbit-dim), var(--color-pulsar-dim));
  border: 1px solid var(--color-orbit-border);
}
.turma-microcopy-text {
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-star);
}

/* ── KPI Cards ── */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-3);
  margin-bottom: var(--space-4);
}
@media (max-width: 640px) {
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
}
.kpi-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--radius-xl);
  padding: var(--space-4);
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  box-shadow: var(--card-shadow);
}
.kpi-card--span2 { grid-column: span 2 / span 2; }
@media (min-width: 768px) { .kpi-card--span2 { grid-column: span 1 / span 1; } }

.kpi-label {
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-dust);
}
.kpi-value {
  font-family: var(--font-display);
  font-weight: var(--weight-extrabold);
  font-size: var(--text-4xl);
  line-height: 1;
}
.kpi-unit { font-size: var(--text-base); font-weight: var(--weight-normal); color: var(--color-dust); }
.kpi-value--orbit   { color: var(--color-orbit); }
.kpi-value--stellar { color: var(--color-stellar); }
.score--stellar { color: var(--color-stellar); }
.score--flare   { color: var(--color-flare); }
.score--nova    { color: var(--color-nova); }

/* ── Charts ── */
.chart-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--space-4);
  margin-bottom: var(--space-4);
}
@media (max-width: 768px) { .chart-grid { grid-template-columns: 1fr; } }

.chart-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  box-shadow: var(--card-shadow);
}
.chart-title {
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-star);
  margin-bottom: var(--space-4);
}
.chart-wrap { position: relative; height: 224px; }
.chart-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  font-size: var(--text-sm);
  color: var(--color-dust);
}

/* ── Pódio ── */
.podio-section {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  box-shadow: var(--card-shadow);
  margin-bottom: var(--space-6);
}
.podio-heading {
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-star);
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-5);
}
.podio-trophy { color: var(--color-gold); flex-shrink: 0; }
.podio-empty { text-align: center; padding: var(--space-6) 0; font-size: var(--text-sm); color: var(--color-dust); }

.podio-visual {
  display: flex;
  align-items: flex-end;
  justify-content: center;
  gap: var(--space-3);
  margin-bottom: var(--space-5);
}
.podio-slot {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  width: 96px;
}
.podio-slot--first { order: -1; }
@media (min-width: 400px) { .podio-slot--first { order: 0; } }

.podio-avatar {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-display);
  font-weight: var(--weight-bold);
  font-size: var(--text-lg);
}
.podio-avatar--gold   { background: var(--color-orbit-dim); color: var(--color-orbit); border: 2px solid var(--color-orbit-border); width: 56px; height: 56px; }
.podio-avatar--silver { background: var(--color-bg-elevated); color: var(--color-comet); border: 1px solid var(--color-border); }
.podio-avatar--bronze { background: rgba(205, 127, 50, 0.1); color: var(--color-bronze); border: 1px solid rgba(205, 127, 50, 0.25); }

.podio-bar {
  width: 100%;
  border-radius: var(--radius-md) var(--radius-md) 0 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2px;
  padding: var(--space-2);
}
.podio-bar--gold   { height: 112px; background: linear-gradient(180deg, var(--color-orbit-dim), rgba(0,229,255,0.04)); border: 1px solid var(--color-orbit-border); }
.podio-bar--silver { height: 80px; background: var(--color-bg-elevated); border: 1px solid var(--color-border); }
.podio-bar--bronze { height: 56px; background: rgba(255, 119, 0, 0.06); border: 1px solid rgba(255, 119, 0, 0.15); }

.podio-pos { font-size: var(--text-2xs); font-weight: var(--weight-bold); color: var(--color-dust); }
.podio-score { font-family: var(--font-display); font-size: var(--text-sm); font-weight: var(--weight-bold); color: var(--color-star); }
.podio-score--gold { color: var(--color-orbit); }

/* ── Rank list ── */
.rank-list { display: flex; flex-direction: column; gap: var(--space-2); }
.rank-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-lg);
  background: var(--color-bg-elevated);
}
.rank-row--first { background: var(--color-orbit-dim); }

.rank-pos {
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: var(--weight-bold);
  width: 20px;
  text-align: center;
}
.rank-pos--orbit { color: var(--color-orbit); }
.rank-pos--dust  { color: var(--color-dust); }
.rank-pos--flare { color: var(--color-flare); }

.rank-avatar {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: var(--weight-bold);
  font-size: var(--text-xs);
  color: var(--color-star);
}
.rank-name { flex: 1; font-family: var(--font-body); font-size: var(--text-sm); font-weight: var(--weight-medium); color: var(--color-star); }
.rank-score { font-family: var(--font-display); font-size: var(--text-sm); font-weight: var(--weight-bold); }
.rank-count { font-size: var(--text-2xs); color: var(--color-dust); }
</style>

<template>
  <DashboardLayout :username="username" :is-admin="isAdmin">

    <!-- Header -->
    <section class="px-4 pt-6 pb-4 md:px-8 md:pt-8">
      <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
        <div>
          <h1 class="font-display font-bold text-2xl md:text-3xl text-simus-text">
            Dashboard de Batalha
          </h1>
          <p class="text-simus-muted text-sm mt-1 font-body">Inteligência coletiva da sua turma em tempo real.</p>
        </div>

        <!-- Seletor de turma -->
        <select
          v-model="turmaSelecionadaId"
          class="w-full sm:w-56 h-11 px-3 rounded-simus-sm border border-slate-200 bg-white text-simus-text font-body text-sm focus:outline-none focus:ring-2 focus:ring-simus-primary/50 transition-all"
          @change="carregarDashboard"
        >
          <option value="" disabled>Selecione a turma</option>
          <option v-for="t in turmas" :key="t.id" :value="t.id">{{ t.nome }}</option>
        </select>
      </div>
    </section>

    <!-- Loading skeleton -->
    <div v-if="carregando" class="px-4 md:px-8 pb-24 space-y-4">
      <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
        <div v-for="i in 3" :key="i" class="h-24 rounded-2xl bg-slate-100 animate-pulse" />
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div class="h-72 rounded-2xl bg-slate-100 animate-pulse" />
        <div class="h-72 rounded-2xl bg-slate-100 animate-pulse" />
      </div>
    </div>

    <!-- Sem turma selecionada -->
    <div v-else-if="!dados" class="flex flex-col items-center justify-center py-20 px-4 text-center">
      <div class="w-14 h-14 rounded-2xl bg-indigo-50 flex items-center justify-center mb-4 text-indigo-400">
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/>
          <path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>
        </svg>
      </div>
      <p class="font-display font-semibold text-simus-text text-lg">Selecione uma turma</p>
      <p class="text-simus-muted text-sm mt-1">Escolha a turma acima para ver o desempenho coletivo.</p>
    </div>

    <!-- Dashboard completo -->
    <template v-else>

      <!-- Microcopy motivacional -->
      <div class="mx-4 md:mx-8 mb-4 p-4 rounded-2xl bg-gradient-to-r from-indigo-50 to-purple-50 border border-indigo-100">
        <p class="font-display font-semibold text-simus-text text-sm">
          {{ microcopy }}
        </p>
      </div>

      <!-- KPI Cards -->
      <section class="px-4 md:px-8 pb-4">
        <div class="grid grid-cols-2 md:grid-cols-3 gap-3">
          <div class="bg-white rounded-2xl border border-slate-100 shadow-simus-soft p-4 flex flex-col gap-1">
            <span class="text-[11px] font-bold uppercase tracking-wider text-simus-muted">Média da Turma</span>
            <span class="font-display font-bold text-3xl" :class="scoreColor(dados.media_score)">
              {{ dados.media_score.toFixed(1) }}<span class="text-base font-normal text-simus-muted">%</span>
            </span>
          </div>
          <div class="bg-white rounded-2xl border border-slate-100 shadow-simus-soft p-4 flex flex-col gap-1">
            <span class="text-[11px] font-bold uppercase tracking-wider text-simus-muted">Simulados/Semana</span>
            <span class="font-display font-bold text-3xl text-simus-primary">
              {{ dados.simulados_semana }}
            </span>
          </div>
          <div class="col-span-2 md:col-span-1 bg-white rounded-2xl border border-slate-100 shadow-simus-soft p-4 flex flex-col gap-1">
            <span class="text-[11px] font-bold uppercase tracking-wider text-simus-muted">Questões/Semana</span>
            <span class="font-display font-bold text-3xl text-emerald-600">
              {{ dados.questoes_semana }}
            </span>
          </div>
        </div>
      </section>

      <!-- Gráficos -->
      <section class="px-4 md:px-8 pb-4">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

          <!-- Radar: Forças e Fraquezas -->
          <div class="bg-white rounded-2xl border border-slate-100 shadow-simus-soft p-5">
            <h2 class="font-display font-semibold text-sm text-simus-text mb-4">
              Radar de Desempenho por Disciplina
            </h2>
            <div class="relative h-56">
              <Radar v-if="radarData.labels.length" :data="radarData" :options="radarOptions" />
              <div v-else class="flex items-center justify-center h-full text-simus-muted text-sm">
                Sem dados suficientes ainda.
              </div>
            </div>
          </div>

          <!-- Barras: Produtividade semanal -->
          <div class="bg-white rounded-2xl border border-slate-100 shadow-simus-soft p-5">
            <h2 class="font-display font-semibold text-sm text-simus-text mb-4">
              Produtividade Semanal (simulados realizados)
            </h2>
            <div class="relative h-56">
              <Bar v-if="barData.labels.length" :data="barData" :options="barOptions" />
              <div v-else class="flex items-center justify-center h-full text-simus-muted text-sm">
                Sem atividade registrada ainda.
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Pódio: Top 3 Alunos -->
      <section class="px-4 md:px-8 pb-24">
        <div class="bg-white rounded-2xl border border-slate-100 shadow-simus-soft p-5">
          <h2 class="font-display font-semibold text-sm text-simus-text mb-5 flex items-center gap-2">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" class="text-amber-500">
              <circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>
            </svg>
            Top Performers — {{ dados.turma.nome }}
          </h2>

          <div v-if="!dados.top_alunos.length" class="text-center py-6 text-simus-muted text-sm">
            Nenhum resultado registrado ainda.
          </div>

          <!-- Pódio visual -->
          <div v-else class="flex items-end justify-center gap-3 mb-5">
            <!-- 2º lugar -->
            <div v-if="dados.top_alunos[1]" class="flex flex-col items-center gap-2 w-24">
              <div class="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center font-display font-bold text-lg text-simus-muted">
                {{ initials(dados.top_alunos[1]) }}
              </div>
              <div class="w-full h-20 rounded-t-xl bg-slate-100 flex flex-col items-center justify-center">
                <span class="text-[10px] text-simus-muted font-bold">2º</span>
                <span class="text-sm font-display font-bold text-simus-text">{{ formatScore(dados.top_alunos[1].media) }}%</span>
              </div>
            </div>

            <!-- 1º lugar -->
            <div v-if="dados.top_alunos[0]" class="flex flex-col items-center gap-2 w-24">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" class="text-amber-400">
                <path d="M2 16l3-10 4.5 5.5L12 3l2.5 8.5L19 6l3 10H2z"/><rect x="2" y="16" width="20" height="2" rx="1"/>
              </svg>
              <div class="w-14 h-14 rounded-full bg-indigo-100 flex items-center justify-center font-display font-bold text-xl text-simus-primary ring-2 ring-simus-primary/30">
                {{ initials(dados.top_alunos[0]) }}
              </div>
              <div class="w-full h-28 rounded-t-xl bg-gradient-to-b from-simus-primary to-indigo-600 flex flex-col items-center justify-center">
                <span class="text-[10px] text-indigo-200 font-bold">1º</span>
                <span class="text-base font-display font-bold text-white">{{ formatScore(dados.top_alunos[0].media) }}%</span>
              </div>
            </div>

            <!-- 3º lugar -->
            <div v-if="dados.top_alunos[2]" class="flex flex-col items-center gap-2 w-24">
              <div class="w-12 h-12 rounded-full bg-amber-50 flex items-center justify-center font-display font-bold text-lg text-amber-600">
                {{ initials(dados.top_alunos[2]) }}
              </div>
              <div class="w-full h-14 rounded-t-xl bg-amber-50 flex flex-col items-center justify-center">
                <span class="text-[10px] text-amber-600 font-bold">3º</span>
                <span class="text-sm font-display font-bold text-simus-text">{{ formatScore(dados.top_alunos[2].media) }}%</span>
              </div>
            </div>
          </div>

          <!-- Lista expandida -->
          <div class="space-y-2">
            <div
              v-for="(aluno, idx) in dados.top_alunos"
              :key="aluno['aluno__id']"
              class="flex items-center gap-3 px-3 py-2 rounded-xl"
              :class="idx === 0 ? 'bg-indigo-50' : 'bg-slate-50'"
            >
              <span class="font-display font-bold text-sm w-5 text-center"
                :class="['text-simus-primary', 'text-simus-muted', 'text-amber-600'][idx]">
                {{ idx + 1 }}
              </span>
              <div class="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center font-bold text-xs text-simus-text">
                {{ initials(aluno) }}
              </div>
              <span class="flex-1 font-body text-sm text-simus-text font-medium">
                {{ displayName(aluno) }}
              </span>
              <span class="font-display font-bold text-sm" :class="scoreColor(aluno.media)">
                {{ formatScore(aluno.media) }}%
              </span>
              <span class="text-[11px] text-simus-muted">{{ aluno.total_simulados }} sim.</span>
            </div>
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

// Gráfico Radar
const radarData = computed(() => {
  const items = dados.value?.radar_data || []
  return {
    labels: items.map((i) => i.materia),
    datasets: [{
      label: 'Acertos (%)',
      data: items.map((i) => i.percentual),
      backgroundColor: 'rgba(79, 70, 229, 0.15)',
      borderColor: 'rgba(79, 70, 229, 0.8)',
      borderWidth: 2,
      pointBackgroundColor: '#4F46E5',
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
      ticks: { stepSize: 25, font: { size: 10 }, color: '#94a3b8' },
      grid: { color: '#f1f5f9' },
      pointLabels: { font: { size: 11, family: 'Inter' }, color: '#475569' },
    },
  },
  plugins: { legend: { display: false } },
}

// Gráfico de Barras
const barData = computed(() => {
  const items = dados.value?.weekly_data || []
  return {
    labels: items.map((i) => i.semana),
    datasets: [{
      label: 'Simulados',
      data: items.map((i) => i.simulados),
      backgroundColor: 'rgba(79, 70, 229, 0.7)',
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
      ticks: { stepSize: 1, font: { size: 10 }, color: '#94a3b8' },
      grid: { color: '#f8fafc' },
    },
    x: {
      ticks: { font: { size: 10 }, color: '#94a3b8' },
      grid: { display: false },
    },
  },
  plugins: { legend: { display: false } },
}

// Microcopy motivacional dinâmico
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

// Helpers
function scoreColor(score) {
  if (score >= 70) return 'text-emerald-600'
  if (score >= 50) return 'text-amber-500'
  return 'text-red-500'
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

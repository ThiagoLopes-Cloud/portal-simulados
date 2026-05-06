<template>
  <DashboardLayout :username="username" :is-admin="true">
    <header class="page-header">
      <div>
        <h2 class="page-title">Gestão de Alunos</h2>
        <p class="page-sub">Visão geral e acesso aos relatórios individuais de performance.</p>
      </div>
      <SimuslabBadge variant="pulsar">Admin</SimuslabBadge>
    </header>

    <!-- Skeleton -->
    <div v-if="carregando" class="skeleton-list">
      <div v-for="n in 7" :key="n" class="skeleton-row" />
    </div>

    <!-- Erro -->
    <div v-else-if="erro" class="empty-state">
      <div class="empty-icon nova">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
      </div>
      <h3 class="empty-title">Falha de Conexão</h3>
      <p class="empty-sub">{{ erro }}</p>
      <SimuslabButton variant="primary" size="sm" class="mt-5" @click="carregarAlunos">Tentar Novamente</SimuslabButton>
    </div>

    <div v-else>
      <!-- Vazio -->
      <div v-if="alunos.length === 0" class="empty-state">
        <div class="empty-icon">
          <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
        <h3 class="empty-title">Nenhum Registro</h3>
        <p class="empty-sub">O banco de dados de alunos está vazio no momento.</p>
      </div>

      <!-- Tabela -->
      <div v-else class="table-card">
        <div class="table-header">
          <h3 class="table-title">Base de Candidatos</h3>
          <span class="count-badge">{{ alunos.length }} alunos</span>
        </div>

        <!-- Desktop -->
        <table class="data-table">
          <thead>
            <tr class="thead-row">
              <th class="th">Candidato</th>
              <th class="th text-center">Avaliações</th>
              <th class="th text-center">Desempenho</th>
              <th class="th text-right">Relatório</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="aluno in alunos" :key="aluno.id" class="tbody-row">
              <td class="td">
                <div class="user-cell">
                  <div class="user-avatar">{{ aluno.username.charAt(0).toUpperCase() }}</div>
                  <div>
                    <p class="user-name">{{ aluno.username }}</p>
                    <p class="user-email">{{ aluno.email }}</p>
                  </div>
                </div>
              </td>
              <td class="td text-center">
                <span class="sim-count" :class="{ 'sim-count--zero': aluno.total_simulados === 0 }">
                  {{ aluno.total_simulados }}
                </span>
              </td>
              <td class="td text-center">
                <span v-if="aluno.total_simulados > 0" class="score-badge" :class="scoreBg(aluno.score_medio)">
                  {{ aluno.score_medio }}%
                </span>
                <span v-else class="no-data">Sem dados</span>
              </td>
              <td class="td text-right">
                <SimuslabButton
                  variant="ghost"
                  size="sm"
                  :disabled="aluno.total_simulados === 0"
                  @click="verDashboard(aluno.id)"
                >
                  Ver Relatório
                </SimuslabButton>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- Mobile cards -->
        <div class="mobile-cards">
          <div v-for="aluno in alunos" :key="aluno.id" class="mobile-aluno">
            <div class="user-cell">
              <div class="user-avatar">{{ aluno.username.charAt(0).toUpperCase() }}</div>
              <div>
                <p class="user-name">{{ aluno.username }}</p>
                <p class="user-email">{{ aluno.email }}</p>
              </div>
            </div>
            <div class="mobile-row-stats">
              <span class="stat-label">{{ aluno.total_simulados }} avaliações</span>
              <span v-if="aluno.total_simulados > 0" class="score-badge" :class="scoreBg(aluno.score_medio)">{{ aluno.score_medio }}%</span>
              <SimuslabButton variant="ghost" size="sm" :disabled="aluno.total_simulados === 0" @click="verDashboard(aluno.id)">
                Relatório
              </SimuslabButton>
            </div>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import SimuslabButton from '../components/ui/SimuslabButton.vue'
import SimuslabBadge from '../components/ui/SimuslabBadge.vue'

const router = useRouter()
const username = localStorage.getItem('username') || ''
const alunos = ref([])
const carregando = ref(true)
const erro = ref('')

async function carregarAlunos() {
  carregando.value = true
  erro.value = ''
  try {
    const response = await api.get('/api/resultados/admin/alunos/')
    alunos.value = response.data
  } catch {
    erro.value = 'Falha ao sincronizar o banco de dados de alunos.'
  } finally {
    carregando.value = false
  }
}

onMounted(carregarAlunos)

function verDashboard(id) {
  router.push({ name: 'admin-aluno-dashboard', params: { id } })
}

function scoreBg(v) {
  if (v >= 70) return 'score--stellar'
  if (v >= 50) return 'score--flare'
  return 'score--nova'
}
</script>

<style scoped>
.page-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: var(--space-8); }
.page-title { font-family: var(--font-display); font-size: var(--text-2xl); font-weight: var(--weight-bold); color: var(--color-star); }
.page-sub { font-size: var(--text-sm); color: var(--color-comet); margin-top: var(--space-1); }

/* Skeleton */
.skeleton-list { display: flex; flex-direction: column; gap: var(--space-2); }
.skeleton-row { height: 60px; background: var(--color-nebula); border-radius: var(--radius-md); position: relative; overflow: hidden; }
.skeleton-row::after { content: ''; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent); animation: shimmer 1.5s infinite; }
@keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

/* Empty */
.empty-state { display: flex; flex-direction: column; align-items: center; text-align: center; padding: var(--space-14) var(--space-8); background: var(--color-nebula); border: 1px dashed var(--color-border); border-radius: var(--radius-xl); }
.empty-icon { color: var(--color-orbit); margin-bottom: var(--space-5); }
.empty-icon.nova { color: var(--color-nova); }
.empty-title { font-family: var(--font-display); font-size: var(--text-lg); font-weight: var(--weight-bold); color: var(--color-star); margin-bottom: var(--space-2); }
.empty-sub { font-size: var(--text-sm); color: var(--color-comet); }
.mt-5 { margin-top: var(--space-5); }

/* Table card */
.table-card { background: var(--color-nebula); border: 1px solid var(--color-border); border-radius: var(--radius-xl); overflow: hidden; }
.table-header { display: flex; justify-content: space-between; align-items: center; padding: var(--space-5) var(--space-6); border-bottom: 1px solid var(--color-border); }
.table-title { font-family: var(--font-display); font-size: var(--text-base); font-weight: var(--weight-bold); color: var(--color-star); }
.count-badge { padding: 3px var(--space-3); border-radius: var(--radius-full); background: rgba(255,255,255,0.05); color: var(--color-dust); font-size: var(--text-xs); font-family: var(--font-mono); font-weight: var(--weight-bold); }

.data-table { width: 100%; border-collapse: collapse; }
.thead-row { border-bottom: 1px solid var(--color-border); }
.th { padding: var(--space-3) var(--space-5); text-align: left; font-size: var(--text-2xs); font-family: var(--font-mono); font-weight: var(--weight-bold); color: var(--color-dust); text-transform: uppercase; letter-spacing: 0.08em; }
.text-center { text-align: center; }
.text-right { text-align: right; }
.td { padding: var(--space-4) var(--space-5); border-bottom: 1px solid rgba(255,255,255,0.03); vertical-align: middle; }
.tbody-row { transition: background var(--transition-fast); }
.tbody-row:hover { background: rgba(255,255,255,0.02); }

.user-cell { display: flex; align-items: center; gap: var(--space-3); }
.user-avatar { width: 40px; height: 40px; border-radius: 50%; background: rgba(0,229,255,0.1); border: 1px solid rgba(0,229,255,0.2); display: flex; align-items: center; justify-content: center; color: var(--color-orbit); font-weight: var(--weight-bold); font-size: var(--text-base); flex-shrink: 0; }
.user-name { font-size: var(--text-sm); font-weight: var(--weight-semibold); color: var(--color-star); }
.user-email { font-size: var(--text-xs); color: var(--color-dust); margin-top: 2px; }

.sim-count { font-size: var(--text-sm); font-weight: var(--weight-bold); color: var(--color-star); }
.sim-count--zero { color: var(--color-dust); }
.no-data { font-size: var(--text-sm); color: var(--color-dust); font-style: italic; }

.score-badge { display: inline-block; padding: 3px var(--space-2); border-radius: var(--radius-full); font-size: var(--text-xs); font-family: var(--font-mono); font-weight: var(--weight-bold); color: white; }
.score--stellar { background: var(--color-stellar); }
.score--flare   { background: var(--color-flare); }
.score--nova    { background: var(--color-nova); }

/* Mobile */
.mobile-cards { display: none; }
@media (max-width: 640px) {
  .data-table { display: none; }
  .mobile-cards { display: flex; flex-direction: column; }
  .mobile-aluno { padding: var(--space-4) var(--space-5); border-bottom: 1px solid var(--color-border); display: flex; flex-direction: column; gap: var(--space-3); }
  .mobile-row-stats { display: flex; align-items: center; gap: var(--space-3); justify-content: space-between; }
  .stat-label { font-size: var(--text-xs); color: var(--color-dust); }
}
</style>

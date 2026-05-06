<template>
  <DashboardLayout :username="username" :is-admin="isAdmin">
    <header class="page-header">
      <div>
        <h2 class="page-title">Ranking Geral</h2>
        <p class="page-sub">Os melhores desempenhos do laboratório.</p>
      </div>
    </header>

    <div v-if="erro" class="alert alert--error">{{ erro }}</div>

    <div v-else-if="carregando" class="skeleton-list">
      <div v-for="n in 6" :key="n" class="skeleton-row" />
    </div>

    <div v-else>
      <div v-if="ranking.length === 0" class="empty-state">
        <div class="empty-icon">◆</div>
        <h3 class="empty-title">Ranking em formação.</h3>
        <p class="empty-sub">Seja o primeiro a completar uma avaliação e conquiste o topo do laboratório.</p>
      </div>

      <div v-else class="rank-card">
        <!-- Desktop table -->
        <table class="rank-table">
          <thead>
            <tr class="table-head-row">
              <th class="th w-16">Pos.</th>
              <th class="th">Candidato</th>
              <th class="th">Avaliação</th>
              <th class="th text-center">Acertos</th>
              <th class="th text-center">Precisão</th>
              <th class="th text-right">Data</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(item, index) in ranking" :key="index"
                class="table-row"
                :class="{
                  'table-row--gold':   index === 0,
                  'table-row--silver': index === 1,
                  'table-row--bronze': index === 2,
                }">
              <td class="td text-center">
                <div v-if="index < 3" class="medal"
                     :class="{ 'medal--gold': index===0, 'medal--silver': index===1, 'medal--bronze': index===2 }">
                  <span v-if="index===0">🥇</span>
                  <span v-else-if="index===1">🥈</span>
                  <span v-else>🥉</span>
                </div>
                <span v-else class="rank-num">{{ index + 1 }}°</span>
              </td>
              <td class="td">
                <div class="user-cell">
                  <div class="user-avatar">{{ item.aluno_username.charAt(0).toUpperCase() }}</div>
                  <span class="user-name">{{ item.aluno_username }}</span>
                </div>
              </td>
              <td class="td text-comet text-sm">{{ item.simulado_titulo }}</td>
              <td class="td text-center text-star font-semibold text-sm">{{ item.acertos }} / {{ item.total_questoes }}</td>
              <td class="td text-center">
                <span class="score-badge" :class="scoreBg(item.score)">{{ item.score }}%</span>
              </td>
              <td class="td text-right text-dust text-sm">{{ formatarData(item.realizado_em) }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Mobile list -->
        <div class="mobile-list">
          <div v-for="(item, index) in ranking" :key="index" class="mobile-row">
            <div class="mobile-medal" v-if="index < 3"
                 :class="{ 'medal--gold': index===0, 'medal--silver': index===1, 'medal--bronze': index===2 }">
              <span v-if="index===0">🥇</span>
              <span v-else-if="index===1">🥈</span>
              <span v-else>🥉</span>
            </div>
            <span v-else class="mobile-rank">{{ index + 1 }}°</span>
            <div class="mobile-info">
              <p class="user-name">{{ item.aluno_username }}</p>
              <p class="mobile-sim">{{ item.simulado_titulo }}</p>
            </div>
            <span class="score-badge" :class="scoreBg(item.score)">{{ item.score }}%</span>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api.js'
import DashboardLayout from '../layouts/DashboardLayout.vue'

const username = localStorage.getItem('username') || ''
const isAdmin = localStorage.getItem('user_role') === 'admin'
const ranking = ref([])
const carregando = ref(true)
const erro = ref('')

onMounted(async () => {
  try {
    const response = await api.get('/api/resultados/ranking/')
    ranking.value = response.data
  } catch {
    erro.value = 'Erro de conexão com o laboratório.'
  } finally {
    carregando.value = false
  }
})

function scoreBg(score) {
  const v = parseFloat(score)
  if (v >= 70) return 'score--stellar'
  if (v >= 50) return 'score--flare'
  return 'score--nova'
}

function formatarData(data) {
  return new Date(data).toLocaleDateString('pt-BR')
}
</script>

<style scoped>
.page-header { margin-bottom: 32px; }
.page-title {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
}
.page-sub { font-size: 0.875rem; color: #64748b; margin-top: 4px; }

.alert {
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 0.875rem;
  margin-bottom: 20px;
}
.alert--error { background: #fef2f2; border: 1px solid #fecaca; color: #b91c1c; }

/* Skeleton */
.skeleton-list { display: flex; flex-direction: column; gap: 8px; }
.skeleton-row {
  height: 56px;
  background: #f1f5f9;
  border-radius: 10px;
  position: relative;
  overflow: hidden;
}
.skeleton-row::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
  animation: shimmer 1.5s infinite;
}
@keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

/* Empty state */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 56px 32px;
  background: #ffffff;
  border: 1px dashed #e2e8f0;
  border-radius: 16px;
}
.empty-icon { font-size: 2.5rem; color: #2563eb; margin-bottom: 20px; }
.empty-title {
  font-family: var(--font-display);
  font-size: 1.125rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 8px;
}
.empty-sub { font-size: 0.875rem; color: #64748b; }

/* Table */
.rank-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}
.rank-table { width: 100%; border-collapse: collapse; }
.table-head-row { background: #f8fafc; border-bottom: 1px solid #e2e8f0; }
.th {
  padding: 12px 20px;
  text-align: left;
  font-size: 0.7rem;
  font-family: var(--font-body);
  font-weight: 600;
  color: #64748b;
  text-transform: uppercase;
  letter-spacing: 0.06em;
}
.text-center { text-align: center; }
.text-right { text-align: right; }
.td { padding: 14px 20px; vertical-align: middle; border-bottom: 1px solid #f1f5f9; }
.table-row { transition: background 0.12s ease; }
.table-row:hover { background: #f8fafc; }
.table-row--gold   { background: #fffbeb; }
.table-row--silver { background: #f8fafc; }
.table-row--bronze { background: #fff7ed; }

.medal {
  width: 32px; height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  margin: 0 auto;
}
.medal--gold   { background: #fef3c7; }
.medal--silver { background: #f1f5f9; }
.medal--bronze { background: #ffedd5; }

.rank-num { font-size: 0.875rem; font-weight: 700; color: #94a3b8; }

.user-cell { display: flex; align-items: center; gap: 12px; }
.user-avatar {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2563eb;
  font-size: 0.875rem;
  font-weight: 700;
  flex-shrink: 0;
}
.user-name { font-size: 0.875rem; font-weight: 600; color: #0f172a; }

.score-badge {
  display: inline-block;
  padding: 3px 10px;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 700;
  border: 1px solid transparent;
}
.score--stellar { background: #f0fdf4; color: #166534; border-color: #bbf7d0; }
.score--flare   { background: #fffbeb; color: #92400e; border-color: #fde68a; }
.score--nova    { background: #fef2f2; color: #b91c1c; border-color: #fecaca; }

.text-comet { color: #64748b; }
.text-star  { color: #0f172a; }
.text-dust  { color: #94a3b8; }
.text-sm    { font-size: 0.875rem; }
.font-semibold { font-weight: 600; }

/* Mobile list */
.rank-table { display: table; }
.mobile-list { display: none; }

@media (max-width: 640px) {
  .rank-table { display: none; }
  .mobile-list { display: block; }
  .mobile-row {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 14px 20px;
    border-bottom: 1px solid #f1f5f9;
  }
  .mobile-medal {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
  }
  .mobile-rank { width: 32px; text-align: center; font-size: 0.875rem; font-weight: 700; color: #94a3b8; flex-shrink: 0; }
  .mobile-info { flex: 1; min-width: 0; }
  .mobile-sim { font-size: 0.75rem; color: #94a3b8; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
}
</style>

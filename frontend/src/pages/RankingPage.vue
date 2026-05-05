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
.page-header { margin-bottom: var(--space-8); }
.page-title {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: var(--weight-bold);
  color: var(--color-star);
}
.page-sub { font-size: var(--text-sm); color: var(--color-comet); margin-top: var(--space-1); }

.alert {
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  margin-bottom: var(--space-5);
}
.alert--error { background: var(--color-nova-dim); border: 1px solid var(--color-nova-border); color: var(--color-nova); }

/* Skeleton */
.skeleton-list { display: flex; flex-direction: column; gap: var(--space-2); }
.skeleton-row {
  height: 56px;
  background: var(--color-nebula);
  border-radius: var(--radius-md);
  position: relative;
  overflow: hidden;
}
.skeleton-row::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent);
  animation: shimmer 1.5s infinite;
}
@keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

/* Empty state */
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: var(--space-14) var(--space-8);
  background: var(--color-nebula);
  border: 1px dashed var(--color-border);
  border-radius: var(--radius-xl);
}
.empty-icon { font-size: 2.5rem; color: var(--color-orbit); margin-bottom: var(--space-5); }
.empty-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  margin-bottom: var(--space-2);
}
.empty-sub { font-size: var(--text-sm); color: var(--color-comet); }

/* Table */
.rank-card {
  background: var(--color-nebula);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  overflow: hidden;
}
.rank-table { width: 100%; border-collapse: collapse; }
.table-head-row { border-bottom: 1px solid var(--color-border); }
.th {
  padding: var(--space-3) var(--space-5);
  text-align: left;
  font-size: var(--text-2xs);
  font-family: var(--font-mono);
  font-weight: var(--weight-bold);
  color: var(--color-dust);
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
.text-center { text-align: center; }
.text-right { text-align: right; }
.td { padding: var(--space-4) var(--space-5); vertical-align: middle; border-bottom: 1px solid rgba(255,255,255,0.03); }
.table-row { transition: background var(--transition-fast); }
.table-row:hover { background: rgba(255,255,255,0.02); }
.table-row--gold   { background: rgba(255,214,0,0.03); }
.table-row--silver { background: rgba(203,213,225,0.02); }
.table-row--bronze { background: rgba(194,120,63,0.02); }

.medal {
  width: 32px; height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  margin: 0 auto;
}
.medal--gold   { background: rgba(255,214,0,0.1); }
.medal--silver { background: rgba(203,213,225,0.1); }
.medal--bronze { background: rgba(194,120,63,0.1); }

.rank-num { font-size: var(--text-sm); font-weight: var(--weight-bold); color: var(--color-dust); }

.user-cell { display: flex; align-items: center; gap: var(--space-3); }
.user-avatar {
  width: 32px; height: 32px;
  border-radius: 50%;
  background: rgba(0,229,255,0.1);
  border: 1px solid rgba(0,229,255,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-orbit);
  font-size: var(--text-sm);
  font-weight: var(--weight-bold);
  flex-shrink: 0;
}
.user-name { font-size: var(--text-sm); font-weight: var(--weight-semibold); color: var(--color-star); }

.score-badge {
  display: inline-block;
  padding: 3px var(--space-2);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-family: var(--font-mono);
  font-weight: var(--weight-bold);
  color: white;
}
.score--stellar { background: var(--color-stellar); }
.score--flare   { background: var(--color-flare); }
.score--nova    { background: var(--color-nova); }

.text-comet { color: var(--color-comet); }
.text-star  { color: var(--color-star); }
.text-dust  { color: var(--color-dust); }
.text-sm    { font-size: var(--text-sm); }
.font-semibold { font-weight: var(--weight-semibold); }

/* Mobile list */
.rank-table { display: table; }
.mobile-list { display: none; }

@media (max-width: 640px) {
  .rank-table { display: none; }
  .mobile-list { display: block; }
  .mobile-row {
    display: flex;
    align-items: center;
    gap: var(--space-4);
    padding: var(--space-4) var(--space-5);
    border-bottom: 1px solid var(--color-border);
  }
  .mobile-medal {
    width: 32px; height: 32px;
    border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.1rem;
    flex-shrink: 0;
  }
  .mobile-rank { width: 32px; text-align: center; font-size: var(--text-sm); font-weight: var(--weight-bold); color: var(--color-dust); flex-shrink: 0; }
  .mobile-info { flex: 1; min-width: 0; }
  .mobile-sim { font-size: var(--text-xs); color: var(--color-dust); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
}
</style>

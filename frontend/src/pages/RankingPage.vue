<template>
  <div class="dashboard-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1 class="logo-text">
          <span class="logo-white">SIMUS</span><span class="logo-accent">LAB</span>
        </h1>
        <p class="tagline">Performance Lab</p>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-link">
          <span class="icon">📊</span> Dashboard
        </router-link>
        <router-link to="/simulados" class="nav-link">
          <span class="icon">🎯</span> Avaliações
        </router-link>
        <router-link to="/ranking" class="nav-link active">
          <span class="icon">🏆</span> Ranking Geral
        </router-link>
        <router-link v-if="isAdmin" to="/admin/alunos" class="nav-link link-admin">
          <span class="icon">🛡️</span> Admin
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <button @click="logout" class="btn-logout-clean">Sair</button>
      </div>
    </aside>

    <main class="main-content">
      <header class="top-bar">
        <div class="welcome-msg">
          <h2>Ranking Geral</h2>
          <p class="text-secondary">Os melhores desempenhos do laboratório.</p>
        </div>
      </header>

      <div v-if="erro" class="status-msg erro">{{ erro }}</div>

      <div v-else-if="carregando" class="skeleton-wrapper">
        <div class="skeleton-box shimmer" style="height: 60px; margin-bottom: 10px;"></div>
        <div class="skeleton-box shimmer" style="height: 60px; margin-bottom: 10px;" v-for="n in 5" :key="n"></div>
      </div>

      <div v-else class="ranking-container">
        
        <div v-if="ranking.length === 0" class="empty-state-card clean-card">
          <div class="empty-icon-wrapper"><span class="empty-icon">🏆</span></div>
          <h3 class="empty-title">Ranking em formação.</h3>
          <p class="empty-subtitle">Seja o primeiro a completar uma avaliação e conquiste o topo do laboratório.</p>
        </div>

        <div v-else class="tabela-wrapper clean-card">
          <table class="tabela">
            <thead>
              <tr>
                <th class="th-posicao">Posição</th>
                <th>Candidato</th>
                <th>Avaliação</th>
                <th class="th-center">Acertos</th>
                <th class="th-center">Precisão</th>
                <th class="th-right">Data</th>
              </tr>
            </thead>
            <tbody>
              <tr 
                v-for="(item, index) in ranking" 
                :key="index"
                :class="{ 'destaque-ouro': index === 0, 'destaque-prata': index === 1, 'destaque-bronze': index === 2 }"
              >
                <td class="td-posicao">
                  <div class="medal-badge" :class="'medal-' + index" v-if="index < 3">
                    <span v-if="index === 0">🥇</span>
                    <span v-else-if="index === 1">🥈</span>
                    <span v-else-if="index === 2">🥉</span>
                  </div>
                  <span v-else class="pos-numero">{{ index + 1 }}º</span>
                </td>

                <td class="td-aluno">
                  <div class="aluno-info">
                    <span class="aluno-avatar">{{ item.aluno_username.charAt(0).toUpperCase() }}</span>
                    <span class="aluno-nome">{{ item.aluno_username }}</span>
                  </div>
                </td>
                
                <td class="td-simulado">{{ item.simulado_titulo }}</td>
                <td class="td-acertos th-center">{{ item.acertos }} / {{ item.total_questoes }}</td>
                <td class="td-score th-center">
                  <span class="score-badge" :class="corScore(item.score)">{{ item.score }}%</span>
                </td>
                <td class="td-data th-right">{{ formatarData(item.realizado_em) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
// LÓGICA INTACTA
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'

const router = useRouter()
const ranking = ref([])
const carregando = ref(true)
const erro = ref('')
const isAdmin = ref(localStorage.getItem('user_role') === 'admin')

onMounted(async () => {
  try {
    const response = await api.get('/api/resultados/ranking/') // Consertado para garantir o /api/
    ranking.value = response.data
  } catch (error) {
    erro.value = 'Erro de conexão com o laboratório.'
  } finally {
    carregando.value = false
  }
})

function corScore(score) {
  const valor = parseFloat(score)
  if (valor >= 70) return 'bg-green'
  if (valor >= 50) return 'bg-orange'
  return 'bg-red'
}

function formatarData(data) {
  return new Date(data).toLocaleDateString('pt-BR')
}

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_role')  
  router.push({ name: 'login' })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.dashboard-layout {
  display: flex; min-height: 100vh; width: 100vw; position: absolute;
  top: 0; left: 0; background-color: #F1F5F9; font-family: 'Inter', sans-serif;
}

/* Sidebar (Idêntica ao Dashboard) */
.sidebar {
  width: 220px; background: linear-gradient(180deg, #0A2540 0%, #0052FF 100%);
  color: white; display: flex; flex-direction: column; padding: 30px 20px;
  position: fixed; height: 100vh; z-index: 100;
}
.logo-white { color: #FFFFFF; font-weight: 800; font-size: 1.3rem; }
.logo-accent { color: #00D09C; font-weight: 800; font-size: 1.3rem; }
.tagline { font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1.2px; opacity: 0.7; margin-top: 2px; }

.sidebar-nav { margin-top: 40px; flex: 1; }
.nav-link {
  display: flex; align-items: center; gap: 10px; color: rgba(255, 255, 255, 0.8);
  text-decoration: none; padding: 12px 14px; border-radius: 8px; margin-bottom: 5px;
  font-weight: 500; font-size: 0.9rem; transition: all 0.2s;
}
.nav-link:hover, .nav-link.active { background: rgba(255, 255, 255, 0.15); color: white; }

.btn-logout-clean {
  background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2);
  color: white; width: 100%; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.85rem;
}
.btn-logout-clean:hover { background: #EF4444; border-color: #EF4444; }

/* Main Content */
.main-content { flex: 1; margin-left: 220px; padding: 40px 50px; }
.top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 35px; }
.welcome-msg h2 { font-size: 1.7rem; font-weight: 700; color: #0F172A; margin: 0; }
.text-secondary { color: #475569; font-size: 0.9rem; margin-top: 4px; }

/* UI Clean Tech */
.clean-card {
  background: white; border: 1px solid #E2E8F0; border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Skeleton */
.skeleton-wrapper { width: 100%; }
.shimmer { position: relative; overflow: hidden; background-color: #E2E8F0; border-radius: 8px; }
.shimmer::after {
  content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent);
  animation: loading 1.5s infinite;
}
@keyframes loading { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

/* Tabela Profissional */
.tabela-wrapper { overflow-x: auto; }
.tabela { width: 100%; border-collapse: collapse; white-space: nowrap; }

.tabela thead { background: #F8FAFC; border-bottom: 2px solid #E2E8F0; }
.tabela th { padding: 16px 24px; text-align: left; font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; }
.th-center { text-align: center !important; }
.th-right { text-align: right !important; }

.tabela tbody tr { border-bottom: 1px solid #F1F5F9; transition: background 0.2s; }
.tabela tbody tr:hover { background: #F8FAFC; }

/* Destaques Top 3 */
.destaque-ouro { background: linear-gradient(90deg, rgba(250, 214, 38, 0.05) 0%, transparent 100%); }
.destaque-prata { background: linear-gradient(90deg, rgba(203, 213, 225, 0.1) 0%, transparent 100%); }
.destaque-bronze { background: linear-gradient(90deg, rgba(217, 119, 6, 0.05) 0%, transparent 100%); }

.tabela td { padding: 16px 24px; font-size: 0.9rem; color: #1E293B; vertical-align: middle; }

/* Posição e Medalhas */
.td-posicao { width: 80px; }
.pos-numero { font-weight: 700; color: #94A3B8; font-size: 1rem; }
.medal-badge { width: 32px; height: 32px; display: flex; align-items: center; justify-content: center; border-radius: 50%; font-size: 1.2rem; }
.medal-0 { background: #FEF08A; box-shadow: 0 0 10px rgba(250, 214, 38, 0.4); }
.medal-1 { background: #E2E8F0; }
.medal-2 { background: #FED7AA; }

/* Aluno Avatar */
.aluno-info { display: flex; align-items: center; gap: 12px; }
.aluno-avatar { 
  width: 32px; height: 32px; background: #0052FF; color: white; 
  border-radius: 50%; display: flex; align-items: center; justify-content: center; 
  font-weight: 700; font-size: 0.85rem; 
}
.aluno-nome { font-weight: 600; }

.td-simulado { color: #475569; font-weight: 500; }
.td-acertos { color: #64748B; font-weight: 600; }
.td-data { color: #94A3B8; font-size: 0.85rem; }

/* Score Badges */
.score-badge { padding: 4px 10px; border-radius: 20px; font-weight: 700; font-size: 0.85rem; color: white; }
.bg-green { background-color: #10B981; }
.bg-orange { background-color: #F59E0B; }
.bg-red { background-color: #EF4444; }

/* Empty State */
.empty-state-card {
  padding: 60px 40px; text-align: center; border-radius: 16px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.empty-icon-wrapper { width: 80px; height: 80px; background: #EFF6FF; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 24px; }
.empty-icon { font-size: 2.5rem; }
.empty-title { font-size: 1.4rem; font-weight: 700; color: #0F172A; margin-bottom: 12px; }
.empty-subtitle { color: #64748B; max-width: 500px; font-size: 0.95rem; }

/* Responsivo */
@media (max-width: 1000px) {
  .sidebar { width: 70px; padding: 30px 10px; }
  .logo-text, .tagline, .nav-link span:not(.icon), .btn-logout-clean { display: none; }
  .main-content { margin-left: 70px; padding: 20px; }
}

@media (max-width: 600px) {
  .tabela thead { display: none; }
  .tabela tbody tr { display: flex; flex-direction: column; padding: 15px; position: relative; }
  .tabela td { padding: 5px 0; text-align: left !important; border: none; }
  .td-posicao { position: absolute; top: 15px; right: 15px; width: auto; }
  .aluno-info { margin-bottom: 10px; }
  .td-score { position: absolute; bottom: 15px; right: 15px; }
}
</style>
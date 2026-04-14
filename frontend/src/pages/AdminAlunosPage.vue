<template>
  <div class="dashboard-layout">
    
    <aside class="sidebar admin-sidebar">
      <div class="sidebar-header">
        <h1 class="logo-text">
          <span class="logo-white">SIMUS</span><span class="logo-accent">LAB</span>
        </h1>
        <p class="tagline">Comando Admin</p>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/admin/alunos" class="nav-link active">
          <span class="icon">👥</span> Gestão de Alunos
        </router-link>
        <router-link to="/admin/importar" class="nav-link">
          <span class="icon">📥</span> Importar Questões
        </router-link>
        <router-link to="/simulados" class="nav-link">
          <span class="icon">🎯</span> Ver Avaliações
        </router-link>
        <router-link to="/ranking" class="nav-link">
          <span class="icon">🏆</span> Ranking Geral
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <button @click="logout" class="btn-logout-clean">Sair do Sistema</button>
      </div>
    </aside>

    <main class="main-content">
      <header class="top-bar">
        <div class="welcome-msg">
          <h2>Gestão de Alunos</h2>
          <p class="text-secondary">Visão geral e acesso aos relatórios individuais de performance.</p>
        </div>
        <div class="admin-badge">Modo Administrador</div>
      </header>

      <div v-if="carregando" class="skeleton-wrapper">
        <div class="skeleton-box shimmer" style="height: 60px; margin-bottom: 10px;"></div>
        <div class="skeleton-box shimmer" style="height: 60px; margin-bottom: 10px;" v-for="n in 6" :key="n"></div>
      </div>

      <div v-else-if="erro" class="empty-state-card clean-card">
        <div class="empty-icon-wrapper error-wrapper"><span class="empty-icon">⚠️</span></div>
        <h3 class="empty-title">Falha de Conexão</h3>
        <p class="empty-subtitle">{{ erro }}</p>
        <button @click="recarregar" class="btn-primary-action">Tentar Novamente</button>
      </div>

      <div v-else class="data-container">
        
        <div v-if="alunos.length === 0" class="empty-state-card clean-card">
          <div class="empty-icon-wrapper"><span class="empty-icon">👥</span></div>
          <h3 class="empty-title">Nenhum Registro</h3>
          <p class="empty-subtitle">O banco de dados de alunos está vazio no momento.</p>
        </div>

        <div class="table-wrapper clean-card" v-else>
          <div class="table-header">
            <h3 class="table-title">Base de Candidatos Cadastrados</h3>
            <span class="total-badge">{{ alunos.length }} alunos</span>
          </div>

          <table class="data-table">
            <thead>
              <tr>
                <th>Candidato</th>
                <th class="th-center">Avaliações</th>
                <th class="th-center">Desempenho Geral</th>
                <th class="th-right">Relatório Tático</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="aluno in alunos" :key="aluno.id">
                
                <td class="td-profile">
                  <div class="profile-meta">
                    <div class="profile-avatar">{{ aluno.username.charAt(0).toUpperCase() }}</div>
                    <div class="profile-text">
                      <span class="profile-name">{{ aluno.username }}</span>
                      <span class="profile-email">{{ aluno.email }}</span>
                    </div>
                  </div>
                </td>

                <td class="td-center">
                  <span class="simulados-count" :class="{ 'zero-count': aluno.total_simulados === 0 }">
                    {{ aluno.total_simulados }}
                  </span>
                </td>

                <td class="td-center">
                  <span v-if="aluno.total_simulados > 0" class="score-pill" :class="corScoreBg(aluno.score_medio)">
                    {{ aluno.score_medio }}%
                  </span>
                  <span v-else class="text-gray italic">Sem dados</span>
                </td>

                <td class="td-right">
                  <button
                    @click="verDashboard(aluno.id)"
                    class="btn-report"
                    :disabled="aluno.total_simulados === 0"
                  >
                    Ver Relatório
                  </button>
                </td>

              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'

const router = useRouter()
const alunos = ref([])
const carregando = ref(true)
const erro = ref('')

async function carregarAlunos() {
  carregando.value = true
  erro.value = ''
  try {
    // ATUALIZADO: Rota API com /api/
    const response = await api.get('/api/resultados/admin/alunos/')
    alunos.value = response.data
  } catch (error) {
    erro.value = 'Falha ao sincronizar o banco de dados de alunos.'
  } finally {
    carregando.value = false
  }
}

onMounted(carregarAlunos)

function recarregar() {
  carregarAlunos()
}

function verDashboard(id) {
  router.push({ name: 'admin-aluno-dashboard', params: { id } })
}

function corScoreBg(valor) {
  if (valor >= 70) return 'bg-green'
  if (valor >= 50) return 'bg-orange'
  return 'bg-red'
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

/* Base & Layout */
.dashboard-layout { display: flex; min-height: 100vh; width: 100vw; position: absolute; top: 0; left: 0; background-color: #F8FAFC; font-family: 'Inter', sans-serif; }

/* Sidebar do Admin */
.admin-sidebar { width: 220px; background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%); color: white; display: flex; flex-direction: column; padding: 30px 20px; position: fixed; height: 100vh; z-index: 100; border-right: 1px solid #334155; }
.logo-white { color: #FFFFFF; font-weight: 800; font-size: 1.3rem; }
.logo-accent { color: #38BDF8; font-weight: 800; font-size: 1.3rem; }
.tagline { font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1.2px; color: #94A3B8; margin-top: 2px; }
.sidebar-nav { margin-top: 40px; flex: 1; }
.nav-link { display: flex; align-items: center; gap: 10px; color: #94A3B8; text-decoration: none; padding: 12px 14px; border-radius: 8px; margin-bottom: 5px; font-weight: 500; font-size: 0.9rem; transition: all 0.2s; }
.nav-link:hover, .nav-link.active { background: rgba(255, 255, 255, 0.1); color: white; }
.btn-logout-clean { background: transparent; border: 1px solid #475569; color: #CBD5E1; width: 100%; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.85rem; transition: all 0.2s; }
.btn-logout-clean:hover { background: #EF4444; border-color: #EF4444; color: white; }

/* Main Content */
.main-content { flex: 1; margin-left: 220px; padding: 30px 50px; }
.top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
.welcome-msg h2 { font-size: 1.7rem; font-weight: 700; color: #0F172A; margin: 0; }
.text-secondary { color: #475569; font-size: 0.9rem; margin-top: 4px; }
.admin-badge { background: #1E293B; color: white; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; padding: 5px 12px; border-radius: 20px; }

/* Utils */
.clean-card { background: white; border: 1px solid #E2E8F0; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03); }
.text-gray { color: #94A3B8; } .italic { font-style: italic; }
.bg-green { background-color: #10B981; } .bg-orange { background-color: #F59E0B; } .bg-red { background-color: #EF4444; }

/* Skeleton */
.skeleton-wrapper { width: 100%; }
.shimmer { position: relative; overflow: hidden; background-color: #E2E8F0; border-radius: 12px; }
.shimmer::after { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent); animation: loading 1.5s infinite; }
@keyframes loading { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

/* Empty State & Error */
.empty-state-card { text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px; margin-top: 20px; }
.empty-icon-wrapper { width: 80px; height: 80px; background: #F1F5F9; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 20px; }
.error-wrapper { background: #FEF2F2 !important; }
.empty-icon { font-size: 2.5rem; }
.empty-title { font-size: 1.3rem; font-weight: 700; color: #0F172A; margin-bottom: 10px; }
.empty-subtitle { color: #64748B; font-size: 0.95rem; }
.btn-primary-action { background: #0052FF; color: white; padding: 12px 24px; border-radius: 8px; font-weight: 600; border: none; cursor: pointer; margin-top: 20px; transition: all 0.2s; }
.btn-primary-action:hover { background: #0043D1; transform: translateY(-2px); }

/* Tabela de Alunos */
.table-wrapper { overflow-x: auto; }
.table-header { display: flex; justify-content: space-between; align-items: center; padding: 20px 25px; border-bottom: 1px solid #E2E8F0; }
.table-title { font-size: 1.1rem; font-weight: 700; color: #0F172A; margin: 0; }
.total-badge { background: #F1F5F9; color: #475569; padding: 4px 12px; border-radius: 20px; font-size: 0.8rem; font-weight: 600; }

.data-table { width: 100%; border-collapse: collapse; white-space: nowrap; }
.data-table thead { background: #F8FAFC; border-bottom: 2px solid #E2E8F0; }
.data-table th { padding: 16px 25px; text-align: left; font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; }
.data-table tbody tr { border-bottom: 1px solid #F1F5F9; transition: background 0.2s; }
.data-table tbody tr:hover { background: #F8FAFC; }
.data-table td { padding: 16px 25px; vertical-align: middle; }

.th-center, .td-center { text-align: center !important; }
.th-right, .td-right { text-align: right !important; }

/* Profile na Tabela */
.td-profile { width: 40%; }
.profile-meta { display: flex; align-items: center; gap: 15px; }
.profile-avatar { width: 40px; height: 40px; background: #E0E7FF; color: #4338CA; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 1rem; }
.profile-text { display: flex; flex-direction: column; gap: 2px; }
.profile-name { font-weight: 600; color: #1E293B; font-size: 0.95rem; }
.profile-email { font-size: 0.8rem; color: #64748B; }

/* Badges e Botões na Tabela */
.simulados-count { font-weight: 700; color: #0F172A; font-size: 0.95rem; }
.zero-count { color: #94A3B8; }
.score-pill { color: white; font-weight: 700; font-size: 0.85rem; padding: 4px 12px; border-radius: 20px; }

.btn-report { background: #EFF6FF; color: #0052FF; border: 1px solid #BFDBFE; padding: 8px 16px; border-radius: 6px; font-weight: 600; font-size: 0.85rem; cursor: pointer; transition: all 0.2s; }
.btn-report:hover:not(:disabled) { background: #0052FF; color: white; border-color: #0052FF; }
.btn-report:disabled { background: #F1F5F9; color: #94A3B8; border-color: #E2E8F0; cursor: not-allowed; }

@media (max-width: 1000px) {
  .admin-sidebar { width: 70px; padding: 30px 10px; }
  .logo-text, .tagline, .nav-link span:not(.icon), .btn-logout-clean { display: none; }
  .main-content { margin-left: 70px; padding: 20px; }
}
</style>
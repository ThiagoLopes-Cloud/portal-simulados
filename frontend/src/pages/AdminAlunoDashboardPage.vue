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
      
      <div v-if="carregando" class="skeleton-wrapper">
        <header class="top-bar">
          <div class="skeleton-box shimmer" style="width: 200px; height: 40px;"></div>
        </header>
        <div class="skeleton-box shimmer" style="height: 100px; margin-bottom: 30px;"></div>
        <div class="kpi-grid">
          <div class="skeleton-box shimmer" style="height: 120px;" v-for="n in 4" :key="n"></div>
        </div>
      </div>

      <div v-else-if="erro" class="empty-state-card clean-card">
        <div class="empty-icon-wrapper error-wrapper"><span class="empty-icon">⚠️</span></div>
        <h3 class="empty-title">Falha de Leitura</h3>
        <p class="empty-subtitle">{{ erro }}</p>
        <button @click="$router.push('/admin/alunos')" class="btn-primary-action">Voltar para Base de Alunos</button>
      </div>

      <div v-else class="analytics-container">

        <header class="top-bar">
          <div class="breadcrumb">
            <button @click="$router.push('/admin/alunos')" class="btn-back">
              <span class="back-icon">←</span> Voltar para Base
            </button>
          </div>
          <div class="admin-badge">Modo Administrador</div>
        </header>

        <div class="aluno-profile-card clean-card">
          <div class="profile-avatar">{{ dados.aluno.username.charAt(0).toUpperCase() }}</div>
          <div class="profile-info">
            <h2 class="profile-name">{{ dados.aluno.username }}</h2>
            <p class="profile-email">{{ dados.aluno.email }}</p>
          </div>
          <div class="profile-status">
            <span class="status-indicator">Ativo no Laboratório</span>
          </div>
        </div>

        <div class="kpi-grid">
          <div class="kpi-card clean-card">
            <span class="kpi-value" :class="corScoreText(dados.score_geral)">{{ dados.score_geral }}%</span>
            <span class="kpi-label">Aproveitamento Geral</span>
          </div>
          <div class="kpi-card clean-card">
            <span class="kpi-value text-primary">{{ dados.total_simulados }}</span>
            <span class="kpi-label">Avaliações Realizadas</span>
          </div>
          <div class="kpi-card clean-card">
            <span class="kpi-value text-purple">{{ dados.por_materia.length }}</span>
            <span class="kpi-label">Disciplinas Mapeadas</span>
          </div>
          <div class="kpi-card clean-card">
            <span class="kpi-value" :class="corScoreText(dados.por_materia.length > 0 ? dados.por_materia[0].percentual : 0)">
              {{ pontoFraco }}
            </span>
            <span class="kpi-label">Ponto de Atenção Crítico</span>
          </div>
        </div>

        <div class="data-split">
          
          <section class="analysis-section">
            <h3 class="section-title">Análise de Disciplinas</h3>
            
            <div v-if="dados.por_materia.length === 0" class="empty-list-card clean-card">
              Sem dados suficientes para gerar relatório tático.
            </div>

            <div v-for="materia in dados.por_materia" :key="materia.codigo" class="subject-analysis-card clean-card">
              
              <div class="subject-header" @click="toggleMateria(materia.codigo)">
                <div class="subj-meta">
                  <span class="subj-badge">{{ materia.codigo }}</span>
                  <span class="subj-name">{{ materia.materia }}</span>
                  <span class="subj-volume">{{ materia.acertos }}/{{ materia.total_questoes }} corretas</span>
                </div>
                <div class="subj-stats">
                  <div class="progress-bar-thin">
                    <div class="progress-fill-thin" :class="corScoreBg(materia.percentual)" :style="{ width: materia.percentual + '%' }"></div>
                  </div>
                  <span class="subj-score" :class="corScoreText(materia.percentual)">{{ materia.percentual }}%</span>
                  <span class="subj-trend" :class="materia.diferenca_media >= 0 ? 'trend-up' : 'trend-down'">
                    {{ materia.diferenca_media >= 0 ? '▲ +' : '▼ ' }}{{ materia.diferenca_media }}% vs média
                  </span>
                  <span class="toggle-icon">{{ materiasAbertas.includes(materia.codigo) ? '▲' : '▼' }}</span>
                </div>
              </div>

              <div v-if="materiasAbertas.includes(materia.codigo)" class="themes-breakdown">
                <div class="themes-legend">
                  <span>Métrica do Aluno</span>
                  <span>Média da Base</span>
                </div>
                
                <div v-for="tema in materia.temas" :key="tema.tema" class="theme-row">
                  <div class="theme-info">
                    <span class="theme-name">{{ tema.tema }}</span>
                    <span class="theme-vol">{{ tema.acertos }}/{{ tema.total }} acertos</span>
                  </div>
                  
                  <div class="theme-charts">
                    <div class="chart-line">
                      <span class="chart-label text-primary">Aluno</span>
                      <div class="chart-bar-bg">
                        <div class="chart-bar-fill" :class="corScoreBg(tema.percentual)" :style="{ width: tema.percentual + '%' }"></div>
                      </div>
                      <span class="chart-value" :class="corScoreText(tema.percentual)">{{ tema.percentual }}%</span>
                    </div>
                    <div class="chart-line">
                      <span class="chart-label text-gray">Média</span>
                      <div class="chart-bar-bg">
                        <div class="chart-bar-fill bg-gray" :style="{ width: tema.media_plataforma + '%' }"></div>
                      </div>
                      <span class="chart-value text-gray">{{ tema.media_plataforma }}%</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </section>

          <section class="history-section">
            <h3 class="section-title">Registro de Atividades</h3>
            
            <div v-if="dados.historico.length === 0" class="empty-list-card clean-card">
              Nenhum registro de avaliação no banco de dados.
            </div>
            
            <div class="table-wrapper clean-card" v-else>
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Simulação</th>
                    <th class="th-center">Acertos</th>
                    <th class="th-center">Precisão</th>
                    <th class="th-right">Data</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="item in dados.historico" :key="item.simulado_id">
                    <td class="td-title">{{ item.simulado }}</td>
                    <td class="td-center">{{ item.acertos }}/{{ item.total }}</td>
                    <td class="td-center"><span class="score-pill" :class="corScoreBg(item.score)">{{ item.score }}%</span></td>
                    <td class="td-right td-date">{{ item.data }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </section>

        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../services/api.js'

const router = useRouter()
const route = useRoute()
const carregando = ref(true)
const erro = ref('')
const materiasAbertas = ref([])

const dados = ref({
  aluno: { username: '', email: '' },
  score_geral: 0,
  total_simulados: 0,
  por_materia: [],
  historico: [],
})

const pontoFraco = computed(() => {
  if (dados.value.por_materia.length === 0) return 'N/A'
  return dados.value.por_materia[0].codigo
})

onMounted(async () => {
  try {
    const response = await api.get(`/api/resultados/admin/alunos/${route.params.id}/`)
    dados.value = response.data

    if (dados.value.por_materia.length > 0) {
      materiasAbertas.value = [dados.value.por_materia[0].codigo]
    }
  } catch (error) {
    erro.value = 'Falha ao extrair dados do candidato. Verifique a conexão.'
  } finally {
    carregando.value = false
  }
})

function toggleMateria(codigo) {
  const index = materiasAbertas.value.indexOf(codigo)
  if (index === -1) materiasAbertas.value.push(codigo)
  else materiasAbertas.value.splice(index, 1)
}

function corScoreText(v) { return v >= 70 ? 'text-green' : v >= 50 ? 'text-orange' : 'text-red'; }
function corScoreBg(v) { return v >= 70 ? 'bg-green' : v >= 50 ? 'bg-orange' : 'bg-red'; }

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

/* Sidebar do Admin (Mais Sóbria) */
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

/* Top Bar */
.top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
.btn-back { background: white; border: 1px solid #E2E8F0; padding: 8px 16px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; color: #475569; cursor: pointer; transition: all 0.2s; display: flex; align-items: center; gap: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.02); }
.btn-back:hover { border-color: #0052FF; color: #0052FF; }
.admin-badge { background: #1E293B; color: white; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; padding: 5px 12px; border-radius: 20px; }

/* Utils */
.clean-card { background: white; border: 1px solid #E2E8F0; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03); }
.section-title { font-size: 1.1rem; font-weight: 700; color: #0F172A; margin: 0 0 20px 0; }
.text-green { color: #10B981; } .text-orange { color: #F59E0B; } .text-red { color: #EF4444; } .text-primary { color: #0052FF; } .text-purple { color: #7C3AED; } .text-gray { color: #64748B; }
.bg-green { background-color: #10B981; } .bg-orange { background-color: #F59E0B; } .bg-red { background-color: #EF4444; } .bg-gray { background-color: #CBD5E1; }

/* Skeleton & Errors */
.skeleton-wrapper { width: 100%; }
.shimmer { position: relative; overflow: hidden; background-color: #E2E8F0; border-radius: 12px; }
.shimmer::after { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent); animation: loading 1.5s infinite; }
@keyframes loading { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }
.empty-state-card { text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px; margin-top: 20px; }
.empty-icon-wrapper { width: 80px; height: 80px; background: #F1F5F9; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 20px; }
.error-wrapper { background: #FEF2F2 !important; }
.empty-icon { font-size: 2.5rem; }
.empty-title { font-size: 1.3rem; font-weight: 700; color: #0F172A; margin-bottom: 10px; }
.empty-subtitle { color: #64748B; font-size: 0.95rem; }
.btn-primary-action { background: #0052FF; color: white; padding: 12px 24px; border-radius: 8px; font-weight: 600; border: none; cursor: pointer; margin-top: 20px; transition: all 0.2s; }
.btn-primary-action:hover { background: #0043D1; transform: translateY(-2px); }

/* Aluno Profile */
.aluno-profile-card { display: flex; align-items: center; gap: 20px; padding: 25px 30px; margin-bottom: 25px; position: relative; overflow: hidden; }
.aluno-profile-card::before { content: ''; position: absolute; left: 0; top: 0; height: 100%; width: 4px; background: #0052FF; }
.profile-avatar { width: 60px; height: 60px; background: #EFF6FF; color: #0052FF; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.6rem; font-weight: 800; border: 2px solid #DBEAFE; }
.profile-info { flex: 1; }
.profile-name { font-size: 1.4rem; font-weight: 700; color: #0F172A; margin: 0 0 4px 0; }
.profile-email { color: #64748B; font-size: 0.95rem; margin: 0; }
.profile-status { background: #ECFDF5; border: 1px solid #A7F3D0; color: #059669; padding: 6px 14px; border-radius: 20px; font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }

/* KPIs */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }
.kpi-card { padding: 25px 20px; display: flex; flex-direction: column; align-items: center; text-align: center; justify-content: center; }
.kpi-value { font-size: 2.2rem; font-weight: 800; line-height: 1; margin-bottom: 8px; }
.kpi-label { font-size: 0.75rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }

/* Data Split */
.data-split { display: grid; grid-template-columns: 1.4fr 1fr; gap: 30px; }
.empty-list-card { padding: 30px; text-align: center; color: #94A3B8; font-size: 0.9rem; font-style: italic; }

/* Análise de Disciplinas */
.subject-analysis-card { margin-bottom: 15px; overflow: hidden; }
.subject-header { display: flex; justify-content: space-between; align-items: center; padding: 18px 25px; cursor: pointer; transition: background 0.2s; background: white; }
.subject-header:hover { background: #F8FAFC; }
.subj-meta { display: flex; align-items: center; gap: 12px; }
.subj-badge { background: #0052FF; color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.7rem; font-weight: 700; letter-spacing: 0.5px; }
.subj-name { font-weight: 700; color: #1E293B; font-size: 0.95rem; }
.subj-volume { font-size: 0.8rem; color: #94A3B8; font-weight: 500; }

.subj-stats { display: flex; align-items: center; gap: 15px; }
.progress-bar-thin { width: 80px; height: 6px; background: #E2E8F0; border-radius: 10px; overflow: hidden; }
.progress-fill-thin { height: 100%; border-radius: 10px; }
.subj-score { font-weight: 800; font-size: 1rem; width: 45px; text-align: right; }
.subj-trend { font-size: 0.7rem; font-weight: 700; padding: 3px 8px; border-radius: 4px; }
.trend-up { background: #ECFDF5; color: #059669; }
.trend-down { background: #FEF2F2; color: #DC2626; }
.toggle-icon { color: #94A3B8; font-size: 0.7rem; margin-left: 5px; }

/* Detalhamento (Temas) */
.themes-breakdown { border-top: 1px solid #F1F5F9; background: #F8FAFC; padding: 15px 25px 25px 25px; }
.themes-legend { display: flex; justify-content: flex-end; gap: 30px; font-size: 0.7rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; margin-bottom: 15px; padding-bottom: 10px; border-bottom: 1px solid #E2E8F0; }
.theme-row { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px dashed #E2E8F0; }
.theme-row:last-child { border-bottom: none; padding-bottom: 0; }
.theme-info { display: flex; flex-direction: column; gap: 4px; }
.theme-name { font-size: 0.9rem; font-weight: 600; color: #334155; }
.theme-vol { font-size: 0.75rem; color: #94A3B8; }

.theme-charts { display: flex; flex-direction: column; gap: 8px; width: 220px; }
.chart-line { display: flex; align-items: center; justify-content: space-between; gap: 10px; }
.chart-label { font-size: 0.7rem; font-weight: 700; width: 40px; text-transform: uppercase; }
.chart-bar-bg { flex: 1; height: 6px; background: #E2E8F0; border-radius: 10px; overflow: hidden; }
.chart-bar-fill { height: 100%; border-radius: 10px; }
.chart-value { font-size: 0.8rem; font-weight: 700; width: 35px; text-align: right; }

/* Tabela Histórico */
.table-wrapper { overflow-x: auto; }
.data-table { width: 100%; border-collapse: collapse; }
.data-table thead { background: #F8FAFC; border-bottom: 1px solid #E2E8F0; }
.data-table th { padding: 15px 20px; text-align: left; font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px; }
.data-table tbody tr { border-bottom: 1px solid #F1F5F9; transition: background 0.2s; }
.data-table tbody tr:hover { background: #F8FAFC; }
.data-table td { padding: 15px 20px; font-size: 0.9rem; color: #1E293B; vertical-align: middle; }
.td-title { font-weight: 600; }
.td-center, .th-center { text-align: center !important; }
.td-right, .th-right { text-align: right !important; }
.td-date { color: #64748B; font-size: 0.8rem; }
.score-pill { color: white; font-weight: 700; font-size: 0.8rem; padding: 4px 10px; border-radius: 20px; }

@media (max-width: 1100px) {
  .admin-sidebar { width: 70px; padding: 30px 10px; }
  .logo-text, .tagline, .nav-link span:not(.icon), .btn-logout-clean { display: none; }
  .main-content { margin-left: 70px; padding: 20px; }
  .data-split { grid-template-columns: 1fr; }
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
  .subj-stats { flex-direction: column; align-items: flex-end; gap: 5px; }
  .progress-bar-thin { display: none; }
}
</style>
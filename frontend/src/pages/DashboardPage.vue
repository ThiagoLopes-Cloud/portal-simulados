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
        <router-link to="/dashboard" class="nav-link active">
          <span class="icon">📊</span> Dashboard
        </router-link>
        <router-link to="/simulados" class="nav-link">
          <span class="icon">🎯</span> Avaliações
        </router-link>
        <router-link to="/turmas" class="nav-link">
          <span class="icon">👥</span> Minhas Turmas
        </router-link>
        <router-link to="/ranking" class="nav-link">
          <span class="icon">🏆</span> Ranking
        </router-link>
        
        <template v-if="isAdmin">
          <div class="nav-divider">Comando Admin</div>
          <router-link to="/admin/alunos" class="nav-link link-admin">
            <span class="icon">👥</span> Gestão Alunos
          </router-link>
          <router-link to="/admin/importar" class="nav-link link-admin">
            <span class="icon">📥</span> Importar Bateria
          </router-link>
        </template>
      </nav>

      <div class="sidebar-footer">
        <button @click="logout" class="btn-logout-clean">Sair</button>
      </div>
    </aside>

    <main class="main-content">
      <header class="top-bar">
        <div class="welcome-msg">
          <h2>Olá, {{ username || 'Candidato' }}</h2>
          <p class="text-secondary">Análise tática e evolução constante.</p>
        </div>

        <div class="user-stats-top" v-if="!carregando && dados.gamificacao">
          <div class="stat-item">
            <span class="lvl-tag">NÍVEL {{ nivelAtual }}</span>
            <div class="xp-mini-bar">
              <div class="xp-fill" :style="{ width: progressoNivel + '%' }"></div>
            </div>
          </div>
          <div class="streak-mini">
            🔥 {{ dados.gamificacao?.ofensiva || 0 }} Dias
          </div>
        </div>
      </header>

      <div v-if="erro" class="status-msg erro">{{ erro }}</div>

      <div v-else-if="carregando" class="skeleton-wrapper">
        <div class="skeleton-box shimmer" style="height: 180px; margin-bottom: 30px;"></div>
        <div class="quick-stats">
          <div class="skeleton-card shimmer" v-for="n in 3" :key="n"></div>
        </div>
      </div>

      <div v-else>
        
        <section v-if="isAdmin" class="admin-quick-actions">
          <div class="admin-banner clean-card">
            <div class="banner-info">
              <div class="admin-shield">🛡️</div>
              <div>
                <h3 class="banner-title">Painel de Comando Ativo</h3>
                <p class="banner-desc">Acesso rápido às ferramentas de gestão e conteúdo do laboratório.</p>
              </div>
            </div>
            <div class="banner-buttons">
              <button @click="$router.push('/admin/alunos')" class="btn-outline-admin">
                👥 Base de Alunos
              </button>
              <button @click="$router.push('/admin/importar')" class="btn-primary-admin">
                📥 Importar Questões (IA)
              </button>
            </div>
          </div>
        </section>

        <div v-if="dados.total_simulados === 0 && !isAdmin" class="empty-state-card clean-card">
          <div class="empty-icon-wrapper">
            <span class="empty-icon">🎯</span>
          </div>
          <h3 class="empty-title">Seu diagnóstico tático começa aqui.</h3>
          <p class="empty-subtitle">
            O laboratório de inteligência precisa de dados para calibrar sua estratégia. 
            Realize sua primeira avaliação para destrancar seu painel de performance.
          </p>
          <button @click="$router.push('/simulados')" class="btn-primary-action">
            Iniciar Primeira Simulação
          </button>
        </div>

        <div v-if="dados.total_simulados > 0 || isAdmin" class="dashboard-grid">
          
          <section v-if="recomendacaoPrincipal.titulo" class="recommendation-area">
            <div class="intelligence-card">
              <div class="intel-header">
                <span class="intel-badge">FASE 7: RECOMENDAÇÃO TÁTICA</span>
                <span class="intel-status">Inteligência Ativa</span>
              </div>
              <div class="intel-content">
                <div class="intel-text">
                  <h3>{{ recomendacaoPrincipal.titulo }}</h3>
                  <p>{{ recomendacaoPrincipal.descricao }}</p>
                </div>
                <button @click="$router.push('/simulados')" class="btn-intel-action">
                  Executar Plano de Ação
                </button>
              </div>
            </div>
          </section>

          <section class="quick-stats">
            <div class="stat-card highlight-card">
              <span class="stat-value" :class="corScoreText(dados.score_geral)">{{ dados.score_geral }}%</span>
              <span class="stat-label">Precisão Geral</span>
            </div>
            <div class="stat-card highlight-card">
              <span class="stat-value text-primary">{{ dados.total_simulados }}</span>
              <span class="stat-label">Simulações</span>
            </div>
            <div class="stat-card highlight-card">
              <span class="stat-value text-purple">{{ dados.por_materia.length }}</span>
              <span class="stat-label">Disciplinas</span>
            </div>
          </section>

          <div class="data-split">
            
            <section class="performance-section">
              <h3 class="section-title">Diagnóstico de Performance</h3>
              <div v-for="materia in dados.por_materia" :key="materia.codigo" class="materia-card highlight-card">
                <div class="materia-main">
                  <div class="materia-info">
                    <span class="m-code">{{ materia.codigo }}</span>
                    <span class="m-name">{{ materia.materia }}</span>
                  </div>
                  <div class="materia-stats">
                    <div class="progress-container">
                      <div class="progress-fill" :class="corScoreBg(materia.percentual)" :style="{ width: materia.percentual + '%' }"></div>
                    </div>
                    <span class="m-percent" :class="corScoreText(materia.percentual)">{{ materia.percentual }}%</span>
                  </div>
                </div>
              </div>
            </section>

            <section class="history-section">
              <h3 class="section-title">Atividades Recentes</h3>
              
              <div v-if="dados.historico.length === 0" class="history-card highlight-card empty-history">
                Nenhuma atividade recente encontrada.
              </div>

              <div v-else class="history-card highlight-card">
                <div 
                  v-for="item in historicoComTendencia" 
                  :key="item.resultado_id" 
                  class="history-row clickable-row"
                  @click="$router.push({ name: 'resultado', params: { id: item.resultado_id } })"
                >
                  <div class="h-info">
                    <span class="h-title">{{ item.simulado }}</span>
                    <span class="h-date">{{ item.data }}</span>
                  </div>
                  <div class="h-action-area">
                    <span class="h-percent" :class="corScoreText(item.score)">{{ item.score }}%</span>
                    <span class="action-arrow">→</span>
                  </div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </main>

    <nav class="mobile-bottom-nav">
      <router-link to="/dashboard" class="mnav-item"><span class="mnav-icon">📊</span><span>Dashboard</span></router-link>
      <router-link to="/simulados" class="mnav-item"><span class="mnav-icon">🎯</span><span>Avaliações</span></router-link>
      <router-link to="/turmas" class="mnav-item"><span class="mnav-icon">👥</span><span>Turmas</span></router-link>
      <router-link to="/ranking" class="mnav-item"><span class="mnav-icon">🏆</span><span>Ranking</span></router-link>
      <router-link v-if="isAdmin" to="/admin/alunos" class="mnav-item"><span class="mnav-icon">🛡️</span><span>Admin</span></router-link>
    </nav>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'

const router = useRouter()
const username = ref('')
const carregando = ref(true)
const erro = ref('')
const isAdmin = ref(localStorage.getItem('user_role') === 'admin')

const dados = ref({
  score_geral: 0,
  total_simulados: 0,
  por_materia: [],
  historico: [],
  gamificacao: { xp: 0, ofensiva: 0 }
})

// Lógica de Recomendação Baseada em Dados
const recomendacaoPrincipal = computed(() => {
  if (!dados.value.por_materia || dados.value.por_materia.length === 0) return {}
  const piorMateria = [...dados.value.por_materia].sort((a, b) => a.percentual - b.percentual)[0]
  return {
    titulo: `Foco Estratégico: ${piorMateria.materia}`,
    descricao: `O teu desempenho nesta área está em ${piorMateria.percentual}%. Recomendamos uma bateria de exercícios focada em mapear as tuas lacunas nesta disciplina hoje.`
  }
})

const XP_POR_NIVEL = 500
const nivelAtual = computed(() => Math.floor((dados.value.gamificacao?.xp || 0) / XP_POR_NIVEL) + 1)
const xpProgresso = computed(() => (dados.value.gamificacao?.xp || 0) % XP_POR_NIVEL)
const progressoNivel = computed(() => (xpProgresso.value / XP_POR_NIVEL) * 100)

const historicoComTendencia = computed(() => {
  const mapPorSimulado = {};
  const historicoCronologico = [...dados.value.historico].reverse();
  const historicoEnriquecido = historicoCronologico.map(item => {
    let trend = null;
    if (mapPorSimulado[item.simulado_id] !== undefined) {
      const scoreAnterior = mapPorSimulado[item.simulado_id];
      const diff = parseFloat((item.score - scoreAnterior).toFixed(1));
      if (diff > 0) trend = 'up'; else if (diff < 0) trend = 'down';
    }
    mapPorSimulado[item.simulado_id] = item.score;
    return { ...item, trend };
  });
  return historicoEnriquecido.reverse();
});

onMounted(async () => {
  try {
    const [perfil, dashboard] = await Promise.all([
      api.get('/api/profile/'),
      api.get('/api/resultados/dashboard/'),
    ])
    username.value = perfil.data.username
    dados.value = dashboard.data
  } catch (error) {
    erro.value = 'Erro de conexão.'
  } finally {
    carregando.value = false
  }
})

function corScoreText(v) { return v >= 70 ? 'text-green' : v >= 50 ? 'text-orange' : 'text-red'; }
function corScoreBg(v) { return v >= 70 ? 'bg-green' : v >= 50 ? 'bg-orange' : 'bg-red'; }
function logout() { localStorage.clear(); router.push('/login'); }
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

.dashboard-layout {
  display: flex; min-height: 100vh; width: 100vw; position: absolute;
  top: 0; left: 0; background-color: #F1F5F9; font-family: 'Inter', sans-serif;
}

/* Sidebar */
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

.nav-divider { font-size: 0.65rem; color: #94A3B8; font-weight: 800; text-transform: uppercase; margin: 20px 0 10px 10px; letter-spacing: 0.5px; }
.link-admin { color: #CBD5E1; } .link-admin:hover { color: white; background: rgba(255, 255, 255, 0.1); }

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

/* NOVO: BANNER VIP ADMIN */
.admin-quick-actions { margin-bottom: 35px; }
.admin-banner { background: #0F172A; border: 1px solid #1E293B; border-radius: 16px; padding: 25px 30px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 10px 25px rgba(15, 23, 42, 0.1); }
.banner-info { display: flex; align-items: center; gap: 15px; }
.admin-shield { font-size: 2.5rem; background: rgba(255, 255, 255, 0.1); width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.banner-title { color: white; font-size: 1.3rem; font-weight: 700; margin: 0 0 4px 0; }
.banner-desc { color: #94A3B8; font-size: 0.95rem; margin: 0; }

.banner-buttons { display: flex; gap: 15px; }
.btn-outline-admin { background: transparent; border: 1px solid #334155; color: white; padding: 12px 20px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-outline-admin:hover { background: #1E293B; border-color: #475569; }
.btn-primary-admin { background: #0052FF; color: white; border: none; padding: 12px 20px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.2s; box-shadow: 0 4px 12px rgba(0, 82, 255, 0.2); }
.btn-primary-admin:hover { background: #0043D1; transform: translateY(-2px); }

/* Top Gamificação */
.user-stats-top { display: flex; align-items: center; gap: 15px; }
.lvl-tag { background: #00D09C; color: white; padding: 4px 10px; border-radius: 6px; font-weight: 800; font-size: 0.75rem; }
.xp-mini-bar { width: 80px; height: 6px; background: #E2E8F0; border-radius: 10px; margin-top: 4px; overflow: hidden; }
.xp-fill { height: 100%; background: #0052FF; }
.streak-mini { font-weight: 700; color: #EA580C; background: #FFF7ED; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #FFEDD5; }

/* Bloco Inteligência */
.recommendation-area { margin-bottom: 35px; }
.intelligence-card { background: #FFFFFF; border: 1px solid rgba(0, 82, 255, 0.2); border-radius: 16px; padding: 25px; box-shadow: 0 10px 30px rgba(0, 82, 255, 0.08); position: relative; overflow: hidden; }
.intelligence-card::before { content: ''; position: absolute; top: 0; left: 0; width: 6px; height: 100%; background: #0052FF; }
.intel-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.intel-badge { font-size: 0.65rem; font-weight: 800; letter-spacing: 1px; background: #EFF6FF; color: #0052FF; padding: 4px 10px; border-radius: 4px; }
.intel-status { font-size: 0.75rem; font-weight: 600; color: #10B981; display: flex; align-items: center; gap: 5px; }
.intel-status::before { content: ''; width: 8px; height: 8px; background: #10B981; border-radius: 50%; display: inline-block; }
.intel-content { display: flex; justify-content: space-between; align-items: flex-end; gap: 40px; }
.intel-text h3 { font-size: 1.3rem; font-weight: 700; color: #0F172A; margin-bottom: 8px; }
.intel-text p { color: #475569; font-size: 0.95rem; line-height: 1.5; margin: 0; }
.btn-intel-action { background: #0052FF; color: white; padding: 12px 24px; border-radius: 8px; font-weight: 600; border: none; cursor: pointer; transition: all 0.2s; white-space: nowrap; }
.btn-intel-action:hover { background: #0043D1; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 82, 255, 0.2); }

/* Skeleton */
.skeleton-wrapper { width: 100%; }
.shimmer { position: relative; overflow: hidden; background-color: #E2E8F0; border-radius: 12px; }
.shimmer::after { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent); animation: loading 1.5s infinite; }
@keyframes loading { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

/* Cards Genéricos */
.highlight-card { background: white; border: 1px solid #E2E8F0; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1); }
.quick-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 35px; }
.stat-card { padding: 25px; text-align: center; }
.stat-value { font-size: 2.3rem; font-weight: 800; display: block; line-height: 1; }
.stat-label { color: #64748B; font-size: 0.85rem; font-weight: 600; margin-top: 8px; display: block; }
.data-split { display: grid; grid-template-columns: 1.5fr 1fr; gap: 30px; }
.section-title { font-size: 1.1rem; font-weight: 700; margin-bottom: 15px; color: #1E293B; }

/* Diagnóstico */
.materia-card { margin-bottom: 12px; padding: 16px 20px; }
.materia-main { display: flex; justify-content: space-between; align-items: center; }
.m-code { background: #F8FAFC; color: #64748B; padding: 3px 7px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; border: 1px solid #E2E8F0; }
.m-name { font-weight: 600; color: #1E293B; margin-left: 10px; font-size: 0.95rem; }
.progress-container { width: 120px; height: 8px; background: #F1F5F9; border-radius: 10px; overflow: hidden; margin-right: 15px; }
.progress-fill { height: 100%; border-radius: 10px; }

/* Histórico Clicável */
.history-card { padding: 5px 0; }
.empty-history { padding: 30px; text-align: center; color: #94A3B8; font-size: 0.9rem; }
.history-row { display: flex; justify-content: space-between; padding: 14px 20px; border-bottom: 1px solid #F1F5F9; }
.h-title { font-weight: 600; font-size: 0.9rem; color: #1E293B; }
.h-date { font-size: 0.75rem; color: #94A3B8; margin-top: 2px; display: block; }
.h-percent { font-weight: 700; font-size: 0.95rem; }

/* Animações Mágicas do Histórico */
.clickable-row { cursor: pointer; transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); border-radius: 8px; margin: 4px 8px; border-bottom: none; }
.clickable-row:hover { background-color: #EFF6FF; transform: translateX(6px); box-shadow: 0 2px 8px rgba(0, 82, 255, 0.05); }
.h-action-area { display: flex; align-items: center; gap: 15px; }
.action-arrow { color: #0052FF; font-weight: 800; font-size: 1.1rem; opacity: 0; transform: translateX(-10px); transition: all 0.3s ease; }
.clickable-row:hover .action-arrow { opacity: 1; transform: translateX(0); }

/* Cores Premium */
.text-green { color: #10B981; } .text-orange { color: #F59E0B; } .text-red { color: #EF4444; }
.text-primary { color: #0052FF; } .text-purple { color: #7C3AED; }
.bg-green { background-color: #10B981; } .bg-orange { background-color: #F59E0B; } .bg-red { background-color: #EF4444; }

/* Empty State Base */
.empty-state-card { padding: 60px 40px; text-align: center; border-radius: 16px; background: white; border: 1px dashed #CBD5E1; box-shadow: 0 10px 25px rgba(0,0,0,0.02); display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 20px; }
.empty-icon-wrapper { width: 80px; height: 80px; background: #EFF6FF; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 24px; }
.empty-icon { font-size: 2.5rem; }
.empty-title { font-size: 1.4rem; font-weight: 700; color: #0F172A; margin-bottom: 12px; }
.empty-subtitle { color: #64748B; line-height: 1.6; max-width: 500px; margin-bottom: 30px; font-size: 0.95rem; }
.btn-primary-action { background: #0052FF; color: white; padding: 14px 28px; border-radius: 8px; font-weight: 600; border: none; cursor: pointer; transition: all 0.2s; box-shadow: 0 4px 12px rgba(0, 82, 255, 0.2); }
.btn-primary-action:hover { background: #0043D1; transform: translateY(-2px); }

@media (max-width: 1000px) {
  .sidebar { width: 70px; padding: 30px 10px; }
  .logo-text, .tagline, .nav-link span:not(.icon), .btn-logout-clean { display: none; }
  .main-content { margin-left: 70px; }
  .intel-content { flex-direction: column; align-items: flex-start; gap: 20px; }
  .data-split { grid-template-columns: 1fr; }
  .admin-banner { flex-direction: column; text-align: center; gap: 20px; }
  .banner-info { flex-direction: column; }
}

/* Mobile Bottom Navigation */
.mobile-bottom-nav { display: none; position: fixed; bottom: 0; left: 0; right: 0; background: white; border-top: 1px solid #E2E8F0; z-index: 200; box-shadow: 0 -4px 12px rgba(0,0,0,0.06); padding-bottom: env(safe-area-inset-bottom, 0); }
.mnav-item { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 3px; padding: 10px 4px; color: #64748B; text-decoration: none; font-size: 0.6rem; font-weight: 600; background: none; border: none; cursor: pointer; font-family: inherit; transition: color 0.2s; }
.mnav-icon { font-size: 1.2rem; line-height: 1; }
.mnav-item.router-link-active { color: #0052FF; }

@media (max-width: 768px) {
  .mobile-bottom-nav { display: flex; }
  .sidebar { display: none !important; }
  .main-content { margin-left: 0 !important; padding: 20px 16px 84px !important; }
  .top-bar { flex-wrap: wrap; gap: 10px; }
  .user-stats-top { flex-wrap: wrap; gap: 10px; }
  .welcome-msg h2 { font-size: 1.4rem; }
  .intel-content { flex-direction: column; align-items: flex-start; gap: 15px; }
  .btn-intel-action { width: 100%; text-align: center; }
  .admin-banner { padding: 20px; }
  .banner-buttons { flex-direction: column; width: 100%; gap: 10px; }
  .btn-outline-admin, .btn-primary-admin { width: 100%; text-align: center; }
}

@media (max-width: 480px) {
  .quick-stats { gap: 10px; }
  .stat-card { padding: 15px 8px; }
  .stat-value { font-size: 1.7rem; }
  .materia-main { flex-direction: column; align-items: flex-start; gap: 8px; }
  .materia-stats { width: 100%; }
  .progress-container { flex: 1; width: auto; max-width: none; margin-right: 10px; }
}
</style>
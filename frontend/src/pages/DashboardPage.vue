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
        <router-link to="/ranking" class="nav-link">
          <span class="icon">🏆</span> Ranking
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
        <div class="quick-stats">
          <div class="skeleton-card shimmer" v-for="n in 3" :key="n"></div>
        </div>
        <div class="data-split">
          <div class="skeleton-box shimmer" style="height: 400px;"></div>
          <div class="skeleton-box shimmer" style="height: 400px;"></div>
        </div>
      </div>

      <div v-else-if="dados.total_simulados === 0" class="empty-state-card clean-card">
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

      <div v-else class="dashboard-grid">
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
            <div class="history-card highlight-card">
              <div v-for="item in historicoComTendencia" :key="item.resultado_id" class="history-row">
                <div class="h-info">
                  <span class="h-title">{{ item.simulado }}</span>
                  <span class="h-date">{{ item.data }}</span>
                </div>
                <div class="h-result">
                  <span class="h-percent" :class="corScoreText(item.score)">{{ item.score }}%</span>
                </div>
              </div>
            </div>
          </section>
        </div>
      </div>
    </main>
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
const materiasAbertas = ref([])
const isAdmin = ref(localStorage.getItem('user_role') === 'admin')

const dados = ref({
  score_geral: 0,
  total_simulados: 0,
  por_materia: [],
  historico: [],
  gamificacao: { xp: 0, ofensiva: 0 }
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
.nav-link:hover, .nav-link.router-link-active { background: rgba(255, 255, 255, 0.15); color: white; }

/* Top Bar & Content */
.main-content { flex: 1; margin-left: 220px; padding: 40px 50px; }
.top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 35px; }
.welcome-msg h2 { font-size: 1.7rem; font-weight: 700; color: #0F172A; margin: 0; }
.text-secondary { color: #475569; font-size: 0.9rem; margin-top: 4px; }

.user-stats-top { display: flex; align-items: center; gap: 15px; }
.lvl-tag { background: #00D09C; color: white; padding: 4px 10px; border-radius: 6px; font-weight: 800; font-size: 0.75rem; }
.xp-mini-bar { width: 80px; height: 6px; background: #E2E8F0; border-radius: 10px; margin-top: 4px; overflow: hidden; }
.xp-fill { height: 100%; background: #0052FF; }
.streak-mini { font-weight: 700; color: #EA580C; background: #FFF7ED; padding: 5px 12px; border-radius: 20px; font-size: 0.8rem; border: 1px solid #FFEDD5; }

/* --- NOVO: SKELETON LOADERS --- */
.skeleton-wrapper { width: 100%; }
.skeleton-card { height: 115px; background: #E2E8F0; border-radius: 12px; }
.skeleton-box { background: #E2E8F0; border-radius: 12px; width: 100%; }

.shimmer {
  position: relative; overflow: hidden; background-color: #E2E8F0;
}
.shimmer::after {
  content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent);
  animation: loading 1.5s infinite;
}
@keyframes loading {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

/* --- NOVO: EMPTY STATE PREMIUM --- */
.empty-state-card {
  padding: 60px 40px; text-align: center; border-radius: 16px;
  background: white; border: 1px dashed #CBD5E1; box-shadow: 0 10px 25px rgba(0,0,0,0.02);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  margin-top: 20px;
}
.empty-icon-wrapper {
  width: 80px; height: 80px; background: #EFF6FF; border-radius: 50%;
  display: flex; align-items: center; justify-content: center; margin-bottom: 24px;
}
.empty-icon { font-size: 2.5rem; }
.empty-title { font-size: 1.4rem; font-weight: 700; color: #0F172A; margin-bottom: 12px; }
.empty-subtitle { color: #64748B; line-height: 1.6; max-width: 500px; margin-bottom: 30px; font-size: 0.95rem; }
.btn-primary-action {
  background: #0052FF; color: white; padding: 14px 28px; border-radius: 8px;
  font-weight: 600; border: none; cursor: pointer; transition: all 0.2s; box-shadow: 0 4px 12px rgba(0, 82, 255, 0.2);
}
.btn-primary-action:hover { background: #0043D1; transform: translateY(-2px); }

/* Grid e Cards Padrão */
.highlight-card {
  background: white; border: 1px solid #E2E8F0; border-radius: 12px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.quick-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 35px; }
.stat-card { padding: 25px; text-align: center; }
.stat-value { font-size: 2.3rem; font-weight: 800; display: block; line-height: 1; }
.stat-label { color: #64748B; font-size: 0.85rem; font-weight: 600; margin-top: 8px; display: block; }

.data-split { display: grid; grid-template-columns: 1.5fr 1fr; gap: 30px; }
.section-title { font-size: 1.1rem; font-weight: 700; margin-bottom: 15px; color: #1E293B; }

.materia-card { margin-bottom: 12px; padding: 16px 20px; }
.materia-main { display: flex; justify-content: space-between; align-items: center; }
.m-code { background: #F8FAFC; color: #64748B; padding: 3px 7px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; border: 1px solid #E2E8F0; }
.m-name { font-weight: 600; color: #1E293B; margin-left: 10px; font-size: 0.95rem; }
.progress-container { width: 120px; height: 8px; background: #F1F5F9; border-radius: 10px; overflow: hidden; margin-right: 15px; }
.progress-fill { height: 100%; border-radius: 10px; }

.history-card { padding: 5px 0; }
.history-row { display: flex; justify-content: space-between; padding: 14px 20px; border-bottom: 1px solid #F1F5F9; }
.h-title { font-weight: 600; font-size: 0.9rem; color: #1E293B; }
.h-date { font-size: 0.75rem; color: #94A3B8; margin-top: 2px; display: block; }
.h-percent { font-weight: 700; font-size: 0.95rem; }

.text-green { color: #10B981; } .text-orange { color: #F59E0B; } .text-red { color: #EF4444; }
.text-primary { color: #0052FF; } .text-purple { color: #7C3AED; }
.bg-green { background-color: #10B981; } .bg-orange { background-color: #F59E0B; } .bg-red { background-color: #EF4444; }

.btn-logout-clean {
  background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2);
  color: white; width: 100%; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.85rem;
}
.btn-logout-clean:hover { background: #EF4444; border-color: #EF4444; }

@media (max-width: 1000px) {
  .sidebar { width: 70px; padding: 30px 10px; }
  .logo-text, .tagline, .nav-link span:not(.icon), .btn-logout-clean { display: none; }
  .main-content { margin-left: 70px; }
}
</style>
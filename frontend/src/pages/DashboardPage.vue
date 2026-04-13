<template>
  <div class="dashboard-layout">
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1 class="logo-text">
          <span class="logo-white">SIMUS</span><span class="logo-accent">LAB</span>
        </h1>
        <p class="tagline">Painel de Performance</p>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-link">
          <span class="icon">📊</span> Dashboard
        </router-link>
        <router-link to="/simulados" class="nav-link">
          <span class="icon">🎯</span> Avaliações
        </router-link>
        <router-link to="/ranking" class="nav-link">
          <span class="icon">🏆</span> Ranking Geral
        </router-link>
        <router-link v-if="isAdmin" to="/admin/alunos" class="nav-link link-admin">
          <span class="icon">🛡️</span> Comando Admin
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <button @click="logout" class="btn-logout-clean">Sair do Sistema</button>
      </div>
    </aside>

    <main class="main-content">
      <header class="top-bar">
        <div class="welcome-msg">
          <h2>Olá, {{ username }}</h2>
          <p class="text-dim">Mantenha a constância. Seus dados mostram sua evolução.</p>
        </div>

        <div class="user-stats-top" v-if="dados.gamificacao">
          <div class="stat-item">
            <span class="lvl-tag">LVL {{ nivelAtual }}</span>
            <div class="xp-mini-bar">
              <div class="xp-fill" :style="{ width: progressoNivel + '%' }"></div>
            </div>
          </div>
          <div class="streak-mini">
            🔥 {{ dados.gamificacao?.ofensiva || 0 }} Dias
          </div>
        </div>
      </header>

      <div v-if="carregando" class="status-msg">Sincronizando laboratório...</div>
      <div v-else-if="erro" class="status-msg erro">{{ erro }}</div>

      <div v-else class="dashboard-grid">
        <section class="quick-stats">
          <div class="stat-card clean-card">
            <span class="stat-value" :class="corScoreText(dados.score_geral)">{{ dados.score_geral }}%</span>
            <span class="stat-label">Precisão Geral</span>
          </div>
          <div class="stat-card clean-card">
            <span class="stat-value color-blue">{{ dados.total_simulados }}</span>
            <span class="stat-label">Simulações</span>
          </div>
          <div class="stat-card clean-card">
            <span class="stat-value color-purple">{{ dados.por_materia.length }}</span>
            <span class="stat-label">Disciplinas</span>
          </div>
        </section>

        <div class="data-split">
          <section class="performance-section">
            <h3 class="section-title">Diagnóstico de Disciplinas</h3>
            <div v-for="materia in dados.por_materia" :key="materia.codigo" class="materia-card clean-card">
              <div class="materia-main" @click="toggleMateria(materia.codigo)">
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
            <div class="history-card clean-card">
              <div v-for="item in historicoComTendencia" :key="item.resultado_id" class="history-row">
                <div class="h-info">
                  <span class="h-title">{{ item.simulado }}</span>
                  <span class="h-date">{{ item.data }}</span>
                </div>
                <div class="h-result">
                  <span :class="corScoreText(item.score)">{{ item.score }}%</span>
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
    erro.value = 'Erro de conexão com o laboratório.'
  } finally {
    carregando.value = false
  }
})

function corScoreText(v) { return v >= 70 ? 'color-green' : v >= 50 ? 'color-orange' : 'color-red'; }
function corScoreBg(v) { return v >= 70 ? 'bg-green' : v >= 50 ? 'bg-orange' : 'bg-red'; }
function logout() { localStorage.clear(); router.push('/login'); }
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.dashboard-layout {
  display: flex;
  min-height: 100vh;
  width: 100vw;
  position: absolute;
  top: 0; left: 0;
  background-color: #F8FAFC;
  font-family: 'Inter', sans-serif;
}

/* --- SIDEBAR AZUL (DNA DO LOGIN) --- */
.sidebar {
  width: 280px;
  background: linear-gradient(180deg, #0A2540 0%, #0052FF 100%);
  color: white;
  display: flex;
  flex-direction: column;
  padding: 40px 24px;
  position: fixed;
  height: 100vh;
}

.logo-white { color: #FFFFFF; font-weight: 700; font-size: 1.5rem; }
.logo-accent { color: #00D09C; font-weight: 700; font-size: 1.5rem; }
.tagline { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1.5px; opacity: 0.7; margin-top: 4px; }

.sidebar-nav { margin-top: 60px; flex: 1; }
.nav-link {
  display: flex; align-items: center; gap: 12px;
  color: rgba(255, 255, 255, 0.7);
  text-decoration: none;
  padding: 14px 18px;
  border-radius: 8px;
  margin-bottom: 8px;
  font-weight: 500;
  transition: all 0.2s;
}
.nav-link:hover, .nav-link.router-link-active {
  background: rgba(255, 255, 255, 0.1);
  color: white;
}

/* --- CONTEÚDO BRANCO --- */
.main-content {
  flex: 1;
  margin-left: 280px;
  padding: 40px 60px;
}

.top-bar {
  display: flex; justify-content: space-between; align-items: center;
  margin-bottom: 40px;
}
.welcome-msg h2 { font-size: 1.8rem; font-weight: 700; color: #0A2540; }
.text-dim { color: #64748B; font-size: 0.95rem; }

.user-stats-top { display: flex; align-items: center; gap: 20px; }
.lvl-tag { background: #00D09C; color: white; padding: 4px 10px; border-radius: 6px; font-weight: 700; font-size: 0.8rem; }
.xp-mini-bar { width: 100px; height: 6px; background: #E2E8F0; border-radius: 10px; margin-top: 4px; overflow: hidden; }
.xp-fill { height: 100%; background: #0052FF; }
.streak-mini { font-weight: 600; color: #EA580C; background: #FFF7ED; padding: 6px 12px; border-radius: 20px; font-size: 0.85rem; }

/* Cards Clean */
.clean-card {
  background: white;
  border: 1px solid rgba(0,0,0,0.05);
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.03);
}

.quick-stats { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-bottom: 40px; }
.stat-card { padding: 30px; text-align: center; }
.stat-value { font-size: 2.2rem; font-weight: 700; display: block; }
.stat-label { color: #64748B; font-size: 0.85rem; font-weight: 500; margin-top: 4px; }

.data-split { display: grid; grid-template-columns: 1.5fr 1fr; gap: 32px; }
.section-title { font-size: 1.1rem; font-weight: 700; margin-bottom: 20px; }

.materia-card { margin-bottom: 12px; padding: 18px 24px; }
.materia-main { display: flex; justify-content: space-between; align-items: center; }
.m-code { background: #F1F5F9; padding: 4px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.m-name { font-weight: 600; margin-left: 12px; }
.progress-container { width: 100px; height: 6px; background: #F1F5F9; border-radius: 10px; overflow: hidden; }
.progress-fill { height: 100%; }

.history-card { padding: 10px 0; }
.history-row { display: flex; justify-content: space-between; padding: 16px 24px; border-bottom: 1px solid #F1F5F9; }
.h-title { font-weight: 600; font-size: 0.9rem; display: block; }
.h-date { font-size: 0.75rem; color: #94A3B8; }

/* Cores */
.color-blue { color: #0052FF; }
.color-purple { color: #7C3AED; }
.color-green { color: #00D09C; }
.color-orange { color: #F59E0B; }
.color-red { color: #EF4444; }
.bg-green { background: #00D09C; }
.bg-orange { background: #F59E0B; }
.bg-red { background: #EF4444; }

.btn-logout-clean {
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  color: white;
  width: 100%;
  padding: 12px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}
.btn-logout-clean:hover { background: #EF4444; border-color: #EF4444; }

@media (max-width: 1100px) {
  .sidebar { width: 80px; padding: 40px 10px; }
  .logo-text, .tagline, .nav-link span:not(.icon), .btn-logout-clean { display: none; }
  .main-content { margin-left: 80px; }
}
</style>
<template>
  <div class="dashboard-wrapper">
    <div class="main-fundo"></div>

    <nav class="navbar clean-card">
      <div class="logo-area">
        <h1 class="logo-text">
          <span class="color-primary">SIMUS</span><span class="color-dark">LAB</span>
        </h1>
        <p class="tagline text-dim">Painel de Performance</p>
      </div>

      <div class="nav-links">
        <router-link to="/simulados" class="nav-item">Avaliações</router-link>
        <router-link to="/ranking" class="nav-item">Ranking Geral</router-link>
        <router-link v-if="isAdmin" to="/admin/alunos" class="nav-item link-admin">
          Painel de Comando
        </router-link>
      </div>

      <div class="user-stats">
        <div class="xp-container" v-if="dados.gamificacao">
          <div class="level-badge">NÍVEL {{ nivelAtual }}</div>
          <div class="xp-bar-bg">
            <div class="xp-bar-fill" :style="{ width: progressoNivel + '%' }"></div>
          </div>
          <span class="xp-text">{{ xpProgresso }} / 500 XP</span>
        </div>

        <div class="streak-badge" :class="{ 'fogo-ativo': dados.gamificacao?.ofensiva > 0 }">
          <span class="fire-icon">{{ dados.gamificacao?.ofensiva > 0 ? '🔥' : '🧊' }}</span>
          <span class="streak-count">{{ dados.gamificacao?.ofensiva || 0 }} Dias</span>
        </div>
        
        <button @click="logout" class="btn-logout">Sair</button>
      </div>
    </nav>

    <div v-if="carregando" class="status-msg loading">Sincronizando dados de performance...</div>
    <div v-else-if="erro" class="status-msg erro">{{ erro }}</div>

    <main v-else class="main-content">
      <header class="welcome-header">
        <h2>Olá, {{ username }}</h2>
        <p class="text-dim">"A constância é o que separa o sonho da aprovação. Analise seus dados e otimize sua estratégia."</p>
      </header>

      <section class="stats-grid">
        <div class="resumo-card clean-card">
          <span class="resumo-valor" :class="corScoreText(dados.score_geral)">{{ dados.score_geral }}%</span>
          <span class="resumo-label">Score Geral de Precisão</span>
        </div>
        <div class="resumo-card clean-card">
          <span class="resumo-valor color-primary">{{ dados.total_simulados }}</span>
          <span class="resumo-label">Simulações Concluídas</span>
        </div>
        <div class="resumo-card clean-card">
          <span class="resumo-valor color-secondary">{{ dados.por_materia.length }}</span>
          <span class="resumo-label">Áreas de Conhecimento</span>
        </div>
        <div class="resumo-card acao-card clean-card" @click="$router.push('/simulados')">
          <span class="action-icon">🎯</span>
          <span class="resumo-label-bold">Iniciar Nova Simulação</span>
        </div>
      </section>

      <div class="content-split">
        <section class="secao-materias">
          <h3 class="section-title">Diagnóstico por Disciplina</h3>

          <div v-if="dados.por_materia.length === 0" class="vazio clean-card">
            <p>Aguardando dados iniciais. Realize sua primeira simulação para gerar o diagnóstico.</p>
          </div>

          <div v-for="materia in dados.por_materia" :key="materia.codigo" class="materia-item clean-card">
            <div class="materia-header" @click="toggleMateria(materia.codigo)">
              <div class="materia-info">
                <span class="materia-badge">{{ materia.codigo }}</span>
                <span class="materia-nome">{{ materia.materia }}</span>
              </div>
              <div class="materia-direita">
                <span class="materia-detalhe text-dim">{{ materia.acertos }}/{{ materia.total_questoes }}</span>
                <div class="barra-progresso">
                  <div class="barra-fill" :class="corScoreBg(materia.percentual)" :style="{ width: materia.percentual + '%' }"></div>
                </div>
                <span class="materia-percentual" :class="corScoreText(materia.percentual)">{{ materia.percentual }}%</span>
                <span class="tendencia" :class="materia.diferenca_media >= 0 ? 'positivo' : 'negativo'">
                  {{ materia.diferenca_media >= 0 ? '+' : '' }}{{ materia.diferenca_media }}%
                </span>
              </div>
            </div>

            <div v-if="materiasAbertas.includes(materia.codigo)" class="temas-container">
              <div v-for="tema in materia.temas" :key="tema.tema" class="tema-row">
                <div class="tema-info">
                  <span class="tema-nome">{{ tema.tema }}</span>
                  <span class="tema-sub text-dim">{{ tema.acertos }}/{{ tema.total }} acertos</span>
                </div>
                <div class="tema-stats">
                  <div class="barra-dupla">
                    <span class="label-mini">Pessoal</span>
                    <div class="barra-mini">
                      <div class="barra-fill" :class="corScoreBg(tema.percentual)" :style="{ width: tema.percentual + '%' }"></div>
                    </div>
                    <span class="percent-mini" :class="corScoreText(tema.percentual)">{{ tema.percentual }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section class="secao-historico">
          <h3 class="section-title">Histórico de Atividades</h3>
          
          <div v-if="dados.historico.length === 0" class="vazio clean-card">Nenhum registro encontrado.</div>
          
          <div class="historico-lista clean-card" v-else>
            <div v-for="item in historicoComTendencia" :key="item.resultado_id" class="hist-row">
              <div class="hist-meta">
                <span class="hist-titulo">{{ item.simulado }}</span>
                <span class="hist-data">{{ item.data }}</span>
              </div>
              <div class="hist-result">
                <span class="hist-percent" :class="corScoreText(item.score)">{{ item.score }}%</span>
                <span class="hist-icon" :class="item.trend === 'up' ? 'positivo' : (item.trend === 'down' ? 'negativo' : '')">
                  {{ item.trend === 'up' ? '▲' : (item.trend === 'down' ? '▼' : '—') }}
                </span>
              </div>
            </div>
          </div>
        </section>
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
    let trend = null; let diff = 0;
    if (mapPorSimulado[item.simulado_id] !== undefined) {
      const scoreAnterior = mapPorSimulado[item.simulado_id];
      diff = parseFloat((item.score - scoreAnterior).toFixed(1));
      if (diff > 0) trend = 'up'; else if (diff < 0) trend = 'down'; else trend = 'same';
    }
    mapPorSimulado[item.simulado_id] = item.score;
    return { ...item, trend, diff };
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
    if (dados.value.por_materia.length > 0) {
      materiasAbertas.value = [dados.value.por_materia[0].codigo]
    }
  } catch (error) {
    erro.value = 'Falha na sincronização com o laboratório.'
    console.error(error)
  } finally {
    carregando.value = false
  }
})

function toggleMateria(codigo) {
  const index = materiasAbertas.value.indexOf(codigo)
  if (index === -1) materiasAbertas.value.push(codigo)
  else materiasAbertas.value.splice(index, 1)
}

function corScoreText(valor) {
  if (valor >= 70) return 'color-success'
  if (valor >= 50) return 'color-warning'
  return 'color-error'
}

function corScoreBg(valor) {
  if (valor >= 70) return 'bg-success'
  if (valor >= 50) return 'bg-warning'
  return 'bg-error'
}

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_role')
  router.push({ name: 'login' })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.dashboard-wrapper {
  position: relative;
  min-height: 100vh;
  background-color: #F8F9FA;
  font-family: 'Inter', sans-serif;
  color: #0A2540;
  padding: 0 0 40px 0;
}

.main-fundo {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  background: linear-gradient(135deg, #FFFFFF 0%, #F1F4F8 100%);
  z-index: 0;
}

.main-content {
  position: relative;
  z-index: 5;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Navbar */
.navbar {
  position: relative;
  z-index: 10;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 40px;
  background: #FFFFFF;
  margin-bottom: 40px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.03);
  border-radius: 0 0 16px 16px;
  width: 100vw;
  left: 50%;
  transform: translateX(-50%);
}

.logo-text { font-size: 1.4rem; font-weight: 700; margin: 0; }
.tagline { font-size: 0.7rem; letter-spacing: 1px; text-transform: uppercase; margin-top: -4px; }

.nav-links { display: flex; gap: 25px; }
.nav-item { 
  text-decoration: none; color: #6B7280; font-size: 0.9rem; font-weight: 500; 
  transition: color 0.2s;
}
.nav-item:hover, .nav-item.router-link-active { color: #0052FF; }

/* Cards & Stats */
.clean-card {
  background: #FFFFFF;
  border: 1px solid rgba(0,0,0,0.05);
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.04);
}

.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; }
.resumo-card { padding: 30px 20px; text-align: center; }
.resumo-valor { font-size: 2.2rem; font-weight: 700; display: block; }
.resumo-label { font-size: 0.8rem; color: #6B7280; font-weight: 500; margin-top: 5px; }
.resumo-label-bold { font-size: 0.85rem; font-weight: 600; color: #0052FF; }

.acao-card { 
  cursor: pointer; background: #F0F5FF; border: 1px solid rgba(0,82,255,0.1); 
  transition: all 0.2s;
}
.acao-card:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,82,255,0.1); }

/* Gamificação Clean */
.user-stats { display: flex; align-items: center; gap: 25px; }
.level-badge { background: #00D09C; color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; }
.xp-bar-bg { width: 120px; height: 8px; background: #E5E7EB; border-radius: 10px; overflow: hidden; }
.xp-bar-fill { height: 100%; background: #0052FF; transition: width 1s; }
.xp-text { font-size: 0.75rem; color: #6B7280; font-weight: 500; }

.streak-badge { 
  display: flex; align-items: center; gap: 6px; padding: 6px 14px; 
  background: #F9FAFB; border: 1px solid #E5E7EB; border-radius: 20px;
}
.streak-badge.fogo-ativo { background: #FFF7ED; border-color: #FED7AA; color: #EA580C; }
.streak-count { font-size: 0.85rem; font-weight: 600; }

/* Materias & Histórico */
.content-split { display: grid; grid-template-columns: 1.6fr 1fr; gap: 30px; }
.section-title { font-size: 1.1rem; font-weight: 700; margin-bottom: 20px; color: #0A2540; }

.materia-item { margin-bottom: 12px; }
.materia-header { display: flex; justify-content: space-between; align-items: center; padding: 20px; cursor: pointer; }
.materia-badge { background: #F3F4F6; color: #374151; padding: 4px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.materia-nome { font-weight: 600; margin-left: 10px; }

.barra-progresso { width: 80px; height: 6px; background: #F3F4F6; border-radius: 10px; overflow: hidden; }
.barra-fill { height: 100%; border-radius: 10px; }

/* Cores de Performance */
.bg-success { background: #00D09C; }
.bg-warning { background: #F5A623; }
.bg-error { background: #EF4444; }
.color-success { color: #00D09C; }
.color-warning { color: #D97706; }
.color-error { color: #EF4444; }
.color-primary { color: #0052FF; }
.color-secondary { color: #7C3AED; }

.hist-row { 
  display: flex; justify-content: space-between; padding: 15px 20px; 
  border-bottom: 1px solid #F3F4F6;
}
.hist-row:last-child { border-bottom: none; }
.hist-titulo { font-size: 0.9rem; font-weight: 600; display: block; }
.hist-data { font-size: 0.75rem; color: #9CA3AF; }
.hist-percent { font-weight: 700; font-size: 1rem; }

.btn-logout { 
  background: none; border: 1px solid #E5E7EB; color: #6B7280; 
  padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 0.8rem;
  transition: all 0.2s;
}
.btn-logout:hover { border-color: #EF4444; color: #EF4444; }

@media (max-width: 1024px) {
  .content-split { grid-template-columns: 1fr; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .user-stats { display: none; }
}
</style>

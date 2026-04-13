<template>
  <div class="dashboard-wrapper">
    <nav class="navbar glass-card">
      <div class="logo">
        <h1 class="ui-display logo-text"><span class="color-primary">SIMUS</span><span class="color-secondary">LAB</span></h1>
      </div>

      <div class="nav-links">
        <router-link to="/simulados" class="nav-item ui-display">Batalhas (Simulados)</router-link>
        <router-link to="/ranking" class="nav-item ui-display">Hall da Fama</router-link>
        <router-link v-if="isAdmin" to="/admin/alunos" class="nav-item ui-display link-admin">
          Comando (Admin)
        </router-link>
      </div>

      <div class="user-stats">
        <div class="xp-container" v-if="dados.gamificacao">
          <div class="level-badge ui-display">LVL {{ nivelAtual }}</div>
          <div class="xp-bar-bg">
            <div class="xp-bar-fill" :style="{ width: progressoNivel + '%' }"></div>
          </div>
          <span class="xp-text ui-display">{{ xpProgresso }} / 500 XP</span>
        </div>

        <div class="streak-badge" :class="{ 'fogo-ativo': dados.gamificacao?.ofensiva > 0 }" title="Dias seguidos de estudo">
          <span class="fire-icon">{{ dados.gamificacao?.ofensiva > 0 ? '🔥' : '🧊' }}</span>
          <span class="streak-count ui-display">{{ dados.gamificacao?.ofensiva || 0 }} D</span>
        </div>
        
        <button @click="logout" class="btn-logout ui-display">Sair</button>
      </div>
    </nav>

    <div v-if="carregando" class="loading ui-display color-primary">Inicializando Sistemas do Laboratório...</div>
    <div v-else-if="erro" class="erro ui-display color-error">{{ erro }}</div>

    <main v-else class="main-content">
      <header class="welcome-header">
        <h2 class="ui-display">Painel Tático, {{ username }}!</h2>
        <p class="text-dim">Treinador: "Foco total, recruta. Os dados abaixo revelam o quão perto você está da aprovação."</p>
      </header>

      <section class="stats-grid">
        <div class="card-resumo glass-card">
          <span class="resumo-valor ui-display" :class="corScoreText(dados.score_geral)">{{ dados.score_geral }}%</span>
          <span class="resumo-label ui-display">Score Geral Tático</span>
        </div>
        <div class="card-resumo glass-card">
          <span class="resumo-valor ui-display color-primary">{{ dados.total_simulados }}</span>
          <span class="resumo-label ui-display">Batalhas Vencidas</span>
        </div>
        <div class="card-resumo glass-card">
          <span class="resumo-valor ui-display color-secondary">{{ dados.por_materia.length }}</span>
          <span class="resumo-label ui-display">Matérias Mapeadas</span>
        </div>
        <div class="card-resumo acao glass-card" @click="$router.push('/simulados')">
          <span class="resumo-valor action-icon">🎯</span>
          <span class="resumo-label ui-display">Iniciar Nova Missão</span>
        </div>
      </section>

      <div class="content-split">
        <section class="secao-materias">
          <h3 class="section-title ui-display"><span class="color-primary">></span> Diagnóstico de Performance</h3>

          <div v-if="dados.por_materia.length === 0" class="vazio glass-card">
            <p>Aguardando dados de combate. Inicie um simulado para gerar seu diagnóstico.</p>
          </div>

          <div v-for="materia in dados.por_materia" :key="materia.codigo" class="card-materia glass-card">
            <div class="materia-header" @click="toggleMateria(materia.codigo)">
              <div class="materia-info">
                <span class="materia-badge ui-display">{{ materia.codigo }}</span>
                <span class="materia-nome">{{ materia.materia }}</span>
              </div>
              <div class="materia-direita">
                <span class="materia-detalhe ui-display text-dim">{{ materia.acertos }}/{{ materia.total_questoes }}</span>
                <div class="barra-mini">
                  <div class="barra-fill" :class="corScoreBg(materia.percentual)" :style="{ width: materia.percentual + '%' }"></div>
                </div>
                <span class="materia-percentual ui-display" :class="corScoreText(materia.percentual)">{{ materia.percentual }}%</span>
                <span class="diferenca ui-display" :class="materia.diferenca_media >= 0 ? 'positivo' : 'negativo'">
                  {{ materia.diferenca_media >= 0 ? '+' : '' }}{{ materia.diferenca_media }}%
                  <span v-if="materia.diferenca_media >= 0" class="trend">▲</span>
                  <span v-else class="trend">▼</span>
                </span>
              </div>
            </div>

            <div v-if="materiasAbertas.includes(materia.codigo)" class="temas-lista">
              <div class="temas-legenda text-dim ui-display">
                <span>Seu Radar</span>
                <span>Média Global</span>
              </div>
              <div v-for="tema in materia.temas" :key="tema.tema" class="tema-item">
                <div class="tema-info">
                  <span class="tema-nome">{{ tema.tema }}</span>
                  <span class="tema-detalhe text-dim">{{ tema.acertos }}/{{ tema.total }} acertos</span>
                </div>
                <div class="tema-direita">
                  <div class="barra-dupla">
                    <div class="barra-mini pequena">
                      <div class="barra-fill" :class="corScoreBg(tema.percentual)" :style="{ width: tema.percentual + '%' }"></div>
                    </div>
                    <span class="tema-percentual ui-display" :class="corScoreText(tema.percentual)">{{ tema.percentual }}%</span>
                  </div>
                  <div class="barra-dupla opacity-50">
                    <div class="barra-mini pequena">
                      <div class="barra-fill bg-dim" :style="{ width: tema.media_plataforma + '%' }"></div>
                    </div>
                    <span class="tema-percentual ui-display text-dim">{{ tema.media_plataforma }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section class="secao-historico">
          <h3 class="section-title ui-display"><span class="color-secondary">></span> Registro de Missões</h3>
          
          <div v-if="dados.historico.length === 0" class="vazio glass-card">
            Nenhum registro encontrado.
          </div>
          
          <div class="historico-container glass-card" v-else>
            <div v-for="item in historicoComTendencia" :key="item.resultado_id" class="historico-item">
              <div class="hist-info">
                <span class="hist-nome">{{ item.simulado }} <span class="tentativa-badge ui-display">T{{ item.tentativa }}</span></span>
                <span class="hist-data text-dim">{{ item.data }}</span>
              </div>
              <div class="hist-score">
                <span class="hist-acertos text-dim">{{ item.acertos }}/{{ item.total }}</span>
                <span class="hist-percentual ui-display" :class="corScoreText(item.score)">{{ item.score }}%</span>
                <div class="hist-trend" :class="item.trend === 'up' ? 'positivo' : (item.trend === 'down' ? 'negativo' : 'text-dim')">
                  <span v-if="item.trend === 'up'">▲ +{{ item.diff }}%</span>
                  <span v-else-if="item.trend === 'down'">▼ {{ item.diff }}%</span>
                  <span v-else>—</span>
                </div>
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

// Lógica de Gamificação
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
      api.get('/profile/'),
      api.get('/resultados/dashboard/'),
    ])
    username.value = perfil.data.username
    dados.value = dashboard.data
    if (dados.value.por_materia.length > 0) {
      materiasAbertas.value = [dados.value.por_materia[0].codigo]
    }
  } catch (error) {
    erro.value = 'Falha ao conectar com o laboratório.'
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
  if (valor >= 50) return 'text-main'
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
.dashboard-wrapper {
  min-height: 100vh;
  /* Reaproveitamos o fundo do login aqui para manter a imersão, mas você pode gerar outro abstrato depois */
  background-image: url('../assets/login-bg-neon.png');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  padding: 20px;
}

/* Navbar */
.navbar {
  display: flex; justify-content: space-between; align-items: center;
  padding: 15px 30px; margin-bottom: 30px;
}
.logo-text { font-size: 1.5rem; letter-spacing: 2px; margin: 0; }
.nav-links { display: flex; gap: 20px; }
.nav-item { color: var(--text-dim); text-decoration: none; font-size: 0.85rem; letter-spacing: 1px; transition: color 0.3s; }
.nav-item:hover, .nav-item.router-link-active { color: var(--color-primary); text-shadow: var(--glow-primary); }
.link-admin { border: 1px solid var(--color-secondary); padding: 4px 10px; border-radius: 4px; color: var(--color-secondary); }

/* User Stats & XP */
.user-stats { display: flex; align-items: center; gap: 20px; }
.xp-container { display: flex; align-items: center; gap: 12px; }
.level-badge { background: var(--color-secondary); color: white; padding: 2px 8px; border-radius: 4px; font-size: 0.75rem; box-shadow: var(--glow-secondary); }
.xp-bar-bg { width: 150px; height: 6px; background: rgba(255, 255, 255, 0.1); border-radius: 99px; overflow: hidden; }
.xp-bar-fill { height: 100%; background: linear-gradient(90deg, var(--color-primary), var(--color-secondary)); box-shadow: var(--glow-primary); transition: width 1s cubic-bezier(0.4, 0, 0.2, 1); }
.xp-text { font-size: 0.75rem; color: var(--text-dim); }

.streak-badge { display: flex; align-items: center; gap: 5px; padding: 4px 12px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.2); transition: all 0.3s; }
.streak-badge.fogo-ativo { border-color: #ff9d00; background: rgba(255, 157, 0, 0.1); box-shadow: 0 0 10px rgba(255, 157, 0, 0.2); }
.fire-icon { font-size: 1rem; filter: grayscale(1); }
.fogo-ativo .fire-icon { filter: grayscale(0); animation: pulsar 2s infinite alternate; }
.streak-count { font-size: 0.85rem; color: var(--text-dim); }
.fogo-ativo .streak-count { color: #ff9d00; font-weight: 700; }

.btn-logout { background: transparent; color: var(--text-dim); border: 1px solid rgba(255,255,255,0.2); padding: 6px 16px; border-radius: 6px; cursor: pointer; font-size: 0.75rem; transition: all 0.3s; }
.btn-logout:hover { border-color: var(--color-error); color: var(--color-error); }

@keyframes pulsar { from { transform: scale(1); } to { transform: scale(1.1); } }

/* Main Content */
.main-content { max-width: 1200px; margin: 0 auto; }
.welcome-header { margin-bottom: 30px; text-align: center; }
.welcome-header h2 { font-size: 2rem; margin-bottom: 5px; text-shadow: 0 0 10px rgba(255,255,255,0.2); }
.section-title { font-size: 1.2rem; margin-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 10px; }

/* Stats Grid */
.stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; }
.card-resumo { padding: 25px; text-align: center; display: flex; flex-direction: column; gap: 5px; border-top: 2px solid transparent; transition: all 0.3s; }
.card-resumo:hover { transform: translateY(-3px); border-top-color: var(--color-primary); }
.resumo-valor { font-size: 2.5rem; }
.resumo-label { font-size: 0.75rem; color: var(--text-dim); letter-spacing: 1px; }
.card-resumo.acao { cursor: pointer; background: rgba(0, 229, 255, 0.05); border: 1px solid rgba(0, 229, 255, 0.2); }
.card-resumo.acao:hover { background: rgba(0, 229, 255, 0.15); box-shadow: var(--glow-primary); }
.action-icon { font-size: 2rem; margin-bottom: 5px; display: inline-block; }

/* Split Layout */
.content-split { display: grid; grid-template-columns: 1.5fr 1fr; gap: 30px; }

/* Materias Accordion */
.card-materia { margin-bottom: 15px; overflow: hidden; transition: all 0.3s; }
.materia-header { display: flex; justify-content: space-between; align-items: center; padding: 18px 20px; cursor: pointer; }
.materia-header:hover { background: rgba(255,255,255,0.02); }
.materia-info { display: flex; align-items: center; gap: 15px; }
.materia-badge { background: rgba(0, 229, 255, 0.1); color: var(--color-primary); padding: 4px 8px; border-radius: 4px; font-size: 0.75rem; border: 1px solid rgba(0, 229, 255, 0.3); }
.materia-nome { font-weight: 600; font-size: 1rem; }
.materia-direita { display: flex; align-items: center; gap: 15px; }
.materia-detalhe { font-size: 0.8rem; }
.materia-percentual { font-size: 1.1rem; min-width: 45px; text-align: right; }

.barra-mini { width: 100px; height: 6px; background: rgba(255,255,255,0.1); border-radius: 99px; overflow: hidden; }
.barra-mini.pequena { width: 70px; }
.barra-fill { height: 100%; border-radius: 99px; transition: width 0.5s ease; }
.bg-success { background: var(--color-success); box-shadow: var(--glow-success); }
.bg-warning { background: #F5A623; }
.bg-error { background: var(--color-error); }
.bg-dim { background: var(--text-dim); }

.diferenca { font-size: 0.8rem; min-width: 50px; text-align: right; }
.positivo { color: var(--color-success); }
.negativo { color: var(--color-error); }

/* Temas Internos */
.temas-lista { background: rgba(0,0,0,0.2); border-top: 1px solid rgba(255,255,255,0.05); padding: 10px 0; }
.temas-legenda { display: flex; justify-content: flex-end; gap: 50px; padding: 5px 25px; font-size: 0.7rem; letter-spacing: 1px; }
.tema-item { display: flex; justify-content: space-between; align-items: center; padding: 12px 25px 12px 50px; border-bottom: 1px solid rgba(255,255,255,0.02); }
.tema-item:last-child { border-bottom: none; }
.tema-info { display: flex; flex-direction: column; }
.tema-nome { font-size: 0.9rem; }
.tema-detalhe { font-size: 0.75rem; }
.tema-direita { display: flex; flex-direction: column; gap: 6px; align-items: flex-end; }
.barra-dupla { display: flex; align-items: center; gap: 10px; }
.tema-percentual { font-size: 0.85rem; min-width: 40px; text-align: right; }
.opacity-50 { opacity: 0.5; }

/* Historico Custom List */
.historico-container { padding: 10px; }
.historico-item { display: flex; justify-content: space-between; align-items: center; padding: 15px; border-bottom: 1px solid rgba(255,255,255,0.05); transition: background 0.2s; }
.historico-item:hover { background: rgba(255,255,255,0.02); }
.historico-item:last-child { border-bottom: none; }
.hist-info { display: flex; flex-direction: column; gap: 4px; }
.hist-nome { font-size: 0.95rem; font-weight: 600; display: flex; align-items: center; gap: 10px; }
.tentativa-badge { background: rgba(176, 38, 255, 0.15); color: var(--color-secondary); padding: 2px 6px; border-radius: 4px; font-size: 0.65rem; border: 1px solid rgba(176, 38, 255, 0.3); }
.hist-data { font-size: 0.75rem; }
.hist-score { display: flex; align-items: center; gap: 15px; }
.hist-acertos { font-size: 0.8rem; }
.hist-percentual { font-size: 1.1rem; min-width: 45px; text-align: right; }
.hist-trend { font-size: 0.8rem; min-width: 60px; text-align: right; font-weight: 600; }

/* Utilitários Locais */
.color-primary { color: var(--color-primary); }
.color-secondary { color: var(--color-secondary); }
.color-success { color: var(--color-success); }
.color-error { color: var(--color-error); }
.text-main { color: var(--text-main); }
.text-dim { color: var(--text-dim); }

@media (max-width: 1024px) {
  .content-split { grid-template-columns: 1fr; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .user-stats { display: none; /* Simplifica mobile */ }
}
</style>
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
      </nav>

      <div class="sidebar-footer">
        <button @click="logout" class="btn-logout-clean">Sair</button>
      </div>
    </aside>

    <main class="main-content">
      
      <header class="top-bar">
        <div class="welcome-msg">
          <h2>Análise de Resultado</h2>
          <p class="text-secondary">Diagnóstico detalhado da sua simulação.</p>
        </div>
        <button @click="$router.push('/simulados')" class="btn-secondary-action">
          Voltar para Avaliações
        </button>
      </header>

      <div v-if="carregando" class="skeleton-wrapper">
        <div class="skeleton-hero shimmer"></div>
        <div class="skeleton-grid">
          <div class="skeleton-box shimmer" v-for="n in 4" :key="n" style="height: 120px;"></div>
        </div>
      </div>

      <div v-else-if="erro" class="empty-state-card clean-card">
        <div class="empty-icon-wrapper error-wrapper"><span class="empty-icon">⚠️</span></div>
        <h3 class="empty-title">Erro na decodificação.</h3>
        <p class="empty-subtitle">{{ erro }}</p>
        <button @click="$router.push('/simulados')" class="btn-primary-action">Voltar</button>
      </div>

      <div v-else class="resultado-grid">

        <div class="score-hero clean-card">
          <div class="hero-content">
            <div class="hero-icon-container" :class="corScoreBox(parseFloat(gabarito.score))">
              <span class="hero-icon">{{ parseFloat(gabarito.score) >= 70 ? '🏆' : parseFloat(gabarito.score) >= 50 ? '📈' : '📚' }}</span>
            </div>
            <div class="hero-text">
              <h2 class="hero-title">{{ mensagemMotivacional }}</h2>
              <p class="hero-subtitle">{{ gabarito.simulado_titulo }}</p>
            </div>
          </div>

          <div class="metrics-grid">
            <div class="metric-box">
              <span class="metric-label">Aproveitamento</span>
              <span class="metric-value" :class="corScoreText(parseFloat(gabarito.score))">{{ gabarito.score }}%</span>
            </div>
            <div class="metric-box">
              <span class="metric-label">Acertos</span>
              <span class="metric-value text-green">{{ gabarito.acertos }}</span>
            </div>
            <div class="metric-box">
              <span class="metric-label">Erros</span>
              <span class="metric-value text-red">{{ gabarito.total_questoes - gabarito.acertos }}</span>
            </div>
            <div class="metric-box">
              <span class="metric-label">Total</span>
              <span class="metric-value text-primary">{{ gabarito.total_questoes }}</span>
            </div>
          </div>
        </div>

        <div v-if="gabarito.resumo_por_materia && gabarito.resumo_por_materia.length > 0" class="section-card clean-card">
          <h3 class="section-title">Diagnóstico por Disciplina</h3>
          <div class="subjects-grid">
            <div v-for="mat in gabarito.resumo_por_materia" :key="mat.materia" class="subject-box">
              <div class="subject-header">
                <span class="subject-badge">{{ mat.materia }}</span>
                <span class="subject-score" :class="corScoreText(mat.percentual)">{{ mat.percentual }}%</span>
              </div>
              <div class="subject-name">{{ mat.nome || mat.materia }}</div>
              <div class="progress-container">
                <div class="progress-fill" :class="corScoreBg(mat.percentual)" :style="{ width: mat.percentual + '%' }"></div>
              </div>
              <div class="subject-details">{{ mat.acertos }}/{{ mat.total }} questões corretas</div>
            </div>
          </div>
        </div>

        <div v-if="gabarito.temas_com_erro && gabarito.temas_com_erro.length > 0" class="section-card clean-card intel-card">
          <div class="intel-header-box">
            <span class="intel-badge">FASE 7: RECOMENDAÇÃO TÁTICA</span>
            <h3 class="section-title margin-0">Trilha de Revisão Personalizada</h3>
            <p class="section-subtitle">Baseado nos seus erros, o laboratório separou estes materiais para fechar suas lacunas:</p>
          </div>

          <div class="revision-grid">
            <div v-for="tema in gabarito.temas_com_erro" :key="tema.tema" class="revision-box">
              <div class="revision-header">
                <div class="revision-info">
                  <span class="rev-badge">{{ tema.materia }}</span>
                  <span class="rev-name">{{ tema.tema }}</span>
                </div>
                <span class="rev-errors">{{ tema.erros }} erro{{ tema.erros > 1 ? 's' : '' }}</span>
              </div>
              
              <div class="revision-materials" v-if="tema.materiais_recomendados && tema.materiais_recomendados.length > 0">
                <p class="materials-title">Conteúdo Recomendado:</p>
                <a v-for="(mat, i) in tema.materiais_recomendados" :key="i" :href="mat.url" target="_blank" class="material-link">
                  <span class="mat-icon">{{ getIconeMaterial(mat.tipo) }}</span>
                  <span class="mat-name">{{ mat.titulo }}</span>
                  <span class="mat-action">Acessar ↗</span>
                </a>
              </div>
              
              <div class="revision-empty" v-else>
                O laboratório está processando novos materiais para este tema.
              </div>
            </div>
          </div>
        </div>

        <EvolucaoGrafico v-if="evolucaoData && evolucaoData.length > 1" :evolucao="evolucaoData" />

        <div class="section-card clean-card">
          <div class="filter-header">
            <h3 class="section-title margin-0">Auditoria do Gabarito</h3>
            <div class="filter-group">
              <button v-for="f in filtros" :key="f.valor" @click="filtroAtivo = f.valor" class="btn-filter" :class="{ active: filtroAtivo === f.valor }">
                {{ f.label }}
                <span class="filter-count">{{ contarFiltro(f.valor) }}</span>
              </button>
            </div>
          </div>

          <div class="questions-list">
            <div v-if="questoesFiltradas.length === 0" class="empty-filter">Nenhuma questão nesta categoria.</div>
            
            <div v-for="questao in questoesFiltradas" :key="questao.ordem" class="q-card" :class="{ 'q-correct': questao.correta === true, 'q-wrong': questao.correta === false, 'q-null': questao.correta === null }">
              
              <div class="q-header" @click="toggleQuestao(questao.ordem)">
                <div class="q-meta">
                  <div class="q-status-icon" :class="{ 'bg-green text-white': questao.correta === true, 'bg-red text-white': questao.correta === false, 'bg-gray': questao.correta === null }">
                    {{ questao.correta === true ? '✓' : questao.correta === false ? '✗' : '—' }}
                  </div>
                  <span class="q-number">Questão {{ questao.ordem }}</span>
                  <span v-if="questao.materia" class="q-tag q-tag-mat">{{ questao.materia }}</span>
                  <span v-if="questao.tema" class="q-tag">{{ questao.tema }}</span>
                  <span class="q-tag-diff" :class="'diff-' + questao.dificuldade">{{ labelDificuldade(questao.dificuldade) }}</span>
                </div>

                <div class="q-compact-res" v-if="!questoesAbertas.includes(questao.ordem)">
                  <span v-if="questao.correta === true" class="text-green font-medium">Acertou · {{ questao.opcao_escolhida }}</span>
                  <span v-else-if="questao.correta === false" class="text-red font-medium">Marcou {{ questao.opcao_escolhida }} · Correta era {{ questao.resposta_correta }}</span>
                  <span v-else class="text-gray">Em branco</span>
                </div>

                <span class="toggle-icon">{{ questoesAbertas.includes(questao.ordem) ? '▲' : '▼' }}</span>
              </div>

              <div v-if="questoesAbertas.includes(questao.ordem)" class="q-body">
                <p class="q-text">{{ questao.enunciado }}</p>
                <img v-if="questao.imagem_enunciado" :src="questao.imagem_enunciado" class="q-image" alt="Imagem" />

                <div class="options-list">
                  <div v-for="opcao in opcoesDaQuestao(questao)" :key="opcao.letra" class="opt-card" :class="classeAlternativa(opcao.letra, questao)">
                    <span class="opt-letter">{{ opcao.letra }}</span>
                    <span class="opt-text">{{ opcao.texto }}</span>
                    
                    <div class="opt-indicators">
                      <span v-if="opcao.letra === questao.resposta_correta" class="ind-correct">✓ Resposta Correta</span>
                      <span v-if="opcao.letra === questao.opcao_escolhida && !questao.correta" class="ind-wrong">Sua Marcação</span>
                    </div>
                  </div>
                </div>

                <div v-if="questao.explicacao" class="explanation-box">
                  <div class="exp-title">💡 Resolução do Laboratório</div>
                  <p class="exp-text">{{ questao.explicacao }}</p>
                </div>
                
                <div v-if="questao.correta === null" class="null-warning">Questão deixada em branco pelo candidato.</div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup>
// LÓGICA INTACTA
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../services/api.js'
import EvolucaoGrafico from '../components/EvolucaoGrafico.vue'

const router = useRouter()
const route  = useRoute()

const carregando = ref(true)
const erro       = ref('')

const gabarito = ref({
  simulado_id:        null,
  simulado_titulo:    '',
  acertos:            0,
  total_questoes:     0,
  score:              '0.00',
  realizado_em:       null,
  questoes:           [],
  resumo_por_materia: [],
  temas_com_erro:     [],
})

const evolucaoData = ref([])
const questoesAbertas = ref([])
const filtroAtivo = ref('todas')

const filtros = [
  { valor: 'todas',   label: 'Todas'  },
  { valor: 'certas',  label: 'Corretas' },
  { valor: 'erradas', label: 'Incorretas' },
]

const questoesFiltradas = computed(() => {
  if (filtroAtivo.value === 'certas')  return gabarito.value.questoes.filter(q => q.correta === true)
  if (filtroAtivo.value === 'erradas') return gabarito.value.questoes.filter(q => q.correta === false)
  return gabarito.value.questoes
})

const mensagemMotivacional = computed(() => {
  const score = parseFloat(gabarito.value.score)
  if (score >= 90) return 'Desempenho de Elite. 🏆'
  if (score >= 70) return 'Estratégia Sólida. Muito bem.'
  if (score >= 50) return 'Evolução Detectada. Mantenha o foco.'
  return 'Atenção Necessária. Revise a Trilha.'
})

function contarFiltro(valor) {
  if (valor === 'certas')  return gabarito.value.questoes.filter(q => q.correta === true).length
  if (valor === 'erradas') return gabarito.value.questoes.filter(q => q.correta === false).length
  return gabarito.value.questoes.length
}

function toggleQuestao(ordem) {
  const index = questoesAbertas.value.indexOf(ordem)
  if (index === -1) {
    questoesAbertas.value.push(ordem)
  } else {
    questoesAbertas.value.splice(index, 1)
  }
}

function opcoesDaQuestao(questao) {
  return [
    { letra: 'A', texto: questao.opcao_a },
    { letra: 'B', texto: questao.opcao_b },
    { letra: 'C', texto: questao.opcao_c },
    { letra: 'D', texto: questao.opcao_d },
    { letra: 'E', texto: questao.opcao_e },
  ].filter(op => op.texto && op.texto.trim() !== '')
}

function classeAlternativa(letra, questao) {
  if (letra === questao.resposta_correta) return 'opt-correct'
  if (letra === questao.opcao_escolhida && !questao.correta) return 'opt-wrong'
  return ''
}

function corScoreText(v) { return v >= 70 ? 'text-green' : v >= 50 ? 'text-orange' : 'text-red'; }
function corScoreBg(v) { return v >= 70 ? 'bg-green' : v >= 50 ? 'bg-orange' : 'bg-red'; }
function corScoreBox(v) { return v >= 70 ? 'box-green' : v >= 50 ? 'box-orange' : 'box-red'; }

function labelDificuldade(dif) {
  const mapa = { F: 'Fácil', M: 'Média', D: 'Difícil' }
  return mapa[dif] || dif
}

function getIconeMaterial(tipo) {
  const icones = { VIDEO: '▶️', PDF: '📄', LINK: '🔗' }
  return icones[tipo] || '📚'
}

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_role')
  router.push({ name: 'login' })
}

onMounted(async () => {
  try {
    const id = route.params.id
    const response = await api.get(`/api/resultados/${id}/gabarito/`) // Rota API Corrigida
    gabarito.value = response.data

    gabarito.value.questoes.forEach(q => {
      if (q.correta === false) questoesAbertas.value.push(q.ordem)
    })

    if (gabarito.value.simulado_id) {
      try {
        const responseEvolucao = await api.get(`/api/resultados/evolucao/${gabarito.value.simulado_id}/`) // Rota API Corrigida
        evolucaoData.value = responseEvolucao.data
      } catch (err) {
        console.error("Erro Evolução:", err)
      }
    }
  } catch (error) {
    const acertos = parseInt(route.query.acertos)
    const total   = parseInt(route.query.total)
    const score   = route.query.score?.replace('%', '') || '0'

    if (acertos !== undefined && total !== undefined && !isNaN(acertos)) {
      gabarito.value = {
        simulado_titulo:    'Simulação Processada',
        acertos:            acertos || 0,
        total_questoes:     total   || 0,
        score:              score,
        questoes:           [],
        resumo_por_materia: [],
        temas_com_erro:     [],
      }
    } else {
      erro.value = 'Falha na extração de dados do laboratório.'
    }
  } finally {
    carregando.value = false
  }
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Base & Layout (Herdado do Dashboard) */
.dashboard-layout { display: flex; min-height: 100vh; width: 100vw; position: absolute; top: 0; left: 0; background-color: #F1F5F9; font-family: 'Inter', sans-serif; }
.sidebar { width: 220px; background: linear-gradient(180deg, #0A2540 0%, #0052FF 100%); color: white; display: flex; flex-direction: column; padding: 30px 20px; position: fixed; height: 100vh; z-index: 100; }
.logo-white { color: #FFFFFF; font-weight: 800; font-size: 1.3rem; }
.logo-accent { color: #00D09C; font-weight: 800; font-size: 1.3rem; }
.tagline { font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1.2px; opacity: 0.7; margin-top: 2px; }
.sidebar-nav { margin-top: 40px; flex: 1; }
.nav-link { display: flex; align-items: center; gap: 10px; color: rgba(255, 255, 255, 0.8); text-decoration: none; padding: 12px 14px; border-radius: 8px; margin-bottom: 5px; font-weight: 500; font-size: 0.9rem; transition: all 0.2s; }
.nav-link:hover { background: rgba(255, 255, 255, 0.15); color: white; }
.btn-logout-clean { background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); color: white; width: 100%; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.85rem; }

.main-content { flex: 1; margin-left: 220px; padding: 40px 50px; }
.top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 35px; }
.welcome-msg h2 { font-size: 1.7rem; font-weight: 700; color: #0F172A; margin: 0; }
.text-secondary { color: #475569; font-size: 0.9rem; margin-top: 4px; }
.btn-secondary-action { background: white; border: 1px solid #CBD5E1; padding: 10px 20px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.2s; color: #334155; }
.btn-secondary-action:hover { border-color: #0052FF; color: #0052FF; }

/* Utilitários Clean */
.clean-card { background: white; border: 1px solid #E2E8F0; border-radius: 16px; box-shadow: 0 4px 10px rgba(0, 0, 0, 0.03); margin-bottom: 24px; padding: 30px; }
.section-title { font-size: 1.2rem; font-weight: 700; color: #0F172A; margin-bottom: 20px; margin-top: 0; }
.margin-0 { margin-bottom: 6px !important; }

/* Cores Globais */
.text-green { color: #10B981; } .text-orange { color: #F59E0B; } .text-red { color: #EF4444; } .text-primary { color: #0052FF; }
.bg-green { background-color: #10B981; } .bg-orange { background-color: #F59E0B; } .bg-red { background-color: #EF4444; } .bg-gray { background-color: #94A3B8; }
.text-white { color: white; }

/* Skeleton & Error */
.skeleton-wrapper { width: 100%; }
.shimmer { position: relative; overflow: hidden; background-color: #E2E8F0; border-radius: 16px; }
.shimmer::after { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent); animation: loading 1.5s infinite; }
@keyframes loading { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }
.skeleton-hero { height: 180px; margin-bottom: 24px; }
.skeleton-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.empty-state-card { text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px; }
.error-wrapper { background: #FEF2F2 !important; }
.btn-primary-action { background: #0052FF; color: white; padding: 12px 24px; border-radius: 8px; font-weight: 600; border: none; cursor: pointer; margin-top: 20px; }

/* HERO DE PERFORMANCE */
.score-hero { display: flex; justify-content: space-between; align-items: center; padding: 40px !important; }
.hero-content { display: flex; align-items: center; gap: 20px; }
.hero-icon-container { width: 80px; height: 80px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; }
.box-green { background: #ECFDF5; } .box-orange { background: #FFF7ED; } .box-red { background: #FEF2F2; }
.hero-title { font-size: 1.8rem; font-weight: 800; color: #0F172A; margin: 0 0 4px 0; }
.hero-subtitle { color: #64748B; font-size: 1rem; margin: 0; font-weight: 500; }

.metrics-grid { display: flex; gap: 15px; }
.metric-box { background: #F8FAFC; border: 1px solid #E2E8F0; padding: 15px 25px; border-radius: 12px; display: flex; flex-direction: column; align-items: center; min-width: 110px; }
.metric-value { font-size: 1.8rem; font-weight: 800; line-height: 1.2; }
.metric-label { font-size: 0.75rem; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }

/* DISCIPLINAS */
.subjects-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 16px; }
.subject-box { background: #F8FAFC; border: 1px solid #E2E8F0; padding: 18px; border-radius: 12px; }
.subject-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.subject-badge { background: #E0E7FF; color: #4338CA; padding: 4px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 700; }
.subject-score { font-weight: 800; font-size: 1.1rem; }
.subject-name { font-size: 0.85rem; color: #475569; font-weight: 600; margin-bottom: 12px; }
.progress-container { height: 6px; background: #E2E8F0; border-radius: 10px; overflow: hidden; margin-bottom: 8px; }
.progress-fill { height: 100%; }
.subject-details { font-size: 0.75rem; color: #94A3B8; font-weight: 500; }

/* TRILHA DE REVISÃO (INTELIGÊNCIA) */
.intel-card { border-color: #0052FF; position: relative; overflow: hidden; }
.intel-card::before { content: ''; position: absolute; top: 0; left: 0; width: 6px; height: 100%; background: #0052FF; }
.intel-badge { display: inline-block; background: #EFF6FF; color: #0052FF; font-size: 0.65rem; font-weight: 800; padding: 4px 10px; border-radius: 4px; letter-spacing: 1px; margin-bottom: 10px; }
.section-subtitle { color: #64748B; font-size: 0.95rem; margin-bottom: 24px; }
.revision-grid { display: flex; flex-direction: column; gap: 16px; }
.revision-box { border: 1px solid #E2E8F0; border-radius: 12px; overflow: hidden; }
.revision-header { background: #F8FAFC; padding: 15px 20px; display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #E2E8F0; }
.revision-info { display: flex; align-items: center; gap: 12px; }
.rev-badge { background: #0052FF; color: white; padding: 3px 8px; border-radius: 6px; font-size: 0.7rem; font-weight: 700; }
.rev-name { font-weight: 600; color: #0F172A; }
.rev-errors { background: #FEF2F2; color: #EF4444; font-size: 0.75rem; font-weight: 700; padding: 3px 10px; border-radius: 20px; }
.revision-materials { padding: 20px; background: white; }
.materials-title { font-size: 0.75rem; text-transform: uppercase; color: #94A3B8; font-weight: 700; margin-bottom: 12px; letter-spacing: 0.5px; }
.material-link { display: flex; align-items: center; gap: 15px; padding: 14px 18px; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; text-decoration: none; margin-bottom: 8px; transition: all 0.2s; }
.material-link:hover { border-color: #0052FF; background: #EFF6FF; transform: translateY(-1px); }
.mat-name { flex: 1; font-weight: 600; color: #1E293B; font-size: 0.9rem; }
.mat-action { font-size: 0.75rem; font-weight: 700; color: #0052FF; }

/* GABARITO & FILTROS */
.filter-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; flex-wrap: wrap; gap: 15px; }
.filter-group { display: flex; gap: 10px; background: #F1F5F9; padding: 4px; border-radius: 10px; }
.btn-filter { display: flex; align-items: center; gap: 8px; padding: 8px 16px; border: none; border-radius: 6px; background: transparent; cursor: pointer; font-size: 0.85rem; font-weight: 600; color: #64748B; transition: all 0.2s; }
.btn-filter.active { background: white; color: #0F172A; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.filter-count { background: #E2E8F0; padding: 2px 6px; border-radius: 10px; font-size: 0.7rem; }
.btn-filter.active .filter-count { background: #0052FF; color: white; }

/* QUESTÕES (Cards Expandíveis) */
.questions-list { display: flex; flex-direction: column; gap: 12px; }
.q-card { border: 1px solid #E2E8F0; border-radius: 12px; overflow: hidden; background: white; }
.q-correct { border-left: 4px solid #10B981; } .q-wrong { border-left: 4px solid #EF4444; } .q-null { border-left: 4px solid #94A3B8; }

.q-header { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; cursor: pointer; transition: background 0.2s; gap: 15px; }
.q-header:hover { background: #F8FAFC; }
.q-meta { display: flex; align-items: center; gap: 12px; flex: 1; flex-wrap: wrap; }
.q-status-icon { width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 0.75rem; font-weight: 800; }
.q-number { font-weight: 700; color: #1E293B; font-size: 0.95rem; }
.q-tag { background: #F1F5F9; color: #475569; padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 600; }
.q-tag-mat { background: #E0E7FF; color: #4338CA; }
.q-tag-diff { padding: 3px 8px; border-radius: 4px; font-size: 0.7rem; font-weight: 700; }
.diff-F { background: #ECFDF5; color: #047857; } .diff-M { background: #FEF3C7; color: #B45309; } .diff-D { background: #FEF2F2; color: #B91C1C; }

.q-compact-res { font-size: 0.85rem; }
.toggle-icon { color: #94A3B8; font-size: 0.7rem; }

.q-body { padding: 25px; border-top: 1px solid #F1F5F9; }
.q-text { font-size: 1rem; color: #334155; line-height: 1.6; margin-bottom: 20px; }
.q-image { max-width: 100%; border-radius: 8px; margin-bottom: 20px; border: 1px solid #E2E8F0; }

.options-list { display: flex; flex-direction: column; gap: 10px; margin-bottom: 25px; }
.opt-card { display: flex; align-items: center; gap: 15px; padding: 14px 18px; border: 1px solid #E2E8F0; border-radius: 8px; background: #F8FAFC; transition: all 0.2s; }
.opt-correct { border-color: #10B981; background: #ECFDF5; } .opt-wrong { border-color: #EF4444; background: #FEF2F2; }
.opt-letter { width: 32px; height: 32px; background: white; border: 1px solid #E2E8F0; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.85rem; color: #64748B; }
.opt-correct .opt-letter { background: #10B981; color: white; border-color: #10B981; } .opt-wrong .opt-letter { background: #EF4444; color: white; border-color: #EF4444; }
.opt-text { flex: 1; color: #1E293B; font-size: 0.95rem; line-height: 1.5; }
.opt-indicators { display: flex; flex-direction: column; align-items: flex-end; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; }
.ind-correct { color: #10B981; } .ind-wrong { color: #EF4444; }

.explanation-box { background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 4px solid #0052FF; border-radius: 8px; padding: 20px; }
.exp-title { font-size: 0.8rem; font-weight: 800; color: #0052FF; text-transform: uppercase; margin-bottom: 10px; letter-spacing: 0.5px; }
.exp-text { color: #334155; line-height: 1.6; font-size: 0.95rem; margin: 0; }
.null-warning { background: #F1F5F9; color: #64748B; text-align: center; padding: 15px; border-radius: 8px; font-weight: 600; font-size: 0.85rem; }

/* Responsivo */
@media (max-width: 1000px) {
  .sidebar { width: 70px; padding: 30px 10px; }
  .logo-text, .tagline, .nav-link span:not(.icon), .btn-logout-clean { display: none; }
  .main-content { margin-left: 70px; padding: 20px; }
  .score-hero { flex-direction: column; text-align: center; }
  .hero-content { flex-direction: column; margin-bottom: 30px; }
  .metrics-grid { width: 100%; display: grid; grid-template-columns: repeat(2, 1fr); }
  .q-meta { flex-direction: column; align-items: flex-start; }
  .q-compact-res { display: none; }
}
</style>
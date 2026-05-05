<template>
  <DashboardLayout :username="username" :is-admin="isAdmin">
    <header class="page-header">
      <div>
        <h2 class="page-title">Análise de Resultado</h2>
        <p class="page-sub">Diagnóstico detalhado da sua simulação.</p>
      </div>
      <OrbynButton variant="ghost" size="sm" @click="$router.push('/simulados')">
        ← Voltar
      </OrbynButton>
    </header>

    <!-- Skeleton -->
    <div v-if="carregando" class="skeleton-stack">
      <div class="sk-hero" />
      <div class="sk-grid">
        <div v-for="n in 4" :key="n" class="sk-box" />
      </div>
    </div>

    <!-- Erro -->
    <div v-else-if="erro" class="empty-state">
      <div class="empty-icon nova">⚠</div>
      <h3 class="empty-title">Erro na decodificação.</h3>
      <p class="empty-sub">{{ erro }}</p>
      <OrbynButton variant="primary" size="sm" class="mt-5" @click="$router.push('/simulados')">Voltar</OrbynButton>
    </div>

    <div v-else class="resultado-stack">

      <!-- Hero de score -->
      <div class="score-hero">
        <div class="hero-left">
          <div class="hero-icon-wrap" :class="heroAccent(parseFloat(gabarito.score))">
            {{ parseFloat(gabarito.score) >= 70 ? '◆' : parseFloat(gabarito.score) >= 50 ? '◈' : '◎' }}
          </div>
          <div>
            <h2 class="hero-title">{{ mensagemMotivacional }}</h2>
            <p class="hero-sub">{{ gabarito.simulado_titulo }}</p>
          </div>
        </div>
        <div class="metrics">
          <div class="metric">
            <span class="metric-val" :class="scoreColor(parseFloat(gabarito.score))">{{ gabarito.score }}%</span>
            <span class="metric-label">Aproveitamento</span>
          </div>
          <div class="metric">
            <span class="metric-val stellar">{{ gabarito.acertos }}</span>
            <span class="metric-label">Acertos</span>
          </div>
          <div class="metric">
            <span class="metric-val nova">{{ gabarito.total_questoes - gabarito.acertos }}</span>
            <span class="metric-label">Erros</span>
          </div>
          <div class="metric">
            <span class="metric-val orbit">{{ gabarito.total_questoes }}</span>
            <span class="metric-label">Total</span>
          </div>
        </div>
      </div>

      <!-- Disciplinas -->
      <div v-if="gabarito.resumo_por_materia?.length" class="section-card">
        <h3 class="section-title">Diagnóstico por Disciplina</h3>
        <div class="subjects-grid">
          <div v-for="mat in gabarito.resumo_por_materia" :key="mat.materia" class="subject-box">
            <div class="subject-top">
              <span class="subject-tag">{{ mat.materia }}</span>
              <span class="subject-score" :class="scoreColor(mat.percentual)">{{ mat.percentual }}%</span>
            </div>
            <div class="subject-name">{{ mat.nome || mat.materia }}</div>
            <div class="progress-bar">
              <div class="progress-fill" :class="scoreBg(mat.percentual)" :style="{ width: mat.percentual + '%' }" />
            </div>
            <div class="subject-detail">{{ mat.acertos }}/{{ mat.total }} questões corretas</div>
          </div>
        </div>
      </div>

      <!-- Trilha de revisão -->
      <div v-if="gabarito.temas_com_erro?.length" class="section-card section-card--orbit">
        <div class="intel-header">
          <span class="intel-badge">Recomendação Tática</span>
          <h3 class="section-title no-mb">Trilha de Revisão Personalizada</h3>
          <p class="intel-sub">Baseado nos seus erros, o laboratório separou estes materiais:</p>
        </div>
        <div class="revision-list">
          <div v-for="tema in gabarito.temas_com_erro" :key="tema.tema" class="revision-item">
            <div class="revision-header">
              <div class="revision-meta">
                <span class="rev-mat">{{ tema.materia }}</span>
                <span class="rev-tema">{{ tema.tema }}</span>
              </div>
              <span class="rev-erros">{{ tema.erros }} erro{{ tema.erros > 1 ? 's' : '' }}</span>
            </div>
            <div v-if="tema.materiais_recomendados?.length" class="materials">
              <a v-for="(m, i) in tema.materiais_recomendados" :key="i"
                 :href="m.url" target="_blank" class="material-link">
                <span>{{ { VIDEO: '▶', PDF: '◧', LINK: '◉' }[m.tipo] || '◎' }}</span>
                <span class="mat-title">{{ m.titulo }}</span>
                <span class="mat-action">Acessar ↗</span>
              </a>
            </div>
            <div v-else class="revision-empty">O laboratório está processando materiais para este tema.</div>
          </div>
        </div>
      </div>

      <!-- Evolução -->
      <EvolucaoGrafico v-if="evolucaoData?.length > 1" :evolucao="evolucaoData" />

      <!-- Gabarito -->
      <div class="section-card">
        <div class="gabarito-header">
          <h3 class="section-title no-mb">Auditoria do Gabarito</h3>
          <div class="filtros">
            <button v-for="f in filtros" :key="f.valor"
                    class="filtro-btn"
                    :class="{ 'filtro-btn--active': filtroAtivo === f.valor }"
                    @click="filtroAtivo = f.valor">
              {{ f.label }}
              <span class="filtro-count">{{ contarFiltro(f.valor) }}</span>
            </button>
          </div>
        </div>

        <div class="questoes-list">
          <div v-if="questoesFiltradas.length === 0" class="filter-empty">Nenhuma questão nesta categoria.</div>

          <div v-for="questao in questoesFiltradas" :key="questao.ordem"
               class="q-item"
               :class="{
                 'q-item--correct': questao.correta === true,
                 'q-item--wrong': questao.correta === false,
                 'q-item--null': questao.correta === null,
               }">
            <div class="q-header" @click="toggleQuestao(questao.ordem)">
              <div class="q-meta">
                <div class="q-status"
                     :class="{ 'q-status--ok': questao.correta, 'q-status--fail': questao.correta === false, 'q-status--blank': questao.correta === null }">
                  {{ questao.correta === true ? '✓' : questao.correta === false ? '✗' : '—' }}
                </div>
                <span class="q-num">Questão {{ questao.ordem }}</span>
                <span v-if="questao.materia" class="q-tag q-tag--mat">{{ questao.materia }}</span>
                <span v-if="questao.tema" class="q-tag">{{ questao.tema }}</span>
                <span class="q-dif" :class="'q-dif--' + questao.dificuldade">{{ labelDif(questao.dificuldade) }}</span>
              </div>
              <div class="q-compact" v-if="!questoesAbertas.includes(questao.ordem)">
                <span v-if="questao.correta === true" class="text-stellar">Acertou · {{ questao.opcao_escolhida }}</span>
                <span v-else-if="questao.correta === false" class="text-nova">{{ questao.opcao_escolhida }} → {{ questao.resposta_correta }}</span>
                <span v-else class="text-dust">Em branco</span>
              </div>
              <span class="q-toggle">{{ questoesAbertas.includes(questao.ordem) ? '▲' : '▼' }}</span>
            </div>

            <div v-if="questoesAbertas.includes(questao.ordem)" class="q-body">
              <p class="q-texto">{{ questao.enunciado }}</p>
              <img v-if="questao.imagem_enunciado" :src="questao.imagem_enunciado" class="q-img" alt="Imagem" />
              <div class="opcoes-list">
                <div v-for="opcao in opcoesDaQuestao(questao)" :key="opcao.letra"
                     class="opcao-item"
                     :class="{
                       'opcao-item--correct': opcao.letra === questao.resposta_correta,
                       'opcao-item--wrong': opcao.letra === questao.opcao_escolhida && !questao.correta,
                     }">
                  <span class="opcao-letra">{{ opcao.letra }}</span>
                  <span class="opcao-texto">{{ opcao.texto }}</span>
                  <div class="opcao-ind">
                    <span v-if="opcao.letra === questao.resposta_correta" class="ind-ok">✓ Correta</span>
                    <span v-if="opcao.letra === questao.opcao_escolhida && !questao.correta" class="ind-fail">Sua marcação</span>
                  </div>
                </div>
              </div>
              <div v-if="questao.explicacao" class="explicacao">
                <div class="exp-title">◈ Resolução do Laboratório</div>
                <p class="exp-text">{{ questao.explicacao }}</p>
              </div>
              <div v-if="questao.correta === null" class="blank-warning">Questão deixada em branco.</div>
            </div>
          </div>
        </div>
      </div>

    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../services/api.js'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import OrbynButton from '../components/ui/OrbynButton.vue'
import EvolucaoGrafico from '../components/EvolucaoGrafico.vue'

const router = useRouter()
const route  = useRoute()
const username = localStorage.getItem('username') || ''
const isAdmin = localStorage.getItem('user_role') === 'admin'
const carregando = ref(true)
const erro = ref('')

const gabarito = ref({
  simulado_id: null, simulado_titulo: '', acertos: 0,
  total_questoes: 0, score: '0.00', realizado_em: null,
  questoes: [], resumo_por_materia: [], temas_com_erro: [],
})

const evolucaoData = ref([])
const questoesAbertas = ref([])
const filtroAtivo = ref('todas')
const filtros = [
  { valor: 'todas',   label: 'Todas'    },
  { valor: 'certas',  label: 'Corretas' },
  { valor: 'erradas', label: 'Incorretas' },
]

const questoesFiltradas = computed(() => {
  if (filtroAtivo.value === 'certas')  return gabarito.value.questoes.filter(q => q.correta === true)
  if (filtroAtivo.value === 'erradas') return gabarito.value.questoes.filter(q => q.correta === false)
  return gabarito.value.questoes
})

const mensagemMotivacional = computed(() => {
  const s = parseFloat(gabarito.value.score)
  if (s >= 90) return 'Desempenho de Elite.'
  if (s >= 70) return 'Estratégia Sólida. Muito bem.'
  if (s >= 50) return 'Evolução Detectada. Mantenha o foco.'
  return 'Atenção Necessária. Revise a Trilha.'
})

function contarFiltro(v) {
  if (v === 'certas')  return gabarito.value.questoes.filter(q => q.correta === true).length
  if (v === 'erradas') return gabarito.value.questoes.filter(q => q.correta === false).length
  return gabarito.value.questoes.length
}

function toggleQuestao(ordem) {
  const i = questoesAbertas.value.indexOf(ordem)
  if (i === -1) questoesAbertas.value.push(ordem)
  else questoesAbertas.value.splice(i, 1)
}

function opcoesDaQuestao(q) {
  return [
    { letra: 'A', texto: q.opcao_a }, { letra: 'B', texto: q.opcao_b },
    { letra: 'C', texto: q.opcao_c }, { letra: 'D', texto: q.opcao_d },
    { letra: 'E', texto: q.opcao_e },
  ].filter(o => o.texto && o.texto.trim())
}

function scoreColor(v) { return v >= 70 ? 'stellar' : v >= 50 ? 'flare' : 'nova' }
function scoreBg(v)    { return v >= 70 ? 'bg-stellar' : v >= 50 ? 'bg-flare' : 'bg-nova' }
function heroAccent(v) { return v >= 70 ? 'hero--stellar' : v >= 50 ? 'hero--flare' : 'hero--nova' }
function labelDif(d)   { return { F: 'Fácil', M: 'Média', D: 'Difícil' }[d] || d }

onMounted(async () => {
  try {
    const id = route.params.id
    const res = await api.get(`/api/resultados/${id}/gabarito/`)
    gabarito.value = res.data
    gabarito.value.questoes.forEach(q => { if (q.correta === false) questoesAbertas.value.push(q.ordem) })
    if (gabarito.value.simulado_id) {
      try {
        const ev = await api.get(`/api/resultados/evolucao/${gabarito.value.simulado_id}/`)
        evolucaoData.value = ev.data
      } catch {}
    }
  } catch {
    const acertos = parseInt(route.query.acertos)
    const total = parseInt(route.query.total)
    if (!isNaN(acertos)) {
      gabarito.value = {
        simulado_titulo: 'Simulação Processada', acertos: acertos || 0,
        total_questoes: total || 0, score: route.query.score?.replace('%', '') || '0',
        questoes: [], resumo_por_materia: [], temas_com_erro: [],
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
.page-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: var(--space-8); }
.page-title { font-family: var(--font-display); font-size: var(--text-2xl); font-weight: var(--weight-bold); color: var(--color-star); }
.page-sub { font-size: var(--text-sm); color: var(--color-comet); margin-top: var(--space-1); }

/* Skeleton */
.skeleton-stack { display: flex; flex-direction: column; gap: var(--space-6); }
.sk-hero { height: 160px; background: var(--color-nebula); border-radius: var(--radius-xl); position: relative; overflow: hidden; }
.sk-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-4); }
.sk-box { height: 120px; background: var(--color-nebula); border-radius: var(--radius-xl); position: relative; overflow: hidden; }
.sk-hero::after, .sk-box::after { content: ''; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent); animation: shimmer 1.5s infinite; }
@keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

/* Empty */
.empty-state { display: flex; flex-direction: column; align-items: center; text-align: center; padding: var(--space-14) var(--space-8); background: var(--color-nebula); border: 1px dashed var(--color-border); border-radius: var(--radius-xl); }
.empty-icon { font-size: 2.5rem; color: var(--color-orbit); margin-bottom: var(--space-5); }
.empty-icon.nova { color: var(--color-nova); }
.empty-title { font-family: var(--font-display); font-size: var(--text-lg); font-weight: var(--weight-bold); color: var(--color-star); margin-bottom: var(--space-2); }
.empty-sub { font-size: var(--text-sm); color: var(--color-comet); }
.mt-5 { margin-top: var(--space-5); }

/* Stack */
.resultado-stack { display: flex; flex-direction: column; gap: var(--space-6); }

/* Score hero */
.score-hero {
  background: var(--color-nebula);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-8) var(--space-8);
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: var(--space-6);
  flex-wrap: wrap;
}
.hero-left { display: flex; align-items: center; gap: var(--space-5); }
.hero-icon-wrap { width: 72px; height: 72px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem; flex-shrink: 0; }
.hero--stellar { background: rgba(0,214,143,0.1); color: var(--color-stellar); }
.hero--flare   { background: rgba(255,184,48,0.1); color: var(--color-flare); }
.hero--nova    { background: var(--color-nova-dim); color: var(--color-nova); }
.hero-title { font-family: var(--font-display); font-size: var(--text-2xl); font-weight: var(--weight-extrabold); color: var(--color-star); margin-bottom: var(--space-1); }
.hero-sub { font-size: var(--text-base); color: var(--color-comet); }

.metrics { display: flex; gap: var(--space-3); flex-wrap: wrap; }
.metric { background: rgba(255,255,255,0.03); border: 1px solid var(--color-border); padding: var(--space-4) var(--space-5); border-radius: var(--radius-md); display: flex; flex-direction: column; align-items: center; min-width: 90px; }
.metric-val { font-size: var(--text-3xl); font-weight: var(--weight-extrabold); line-height: 1.1; }
.metric-label { font-size: var(--text-2xs); font-family: var(--font-mono); color: var(--color-dust); text-transform: uppercase; letter-spacing: 0.08em; margin-top: var(--space-1); }
.stellar { color: var(--color-stellar); }
.nova    { color: var(--color-nova); }
.orbit   { color: var(--color-orbit); }
.flare   { color: var(--color-flare); }

/* Section cards */
.section-card {
  background: var(--color-nebula);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-7);
}
.section-card--orbit { border-color: rgba(0,229,255,0.15); }
.section-title { font-family: var(--font-display); font-size: var(--text-lg); font-weight: var(--weight-bold); color: var(--color-star); margin-bottom: var(--space-5); }
.no-mb { margin-bottom: 0; }

/* Subjects */
.subjects-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: var(--space-4); }
.subject-box { background: rgba(255,255,255,0.03); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--space-4); }
.subject-top { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-2); }
.subject-tag { background: rgba(124,110,255,0.1); color: var(--color-pulsar); padding: 2px var(--space-2); border-radius: var(--radius-sm); font-size: var(--text-2xs); font-family: var(--font-mono); font-weight: var(--weight-bold); }
.subject-score { font-weight: var(--weight-extrabold); font-size: var(--text-base); }
.subject-name { font-size: var(--text-xs); color: var(--color-comet); font-weight: var(--weight-medium); margin-bottom: var(--space-3); }
.progress-bar { height: 5px; background: rgba(255,255,255,0.08); border-radius: var(--radius-full); overflow: hidden; margin-bottom: var(--space-2); }
.progress-fill { height: 100%; border-radius: var(--radius-full); transition: width 0.6s ease; }
.bg-stellar { background: var(--color-stellar); }
.bg-flare   { background: var(--color-flare); }
.bg-nova    { background: var(--color-nova); }
.subject-detail { font-size: var(--text-2xs); color: var(--color-dust); }

/* Intel / Revisão */
.intel-header { margin-bottom: var(--space-6); }
.intel-badge { display: inline-block; background: rgba(0,229,255,0.08); border: 1px solid rgba(0,229,255,0.15); color: var(--color-orbit); font-size: var(--text-2xs); font-family: var(--font-mono); font-weight: var(--weight-bold); letter-spacing: 0.1em; text-transform: uppercase; padding: 3px var(--space-2); border-radius: var(--radius-sm); margin-bottom: var(--space-2); }
.intel-sub { font-size: var(--text-sm); color: var(--color-comet); margin-top: var(--space-2); }
.revision-list { display: flex; flex-direction: column; gap: var(--space-4); }
.revision-item { background: rgba(255,255,255,0.03); border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: hidden; }
.revision-header { background: rgba(255,255,255,0.02); padding: var(--space-4) var(--space-5); display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid var(--color-border); }
.revision-meta { display: flex; align-items: center; gap: var(--space-3); }
.rev-mat { background: var(--color-orbit); color: var(--color-cosmos); padding: 2px var(--space-2); border-radius: var(--radius-sm); font-size: var(--text-2xs); font-family: var(--font-mono); font-weight: var(--weight-bold); }
.rev-tema { font-weight: var(--weight-semibold); color: var(--color-star); font-size: var(--text-sm); }
.rev-erros { background: var(--color-nova-dim); border: 1px solid var(--color-nova-border); color: var(--color-nova); font-size: var(--text-xs); font-weight: var(--weight-bold); padding: 2px var(--space-2); border-radius: var(--radius-full); }
.materials { padding: var(--space-4) var(--space-5); display: flex; flex-direction: column; gap: var(--space-2); }
.material-link { display: flex; align-items: center; gap: var(--space-3); padding: var(--space-3) var(--space-4); background: rgba(255,255,255,0.03); border: 1px solid var(--color-border); border-radius: var(--radius-sm); text-decoration: none; color: var(--color-comet); transition: all var(--transition-fast); font-size: var(--text-sm); }
.material-link:hover { border-color: rgba(0,229,255,0.2); background: rgba(0,229,255,0.04); color: var(--color-star); }
.mat-title { flex: 1; font-weight: var(--weight-medium); }
.mat-action { font-size: var(--text-xs); font-weight: var(--weight-bold); color: var(--color-orbit); }
.revision-empty { padding: var(--space-4) var(--space-5); font-size: var(--text-sm); color: var(--color-dust); font-style: italic; }

/* Gabarito header */
.gabarito-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-6); flex-wrap: wrap; gap: var(--space-4); }
.filtros { display: flex; gap: var(--space-1); background: rgba(255,255,255,0.03); padding: 4px; border-radius: var(--radius-md); }
.filtro-btn { display: flex; align-items: center; gap: var(--space-2); padding: var(--space-2) var(--space-3); border: none; border-radius: var(--radius-sm); background: transparent; cursor: pointer; font-size: var(--text-xs); font-weight: var(--weight-semibold); color: var(--color-dust); transition: all var(--transition-fast); }
.filtro-btn--active { background: var(--color-nebula); color: var(--color-star); box-shadow: 0 1px 4px rgba(0,0,0,0.2); }
.filtro-count { background: rgba(255,255,255,0.08); padding: 2px 6px; border-radius: var(--radius-sm); font-size: var(--text-2xs); }
.filtro-btn--active .filtro-count { background: var(--color-orbit); color: var(--color-cosmos); }

.questoes-list { display: flex; flex-direction: column; gap: var(--space-3); }
.filter-empty { text-align: center; padding: var(--space-6); color: var(--color-dust); font-size: var(--text-sm); }

.q-item { background: var(--color-nebula); border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: hidden; border-left: 3px solid var(--color-border); }
.q-item--correct { border-left-color: var(--color-stellar); }
.q-item--wrong   { border-left-color: var(--color-nova); }
.q-item--null    { border-left-color: var(--color-dust); }

.q-header { display: flex; justify-content: space-between; align-items: center; padding: var(--space-4) var(--space-5); cursor: pointer; transition: background var(--transition-fast); gap: var(--space-4); }
.q-header:hover { background: rgba(255,255,255,0.02); }
.q-meta { display: flex; align-items: center; gap: var(--space-3); flex: 1; flex-wrap: wrap; }
.q-status { width: 24px; height: 24px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: var(--text-xs); font-weight: var(--weight-extrabold); flex-shrink: 0; }
.q-status--ok    { background: var(--color-stellar); color: white; }
.q-status--fail  { background: var(--color-nova); color: white; }
.q-status--blank { background: rgba(255,255,255,0.08); color: var(--color-dust); }
.q-num { font-weight: var(--weight-bold); color: var(--color-star); font-size: var(--text-sm); }
.q-tag { background: rgba(255,255,255,0.05); color: var(--color-dust); padding: 2px var(--space-2); border-radius: 3px; font-size: var(--text-2xs); font-weight: var(--weight-semibold); }
.q-tag--mat { background: rgba(124,110,255,0.1); color: var(--color-pulsar); }
.q-dif { padding: 2px var(--space-2); border-radius: 3px; font-size: var(--text-2xs); font-weight: var(--weight-bold); }
.q-dif--F { background: rgba(0,214,143,0.1); color: var(--color-stellar); }
.q-dif--M { background: rgba(255,184,48,0.1); color: var(--color-flare); }
.q-dif--D { background: var(--color-nova-dim); color: var(--color-nova); }
.q-compact { font-size: var(--text-sm); }
.text-stellar { color: var(--color-stellar); font-weight: var(--weight-medium); }
.text-nova { color: var(--color-nova); font-weight: var(--weight-medium); }
.text-dust { color: var(--color-dust); }
.q-toggle { color: var(--color-dust); font-size: var(--text-xs); }

.q-body { padding: var(--space-6); border-top: 1px solid var(--color-border); }
.q-texto { font-size: var(--text-base); color: var(--color-comet); line-height: var(--leading-relaxed); margin-bottom: var(--space-5); }
.q-img { max-width: 100%; border-radius: var(--radius-md); margin-bottom: var(--space-5); border: 1px solid var(--color-border); }

.opcoes-list { display: flex; flex-direction: column; gap: var(--space-2); margin-bottom: var(--space-6); }
.opcao-item { display: flex; align-items: center; gap: var(--space-4); padding: var(--space-3) var(--space-4); border: 1px solid var(--color-border); border-radius: var(--radius-sm); background: rgba(255,255,255,0.02); transition: all var(--transition-fast); }
.opcao-item--correct { border-color: var(--color-stellar-border); background: var(--color-stellar-dim); }
.opcao-item--wrong   { border-color: var(--color-nova-border); background: var(--color-nova-dim); }
.opcao-letra { width: 32px; height: 32px; background: rgba(255,255,255,0.06); border: 1px solid var(--color-border); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: var(--weight-extrabold); font-size: var(--text-sm); color: var(--color-dust); flex-shrink: 0; }
.opcao-item--correct .opcao-letra { background: var(--color-stellar); color: white; border-color: var(--color-stellar); }
.opcao-item--wrong .opcao-letra   { background: var(--color-nova); color: white; border-color: var(--color-nova); }
.opcao-texto { flex: 1; font-size: var(--text-sm); color: var(--color-comet); line-height: var(--leading-snug); }
.opcao-ind { display: flex; flex-direction: column; align-items: flex-end; gap: 2px; font-size: var(--text-2xs); font-weight: var(--weight-bold); text-transform: uppercase; }
.ind-ok   { color: var(--color-stellar); }
.ind-fail { color: var(--color-nova); }

.explicacao { background: rgba(0,229,255,0.04); border: 1px solid rgba(0,229,255,0.1); border-left: 3px solid var(--color-orbit); border-radius: var(--radius-sm); padding: var(--space-5); }
.exp-title { font-size: var(--text-xs); font-family: var(--font-mono); font-weight: var(--weight-bold); color: var(--color-orbit); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: var(--space-2); }
.exp-text { font-size: var(--text-sm); color: var(--color-comet); line-height: var(--leading-relaxed); margin: 0; }
.blank-warning { background: rgba(255,255,255,0.04); border: 1px solid var(--color-border); border-radius: var(--radius-sm); padding: var(--space-4); text-align: center; font-size: var(--text-sm); color: var(--color-dust); }

@media (max-width: 768px) {
  .score-hero { flex-direction: column; }
  .hero-left { flex-direction: column; text-align: center; }
  .metrics { justify-content: center; }
  .metric { min-width: 80px; }
  .sk-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>

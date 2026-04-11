<template>
  <div class="resultado-page">

    <nav class="navbar">
      <h1>Portal de Simulados</h1>
      <div class="nav-links">
        <router-link to="/simulados">Simulados</router-link>
        <router-link to="/ranking">Ranking</router-link>
        <button @click="logout" class="btn-logout">Sair</button>
      </div>
    </nav>

    <div v-if="carregando" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Carregando resultado...</p>
    </div>

    <div v-else-if="erro" class="erro-container">
      <p>{{ erro }}</p>
      <button @click="$router.push('/simulados')" class="btn-primario">
        Voltar para simulados
      </button>
    </div>

    <div v-else class="container">

      <div class="score-hero">
        <div class="hero-icone">
          {{ parseFloat(gabarito.score) >= 70 ? '🎉' : parseFloat(gabarito.score) >= 50 ? '📈' : '📚' }}
        </div>
        <h2 class="hero-titulo">
          {{ mensagemMotivacional }}
        </h2>
        <p class="hero-subtitulo">{{ gabarito.simulado_titulo }}</p>

        <div class="metricas">
          <div class="metrica-card">
            <span class="metrica-valor" :class="corScore(parseFloat(gabarito.score))">
              {{ gabarito.score }}%
            </span>
            <span class="metrica-label">Aproveitamento</span>
          </div>
          <div class="metrica-card">
            <span class="metrica-valor verde">{{ gabarito.acertos }}</span>
            <span class="metrica-label">Acertos</span>
          </div>
          <div class="metrica-card">
            <span class="metrica-valor vermelho">
              {{ gabarito.total_questoes - gabarito.acertos }}
            </span>
            <span class="metrica-label">Erros</span>
          </div>
          <div class="metrica-card">
            <span class="metrica-valor azul">{{ gabarito.total_questoes }}</span>
            <span class="metrica-label">Total</span>
          </div>
        </div>
      </div>

      <div
        v-if="gabarito.resumo_por_materia && gabarito.resumo_por_materia.length > 0"
        class="secao"
      >
        <h3 class="secao-titulo">Desempenho por matéria</h3>
        <div class="materias-grid">
          <div
            v-for="mat in gabarito.resumo_por_materia"
            :key="mat.materia"
            class="materia-card"
          >
            <div class="materia-topo">
              <span class="materia-badge">{{ mat.materia }}</span>
              <span class="materia-percentual" :class="corScore(mat.percentual)">
                {{ mat.percentual }}%
              </span>
            </div>
            <div class="materia-nome">{{ mat.nome || mat.materia }}</div>
            <div class="barra-progresso">
              <div
                class="barra-fill"
                :class="corScore(mat.percentual)"
                :style="{ width: mat.percentual + '%' }"
              ></div>
            </div>
            <div class="materia-detalhe">{{ mat.acertos }}/{{ mat.total }} questões</div>
          </div>
        </div>
      </div>

      <div
        v-if="gabarito.temas_com_erro && gabarito.temas_com_erro.length > 0"
        class="secao secao-revisao"
      >
        <h3 class="secao-titulo">
          📌 Trilha de Revisão Personalizada
        </h3>
        <p class="secao-subtitulo">
          Com base nos seus erros, separamos materiais específicos para você fortalecer sua base:
        </p>

        <div class="temas-recomendacao-grid">
          <div 
            v-for="tema in gabarito.temas_com_erro" 
            :key="tema.tema" 
            class="tema-rec-card"
          >
            <div class="tema-rec-header">
              <div class="tema-rec-info">
                <span class="tema-badge">{{ tema.materia }}</span>
                <span class="tema-nome">{{ tema.tema }}</span>
              </div>
              <span class="tema-erros">{{ tema.erros }} erro{{ tema.erros > 1 ? 's' : '' }}</span>
            </div>
            
            <div class="tema-materiais" v-if="tema.materiais_recomendados && tema.materiais_recomendados.length > 0">
              <p class="materiais-title">Conteúdo sugerido para revisão:</p>
              <a 
                v-for="(mat, i) in tema.materiais_recomendados" 
                :key="i"
                :href="mat.url"
                target="_blank"
                class="material-btn"
              >
                <span class="mat-icon">{{ getIconeMaterial(mat.tipo) }}</span>
                <span class="mat-nome">{{ mat.titulo }}</span>
                <span class="mat-acao">Acessar ↗</span>
              </a>
            </div>
            
            <div class="tema-materiais-vazio" v-else>
               Nenhum material de apoio associado a este tema no momento.
            </div>
          </div>
        </div>
      </div>

      <EvolucaoGrafico 
        v-if="evolucaoData && evolucaoData.length > 1" 
        :evolucao="evolucaoData" 
      />

      <div class="secao">
        <div class="gabarito-header">
          <h3 class="secao-titulo">Gabarito comentado</h3>

          <div class="filtros">
            <button
              v-for="f in filtros"
              :key="f.valor"
              @click="filtroAtivo = f.valor"
              class="btn-filtro"
              :class="{ ativo: filtroAtivo === f.valor }"
            >
              {{ f.label }}
              <span class="filtro-count">{{ contarFiltro(f.valor) }}</span>
            </button>
          </div>
        </div>

        <div class="questoes-lista">
          <div
            v-for="questao in questoesFiltradas"
            :key="questao.ordem"
            class="card-questao"
            :class="{
              'card-certa':       questao.correta === true,
              'card-errada':      questao.correta === false,
              'card-nao-respondida': questao.correta === null,
            }"
          >
            <div class="questao-header" @click="toggleQuestao(questao.ordem)">
              <div class="questao-meta">

                <div class="questao-status">
                  <span v-if="questao.correta === true"  class="status-icon certa">✓</span>
                  <span v-else-if="questao.correta === false" class="status-icon errada">✗</span>
                  <span v-else class="status-icon nao-respondida">—</span>
                </div>

                <span class="questao-numero">Questão {{ questao.ordem }}</span>

                <span v-if="questao.materia" class="tag-materia">{{ questao.materia }}</span>
                <span v-if="questao.tema" class="tag-tema">{{ questao.tema }}</span>

                <span class="tag-dificuldade" :class="'dif-' + questao.dificuldade">
                  {{ labelDificuldade(questao.dificuldade) }}
                </span>
              </div>

              <div class="questao-resumo-compacto" v-if="!questoesAbertas.includes(questao.ordem)">
                <span v-if="questao.correta === true" class="texto-certa">
                  Você acertou · {{ questao.opcao_escolhida }}
                </span>
                <span v-else-if="questao.correta === false" class="texto-errada">
                  Você: {{ questao.opcao_escolhida }} · Certa: {{ questao.resposta_correta }}
                </span>
                <span v-else class="texto-nao-respondida">Não respondida</span>
              </div>

              <span class="toggle-icon">
                {{ questoesAbertas.includes(questao.ordem) ? '▲' : '▼' }}
              </span>
            </div>

            <div v-if="questoesAbertas.includes(questao.ordem)" class="questao-corpo">
              <p class="enunciado">{{ questao.enunciado }}</p>

              <img
                v-if="questao.imagem_enunciado"
                :src="questao.imagem_enunciado"
                class="imagem-questao"
                alt="Imagem da questão"
              />

              <div class="alternativas">
                <div
                  v-for="opcao in opcoesDaQuestao(questao)"
                  :key="opcao.letra"
                  class="alternativa"
                  :class="classeAlternativa(opcao.letra, questao)"
                >
                  <span class="alternativa-letra">{{ opcao.letra }}</span>
                  <span class="alternativa-texto">{{ opcao.texto }}</span>

                  <div class="alternativa-indicadores">
                    <span
                      v-if="opcao.letra === questao.resposta_correta"
                      class="indicador-correto"
                    >
                      ✓ Correta
                    </span>
                    <span
                      v-if="opcao.letra === questao.opcao_escolhida && !questao.correta"
                      class="indicador-escolhida"
                    >
                      Sua resposta
                    </span>
                  </div>
                </div>
              </div>

              <div v-if="questao.explicacao" class="explicacao">
                <div class="explicacao-titulo">💡 Explicação</div>
                <p class="explicacao-texto">{{ questao.explicacao }}</p>
              </div>

              <div v-if="questao.correta === null" class="nao-respondida-aviso">
                Você não respondeu esta questão.
              </div>
            </div>
          </div>

          <div v-if="questoesFiltradas.length === 0" class="filtro-vazio">
            Nenhuma questão nesta categoria.
          </div>
        </div>
      </div>

      <div class="acoes-finais">
        <button @click="$router.push('/simulados')" class="btn-secundario">
          Ver outros simulados
        </button>
        <button @click="$router.push('/ranking')" class="btn-primario">
          Ver ranking 🏆
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
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
  { valor: 'todas',  label: 'Todas'  },
  { valor: 'certas', label: 'Certas' },
  { valor: 'erradas', label: 'Erradas' },
]

const questoesFiltradas = computed(() => {
  if (filtroAtivo.value === 'certas')  return gabarito.value.questoes.filter(q => q.correta === true)
  if (filtroAtivo.value === 'erradas') return gabarito.value.questoes.filter(q => q.correta === false)
  return gabarito.value.questoes
})

const mensagemMotivacional = computed(() => {
  const score = parseFloat(gabarito.value.score)
  if (score >= 90) return 'Excelente! Resultado incrível! 🏆'
  if (score >= 70) return 'Parabéns! Você foi muito bem!'
  if (score >= 50) return 'Bom resultado! Continue evoluindo!'
  return 'Continue praticando! Cada erro é uma lição.'
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
  if (letra === questao.resposta_correta) return 'alternativa-correta'
  if (letra === questao.opcao_escolhida && !questao.correta) return 'alternativa-errada'
  return ''
}

function corScore(valor) {
  if (valor >= 70) return 'verde'
  if (valor >= 50) return 'amarelo'
  return 'vermelho'
}

function labelDificuldade(dif) {
  const mapa = { F: 'Fácil', M: 'Médio', D: 'Difícil' }
  return mapa[dif] || dif
}

// Fase 7: Função para retornar um ícone baseado no tipo de material
function getIconeMaterial(tipo) {
  const icones = {
    VIDEO: '▶️',
    PDF: '📄',
    LINK: '🔗'
  }
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
    const response = await api.get(`/resultados/${id}/gabarito/`)
    gabarito.value = response.data

    gabarito.value.questoes.forEach(q => {
      if (q.correta === false) {
        questoesAbertas.value.push(q.ordem)
      }
    })

    if (gabarito.value.simulado_id) {
      try {
        const responseEvolucao = await api.get(`/resultados/evolucao/${gabarito.value.simulado_id}/`)
        evolucaoData.value = responseEvolucao.data
      } catch (err) {
        console.error("Erro ao carregar evolução do gráfico:", err)
      }
    }

  } catch (error) {
    const acertos = parseInt(route.query.acertos)
    const total   = parseInt(route.query.total)
    const score   = route.query.score?.replace('%', '') || '0'

    if (acertos !== undefined && total !== undefined) {
      gabarito.value = {
        simulado_titulo:    'Resultado do simulado',
        acertos:            acertos || 0,
        total_questoes:     total   || 0,
        score:              score,
        questoes:           [],
        resumo_por_materia: [],
        temas_com_erro:     [],
      }
    } else {
      erro.value = 'Não foi possível carregar o resultado. Tente novamente.'
    }
  } finally {
    carregando.value = false
  }
})
</script>

<style scoped>
/* ============================================
   Base
   ============================================ */
.resultado-page { min-height: 100vh; background: #f5f5f5; }

.navbar {
  background: #667eea; color: white; padding: 16px 32px;
  display: flex; justify-content: space-between; align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.navbar h1 { font-size: 20px; font-weight: 600; }
.nav-links { display: flex; align-items: center; gap: 24px; }
.nav-links a { color: white; text-decoration: none; font-size: 14px; opacity: 0.9; }
.btn-logout {
  background: rgba(255,255,255,0.2); color: white;
  border: 1px solid rgba(255,255,255,0.4); padding: 6px 16px;
  border-radius: 6px; cursor: pointer; font-size: 14px;
}

.container { max-width: 860px; margin: 0 auto; padding: 40px 20px 60px; }

.loading-container {
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  min-height: 60vh; gap: 16px; color: #999;
}
.loading-spinner {
  width: 40px; height: 40px; border: 3px solid #e5e7eb; border-top-color: #667eea;
  border-radius: 50%; animation: girar 0.8s linear infinite;
}
@keyframes girar { to { transform: rotate(360deg); } }

.erro-container {
  text-align: center; padding: 60px 20px; color: #666;
  display: flex; flex-direction: column; align-items: center; gap: 16px;
}

/* ============================================
   Score hero
   ============================================ */
.score-hero {
  background: white; border-radius: 16px; padding: 40px;
  text-align: center; box-shadow: 0 2px 16px rgba(0,0,0,0.08); margin-bottom: 24px;
}
.hero-icone { font-size: 56px; margin-bottom: 12px; }
.hero-titulo { font-size: 26px; color: #1f2937; font-weight: 700; margin-bottom: 6px; }
.hero-subtitulo { color: #6b7280; font-size: 15px; margin-bottom: 32px; }

.metricas { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
.metrica-card {
  background: #f9fafb; border-radius: 12px; padding: 20px 12px;
  display: flex; flex-direction: column; align-items: center; gap: 6px;
}
.metrica-valor { font-size: 32px; font-weight: 700; line-height: 1; }
.metrica-label { font-size: 12px; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.5px; }

/* ============================================
   Seções genéricas
   ============================================ */
.secao {
  background: white; border-radius: 16px; padding: 28px 32px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08); margin-bottom: 24px;
}
.secao-titulo {
  font-size: 17px; font-weight: 700; color: #1f2937; margin-bottom: 6px;
  display: flex; align-items: center; gap: 10px;
}
.secao-subtitulo { color: #6b7280; font-size: 13px; margin-bottom: 16px; }

/* ============================================
   Resumo por matéria
   ============================================ */
.materias-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr)); gap: 12px; margin-top: 16px; }
.materia-card { background: #f9fafb; border-radius: 10px; padding: 16px; }
.materia-topo { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.materia-badge { background: #667eea; color: white; padding: 2px 8px; border-radius: 99px; font-size: 11px; font-weight: 700; }
.materia-percentual { font-size: 18px; font-weight: 700; }
.materia-nome { font-size: 12px; color: #6b7280; margin-bottom: 8px; }
.barra-progresso { height: 6px; background: #e5e7eb; border-radius: 99px; overflow: hidden; margin-bottom: 6px; }
.barra-fill { height: 100%; border-radius: 99px; transition: width 0.6s ease; }
.materia-detalhe { font-size: 11px; color: #9ca3af; }

/* ============================================
   Trilha de Revisão (Fase 7)
   ============================================ */
.secao-revisao { border-left: 4px solid #8b5cf6; }

.temas-recomendacao-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 20px;
}

.tema-rec-card {
  border: 1px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
}

.tema-rec-header {
  background: #f9fafb;
  padding: 14px 18px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1px solid #e5e7eb;
}

.tema-rec-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.tema-badge {
  background: #8b5cf6;
  color: white;
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 11px;
  font-weight: 700;
}

.tema-nome {
  font-size: 15px;
  font-weight: 600;
  color: #1f2937;
}

.tema-erros {
  font-size: 12px;
  color: #ef4444;
  font-weight: 600;
  background: #fee2e2;
  padding: 2px 8px;
  border-radius: 99px;
}

.tema-materiais {
  padding: 16px 18px;
  background: white;
}

.materiais-title {
  font-size: 12px;
  text-transform: uppercase;
  color: #6b7280;
  font-weight: 600;
  margin-bottom: 12px;
  letter-spacing: 0.5px;
}

.material-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 8px;
  text-decoration: none;
  margin-bottom: 8px;
  transition: all 0.2s;
}

.material-btn:last-child {
  margin-bottom: 0;
}

.material-btn:hover {
  background: #dcfce7;
  border-color: #86efac;
  transform: translateY(-1px);
}

.mat-icon { font-size: 18px; }

.mat-nome {
  flex: 1;
  font-size: 14px;
  font-weight: 500;
  color: #166534;
}

.mat-acao {
  font-size: 12px;
  font-weight: 600;
  color: #15803d;
}

.tema-materiais-vazio {
  padding: 20px;
  text-align: center;
  font-size: 13px;
  color: #9ca3af;
  background: white;
  font-style: italic;
}

/* ============================================
   Gabarito: header com filtros
   ============================================ */
.gabarito-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; flex-wrap: wrap; gap: 12px; }
.filtros { display: flex; gap: 8px; }
.btn-filtro {
  display: flex; align-items: center; gap: 6px; padding: 6px 14px;
  border: 1px solid #e5e7eb; border-radius: 99px; background: white;
  cursor: pointer; font-size: 13px; color: #6b7280; transition: all 0.15s;
}
.btn-filtro:hover { border-color: #667eea; color: #667eea; }
.btn-filtro.ativo { background: #667eea; color: white; border-color: #667eea; }
.filtro-count { background: rgba(255,255,255,0.25); border-radius: 99px; padding: 0 6px; font-size: 11px; font-weight: 700; }
.btn-filtro:not(.ativo) .filtro-count { background: #f3f4f6; color: #6b7280; }

/* ============================================
   Cards de questão
   ============================================ */
.questoes-lista { display: flex; flex-direction: column; gap: 10px; }
.card-questao { border: 2px solid #e5e7eb; border-radius: 12px; overflow: hidden; transition: border-color 0.2s; }
.card-certa  { border-left: 4px solid #22c55e; }
.card-errada { border-left: 4px solid #ef4444; }
.card-nao-respondida { border-left: 4px solid #9ca3af; }

.questao-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 18px; cursor: pointer; background: #fafafa; transition: background 0.15s; gap: 12px;
}
.questao-header:hover { background: #f3f4f6; }
.questao-meta { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; flex: 1; }
.status-icon {
  width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center;
  justify-content: center; font-size: 13px; font-weight: 700; flex-shrink: 0;
}
.status-icon.certa  { background: #dcfce7; color: #16a34a; }
.status-icon.errada { background: #fee2e2; color: #dc2626; }
.status-icon.nao-respondida { background: #f3f4f6; color: #9ca3af; }

.questao-numero { font-size: 14px; font-weight: 600; color: #374151; }
.tag-materia { background: #e0e7ff; color: #4338ca; padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; }
.tag-tema { background: #f3f4f6; color: #6b7280; padding: 2px 8px; border-radius: 4px; font-size: 11px; }
.tag-dificuldade { padding: 2px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }
.dif-F { background: #dcfce7; color: #15803d; }
.dif-M { background: #fef3c7; color: #b45309; }
.dif-D { background: #fee2e2; color: #b91c1c; }

.questao-resumo-compacto { font-size: 13px; flex-shrink: 0; }
.texto-certa  { color: #16a34a; font-weight: 500; }
.texto-errada { color: #dc2626; font-weight: 500; }
.texto-nao-respondida { color: #9ca3af; }
.toggle-icon { color: #9ca3af; font-size: 12px; flex-shrink: 0; }

.questao-corpo { padding: 20px 24px; border-top: 1px solid #f0f0f0; background: white; }
.enunciado { font-size: 15px; color: #374151; line-height: 1.7; margin-bottom: 20px; }
.imagem-questao { width: 100%; border-radius: 8px; margin-bottom: 16px; }

/* ============================================
   Alternativas com estado visual
   ============================================ */
.alternativas { display: flex; flex-direction: column; gap: 8px; margin-bottom: 20px; }
.alternativa {
  display: flex; align-items: center; gap: 12px; padding: 12px 16px;
  border: 1.5px solid #e5e7eb; border-radius: 8px; font-size: 14px;
  color: #374151; transition: all 0.15s;
}
.alternativa-correta { border-color: #22c55e; background: #f0fdf4; }
.alternativa-errada { border-color: #ef4444; background: #fef2f2; }
.alternativa-letra {
  width: 30px; height: 30px; border-radius: 50%; background: #f3f4f6;
  display: flex; align-items: center; justify-content: center; font-weight: 700;
  font-size: 13px; flex-shrink: 0;
}
.alternativa-correta .alternativa-letra { background: #22c55e; color: white; }
.alternativa-errada .alternativa-letra { background: #ef4444; color: white; }
.alternativa-texto { flex: 1; line-height: 1.5; }
.alternativa-indicadores {
  display: flex; flex-direction: column; gap: 2px; font-size: 11px;
  font-weight: 600; text-align: right; flex-shrink: 0;
}
.indicador-correto { color: #16a34a; }
.indicador-escolhida { color: #dc2626; }

/* ============================================
   Explicação
   ============================================ */
.explicacao { background: #f0f9ff; border: 1px solid #bae6fd; border-radius: 10px; padding: 16px 20px; }
.explicacao-titulo { font-size: 13px; font-weight: 700; color: #0369a1; margin-bottom: 8px; }
.explicacao-texto { font-size: 14px; color: #374151; line-height: 1.7; }
.nao-respondida-aviso { text-align: center; color: #9ca3af; font-size: 14px; padding: 16px; background: #f9fafb; border-radius: 8px; }
.filtro-vazio { text-align: center; color: #9ca3af; padding: 32px; }

/* ============================================
   Ações finais
   ============================================ */
.acoes-finais { display: flex; gap: 12px; justify-content: center; margin-top: 8px; }
.btn-primario, .btn-secundario {
  padding: 12px 28px; border-radius: 8px; border: none; cursor: pointer;
  font-size: 15px; font-weight: 500; transition: all 0.2s;
}
.btn-primario { background: #667eea; color: white; }
.btn-primario:hover { background: #5a6fd6; }
.btn-secundario { background: #f3f4f6; color: #374151; }
.btn-secundario:hover { background: #e5e7eb; }

/* ============================================
   Cores de score & Responsivo
   ============================================ */
.verde   { color: #22c55e; }
.amarelo { color: #f59e0b; }
.vermelho { color: #ef4444; }
.azul    { color: #667eea; }

@media (max-width: 640px) {
  .metricas { grid-template-columns: repeat(2, 1fr); }
  .materias-grid { grid-template-columns: repeat(2, 1fr); }
  .gabarito-header { flex-direction: column; align-items: flex-start; }
  .questao-resumo-compacto { display: none; }
  .navbar { flex-direction: column; gap: 12px; padding: 16px; }
}
</style>
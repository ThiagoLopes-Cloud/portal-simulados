<template>
  <div class="resultado-page">

    <!-- Navbar -->
    <nav class="navbar">
      <h1>Portal de Simulados</h1>
      <div class="nav-links">
        <router-link to="/simulados">Simulados</router-link>
        <router-link to="/ranking">Ranking</router-link>
        <button @click="logout" class="btn-logout">Sair</button>
      </div>
    </nav>

    <!-- Estado de carregamento -->
    <div v-if="carregando" class="loading-container">
      <div class="loading-spinner"></div>
      <p>Carregando resultado...</p>
    </div>

    <!-- Estado de erro -->
    <div v-else-if="erro" class="erro-container">
      <p>{{ erro }}</p>
      <button @click="$router.push('/simulados')" class="btn-primario">
        Voltar para simulados
      </button>
    </div>

    <!-- Conteúdo principal -->
    <div v-else class="container">

      <!-- ================================================
           SEÇÃO 1: Score hero — visão imediata do resultado
           ================================================ -->
      <div class="score-hero">

        <!-- Ícone e mensagem motivacional -->
        <div class="hero-icone">
          {{ parseFloat(gabarito.score) >= 70 ? '🎉' : parseFloat(gabarito.score) >= 50 ? '📈' : '📚' }}
        </div>
        <h2 class="hero-titulo">
          {{ mensagemMotivacional }}
        </h2>
        <p class="hero-subtitulo">{{ gabarito.simulado_titulo }}</p>

        <!-- Cards de métricas principais -->
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

      <!-- ================================================
           SEÇÃO 2: Resumo por matéria (base Fase 7)
           Só aparece se houver questões com tema vinculado
           ================================================ -->
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

      <!-- ================================================
           SEÇÃO 3: Temas para revisar (base Fase 7)
           Só aparece se houver erros com tema vinculado
           ================================================ -->
      <div
        v-if="gabarito.temas_com_erro && gabarito.temas_com_erro.length > 0"
        class="secao secao-revisao"
      >
        <h3 class="secao-titulo">
          📌 Temas para revisar
          <span class="badge-novo">Recomendação</span>
        </h3>
        <p class="secao-subtitulo">
          Com base nos seus erros, estes são os temas que mais precisam de atenção:
        </p>
        <div class="temas-revisao">
          <div
            v-for="tema in gabarito.temas_com_erro"
            :key="tema.tema"
            class="tema-tag"
          >
            <span class="tema-badge">{{ tema.materia }}</span>
            <span class="tema-nome">{{ tema.tema }}</span>
            <span class="tema-erros">{{ tema.erros }} erro{{ tema.erros > 1 ? 's' : '' }}</span>
          </div>
        </div>

        <!-- Placeholder para Fase 7 — recomendação de conteúdo -->
        <div class="fase7-placeholder">
          🚀 Em breve: materiais de estudo personalizados para cada tema
        </div>
      </div>

      <!-- ================================================
           SEÇÃO 4: Gabarito comentado — questão a questão
           ================================================ -->
      <div class="secao">
        <div class="gabarito-header">
          <h3 class="secao-titulo">Gabarito comentado</h3>

          <!-- Filtros de visualização -->
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

        <!-- Lista de questões filtrada -->
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
            <!-- Cabeçalho da questão -->
            <div class="questao-header" @click="toggleQuestao(questao.ordem)">
              <div class="questao-meta">

                <!-- Indicador visual de acerto/erro -->
                <div class="questao-status">
                  <span v-if="questao.correta === true"  class="status-icon certa">✓</span>
                  <span v-else-if="questao.correta === false" class="status-icon errada">✗</span>
                  <span v-else class="status-icon nao-respondida">—</span>
                </div>

                <span class="questao-numero">Questão {{ questao.ordem }}</span>

                <!-- Tags de matéria e tema -->
                <span v-if="questao.materia" class="tag-materia">{{ questao.materia }}</span>
                <span v-if="questao.tema" class="tag-tema">{{ questao.tema }}</span>

                <!-- Badge de dificuldade -->
                <span class="tag-dificuldade" :class="'dif-' + questao.dificuldade">
                  {{ labelDificuldade(questao.dificuldade) }}
                </span>
              </div>

              <!-- Resumo compacto da resposta (visível quando fechado) -->
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

            <!-- Corpo expandido da questão -->
            <div v-if="questoesAbertas.includes(questao.ordem)" class="questao-corpo">

              <!-- Enunciado -->
              <p class="enunciado">{{ questao.enunciado }}</p>

              <!-- Imagem do enunciado se existir -->
              <img
                v-if="questao.imagem_enunciado"
                :src="questao.imagem_enunciado"
                class="imagem-questao"
                alt="Imagem da questão"
              />

              <!-- Alternativas com marcação visual -->
              <div class="alternativas">
                <div
                  v-for="opcao in opcoesDaQuestao(questao)"
                  :key="opcao.letra"
                  class="alternativa"
                  :class="classeAlternativa(opcao.letra, questao)"
                >
                  <span class="alternativa-letra">{{ opcao.letra }}</span>
                  <span class="alternativa-texto">{{ opcao.texto }}</span>

                  <!-- Indicadores à direita da alternativa -->
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

              <!-- Explicação do gabarito -->
              <div v-if="questao.explicacao" class="explicacao">
                <div class="explicacao-titulo">💡 Explicação</div>
                <p class="explicacao-texto">{{ questao.explicacao }}</p>
              </div>

              <!-- Mensagem se não respondeu -->
              <div v-if="questao.correta === null" class="nao-respondida-aviso">
                Você não respondeu esta questão.
              </div>

            </div>
          </div>

          <!-- Mensagem quando nenhuma questão corresponde ao filtro -->
          <div v-if="questoesFiltradas.length === 0" class="filtro-vazio">
            Nenhuma questão nesta categoria.
          </div>
        </div>
      </div>

      <!-- ================================================
           SEÇÃO 5: Ações finais
           ================================================ -->
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
// Importa as funções reativas do Vue
import { ref, computed, onMounted } from 'vue'

// Importa o router e a rota atual
import { useRouter, useRoute } from 'vue-router'

// Importa o serviço de API
import api from '../services/api.js'

const router = useRouter()
const route  = useRoute()

// ==========================================
// Estado reativo
// ==========================================

const carregando = ref(true)
const erro       = ref('')

// Dados completos do gabarito retornados pela API
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

// Questões com o corpo expandido
// Por padrão abre as questões erradas automaticamente
const questoesAbertas = ref([])

// Filtro ativo: 'todas' | 'certas' | 'erradas'
const filtroAtivo = ref('todas')

// Definição dos botões de filtro
const filtros = [
  { valor: 'todas',  label: 'Todas'  },
  { valor: 'certas', label: 'Certas' },
  { valor: 'erradas', label: 'Erradas' },
]

// ==========================================
// Computed
// ==========================================

// Filtra as questões conforme o filtro ativo
const questoesFiltradas = computed(() => {
  if (filtroAtivo.value === 'certas')  return gabarito.value.questoes.filter(q => q.correta === true)
  if (filtroAtivo.value === 'erradas') return gabarito.value.questoes.filter(q => q.correta === false)
  return gabarito.value.questoes
})

// Mensagem motivacional baseada no score
const mensagemMotivacional = computed(() => {
  const score = parseFloat(gabarito.value.score)
  if (score >= 90) return 'Excelente! Resultado incrível! 🏆'
  if (score >= 70) return 'Parabéns! Você foi muito bem!'
  if (score >= 50) return 'Bom resultado! Continue evoluindo!'
  return 'Continue praticando! Cada erro é uma lição.'
})

// ==========================================
// Funções auxiliares
// ==========================================

// Conta quantas questões correspondem a cada filtro
function contarFiltro(valor) {
  if (valor === 'certas')  return gabarito.value.questoes.filter(q => q.correta === true).length
  if (valor === 'erradas') return gabarito.value.questoes.filter(q => q.correta === false).length
  return gabarito.value.questoes.length
}

// Abre/fecha o corpo de uma questão
function toggleQuestao(ordem) {
  const index = questoesAbertas.value.indexOf(ordem)
  if (index === -1) {
    questoesAbertas.value.push(ordem)
  } else {
    questoesAbertas.value.splice(index, 1)
  }
}

// Retorna apenas as alternativas com texto preenchido
function opcoesDaQuestao(questao) {
  return [
    { letra: 'A', texto: questao.opcao_a },
    { letra: 'B', texto: questao.opcao_b },
    { letra: 'C', texto: questao.opcao_c },
    { letra: 'D', texto: questao.opcao_d },
    { letra: 'E', texto: questao.opcao_e },
  ].filter(op => op.texto && op.texto.trim() !== '')
}

// Retorna a classe CSS de uma alternativa baseada no estado
function classeAlternativa(letra, questao) {
  if (letra === questao.resposta_correta) return 'alternativa-correta'
  if (letra === questao.opcao_escolhida && !questao.correta) return 'alternativa-errada'
  return ''
}

// Retorna a classe de cor baseada no score/percentual
function corScore(valor) {
  if (valor >= 70) return 'verde'
  if (valor >= 50) return 'amarelo'
  return 'vermelho'
}

// Retorna o label de dificuldade
function labelDificuldade(dif) {
  const mapa = { F: 'Fácil', M: 'Médio', D: 'Difícil' }
  return mapa[dif] || dif
}

// Logout
function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_role')
  router.push({ name: 'login' })
}

// ==========================================
// Inicialização
// ==========================================

onMounted(async () => {
  try {
    // Pega o ID do resultado da URL (/resultado/:id)
    const id = route.params.id

    // Busca o gabarito completo via nova API
    const response = await api.get(`/resultados/${id}/gabarito/`)
    gabarito.value = response.data

    // Abre automaticamente as questões erradas
    // O aluno vai querer ver primeiro onde errou
    gabarito.value.questoes.forEach(q => {
      if (q.correta === false) {
        questoesAbertas.value.push(q.ordem)
      }
    })

  } catch (error) {
    // Se o gabarito não carregar, tenta usar os query params como fallback
    // (compatibilidade com a ProvaPage atual que ainda envia query params)
    const acertos = parseInt(route.query.acertos)
    const total   = parseInt(route.query.total)
    const score   = route.query.score?.replace('%', '') || '0'

    if (acertos !== undefined && total !== undefined) {
      // Monta um gabarito mínimo com os dados dos query params
      // Não tem as questões — só o score
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
.resultado-page {
  min-height: 100vh;
  background: #f5f5f5;
}

.navbar {
  background: #667eea;
  color: white;
  padding: 16px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.navbar h1 { font-size: 20px; font-weight: 600; }
.nav-links { display: flex; align-items: center; gap: 24px; }
.nav-links a { color: white; text-decoration: none; font-size: 14px; opacity: 0.9; }
.btn-logout {
  background: rgba(255,255,255,0.2);
  color: white;
  border: 1px solid rgba(255,255,255,0.4);
  padding: 6px 16px; border-radius: 6px; cursor: pointer; font-size: 14px;
}

.container {
  max-width: 860px;
  margin: 0 auto;
  padding: 40px 20px 60px;
}

/* Loading */
.loading-container {
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  min-height: 60vh; gap: 16px; color: #999;
}
.loading-spinner {
  width: 40px; height: 40px;
  border: 3px solid #e5e7eb;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: girar 0.8s linear infinite;
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
  background: white;
  border-radius: 16px;
  padding: 40px;
  text-align: center;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
  margin-bottom: 24px;
}

.hero-icone { font-size: 56px; margin-bottom: 12px; }

.hero-titulo {
  font-size: 26px;
  color: #1f2937;
  font-weight: 700;
  margin-bottom: 6px;
}

.hero-subtitulo {
  color: #6b7280;
  font-size: 15px;
  margin-bottom: 32px;
}

.metricas {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.metrica-card {
  background: #f9fafb;
  border-radius: 12px;
  padding: 20px 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.metrica-valor {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
}

.metrica-label {
  font-size: 12px;
  color: #9ca3af;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* ============================================
   Seções genéricas
   ============================================ */
.secao {
  background: white;
  border-radius: 16px;
  padding: 28px 32px;
  box-shadow: 0 2px 16px rgba(0,0,0,0.08);
  margin-bottom: 24px;
}

.secao-titulo {
  font-size: 17px;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.secao-subtitulo {
  color: #6b7280;
  font-size: 13px;
  margin-bottom: 16px;
}

/* ============================================
   Resumo por matéria
   ============================================ */
.materias-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 12px;
  margin-top: 16px;
}

.materia-card {
  background: #f9fafb;
  border-radius: 10px;
  padding: 16px;
}

.materia-topo {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.materia-badge {
  background: #667eea;
  color: white;
  padding: 2px 8px;
  border-radius: 99px;
  font-size: 11px;
  font-weight: 700;
}

.materia-percentual {
  font-size: 18px;
  font-weight: 700;
}

.materia-nome {
  font-size: 12px;
  color: #6b7280;
  margin-bottom: 8px;
}

.barra-progresso {
  height: 6px;
  background: #e5e7eb;
  border-radius: 99px;
  overflow: hidden;
  margin-bottom: 6px;
}

.barra-fill {
  height: 100%;
  border-radius: 99px;
  transition: width 0.6s ease;
}

.materia-detalhe {
  font-size: 11px;
  color: #9ca3af;
}

/* ============================================
   Temas para revisar
   ============================================ */
.secao-revisao {
  border-left: 4px solid #f59e0b;
}

.badge-novo {
  background: #fef3c7;
  color: #92400e;
  font-size: 11px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 99px;
}

.temas-revisao {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 16px;
  margin-bottom: 16px;
}

.tema-tag {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 8px;
  padding: 8px 14px;
}

.tema-badge {
  background: #f59e0b;
  color: white;
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 10px;
  font-weight: 700;
}

.tema-nome {
  font-size: 13px;
  color: #1f2937;
  font-weight: 500;
}

.tema-erros {
  font-size: 11px;
  color: #ef4444;
  font-weight: 600;
}

/* Placeholder para Fase 7 */
.fase7-placeholder {
  background: #f0f3ff;
  border: 1px dashed #c7d2fe;
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 13px;
  color: #6366f1;
  text-align: center;
}

/* ============================================
   Gabarito: header com filtros
   ============================================ */
.gabarito-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.filtros {
  display: flex;
  gap: 8px;
}

.btn-filtro {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 99px;
  background: white;
  cursor: pointer;
  font-size: 13px;
  color: #6b7280;
  transition: all 0.15s;
}

.btn-filtro:hover { border-color: #667eea; color: #667eea; }

.btn-filtro.ativo {
  background: #667eea;
  color: white;
  border-color: #667eea;
}

.filtro-count {
  background: rgba(255,255,255,0.25);
  border-radius: 99px;
  padding: 0 6px;
  font-size: 11px;
  font-weight: 700;
}

.btn-filtro:not(.ativo) .filtro-count {
  background: #f3f4f6;
  color: #6b7280;
}

/* ============================================
   Cards de questão
   ============================================ */
.questoes-lista {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.card-questao {
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  overflow: hidden;
  transition: border-color 0.2s;
}

/* Borda colorida baseada no resultado */
.card-certa  { border-left: 4px solid #22c55e; }
.card-errada { border-left: 4px solid #ef4444; }
.card-nao-respondida { border-left: 4px solid #9ca3af; }

/* Cabeçalho clicável da questão */
.questao-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 18px;
  cursor: pointer;
  background: #fafafa;
  transition: background 0.15s;
  gap: 12px;
}

.questao-header:hover { background: #f3f4f6; }

.questao-meta {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  flex: 1;
}

/* Ícone de status (✓ / ✗ / —) */
.status-icon {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
  font-weight: 700;
  flex-shrink: 0;
}
.status-icon.certa  { background: #dcfce7; color: #16a34a; }
.status-icon.errada { background: #fee2e2; color: #dc2626; }
.status-icon.nao-respondida { background: #f3f4f6; color: #9ca3af; }

.questao-numero {
  font-size: 14px;
  font-weight: 600;
  color: #374151;
}

/* Tags */
.tag-materia {
  background: #e0e7ff;
  color: #4338ca;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 700;
}

.tag-tema {
  background: #f3f4f6;
  color: #6b7280;
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
}

.tag-dificuldade {
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 11px;
  font-weight: 600;
}
.dif-F { background: #dcfce7; color: #15803d; }
.dif-M { background: #fef3c7; color: #b45309; }
.dif-D { background: #fee2e2; color: #b91c1c; }

/* Resumo compacto quando fechado */
.questao-resumo-compacto {
  font-size: 13px;
  flex-shrink: 0;
}
.texto-certa  { color: #16a34a; font-weight: 500; }
.texto-errada { color: #dc2626; font-weight: 500; }
.texto-nao-respondida { color: #9ca3af; }

.toggle-icon { color: #9ca3af; font-size: 12px; flex-shrink: 0; }

/* Corpo expandido da questão */
.questao-corpo {
  padding: 20px 24px;
  border-top: 1px solid #f0f0f0;
  background: white;
}

.enunciado {
  font-size: 15px;
  color: #374151;
  line-height: 1.7;
  margin-bottom: 20px;
}

.imagem-questao {
  width: 100%;
  border-radius: 8px;
  margin-bottom: 16px;
}

/* ============================================
   Alternativas com estado visual
   ============================================ */
.alternativas {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.alternativa {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 16px;
  border: 1.5px solid #e5e7eb;
  border-radius: 8px;
  font-size: 14px;
  color: #374151;
  transition: all 0.15s;
}

/* Verde — alternativa correta */
.alternativa-correta {
  border-color: #22c55e;
  background: #f0fdf4;
}

/* Vermelho — alternativa escolhida pelo aluno e errada */
.alternativa-errada {
  border-color: #ef4444;
  background: #fef2f2;
}

.alternativa-letra {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #f3f4f6;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 13px;
  flex-shrink: 0;
}

.alternativa-correta .alternativa-letra {
  background: #22c55e;
  color: white;
}

.alternativa-errada .alternativa-letra {
  background: #ef4444;
  color: white;
}

.alternativa-texto { flex: 1; line-height: 1.5; }

.alternativa-indicadores {
  display: flex;
  flex-direction: column;
  gap: 2px;
  font-size: 11px;
  font-weight: 600;
  text-align: right;
  flex-shrink: 0;
}

.indicador-correto { color: #16a34a; }
.indicador-escolhida { color: #dc2626; }

/* ============================================
   Explicação
   ============================================ */
.explicacao {
  background: #f0f9ff;
  border: 1px solid #bae6fd;
  border-radius: 10px;
  padding: 16px 20px;
}

.explicacao-titulo {
  font-size: 13px;
  font-weight: 700;
  color: #0369a1;
  margin-bottom: 8px;
}

.explicacao-texto {
  font-size: 14px;
  color: #374151;
  line-height: 1.7;
}

.nao-respondida-aviso {
  text-align: center;
  color: #9ca3af;
  font-size: 14px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
}

.filtro-vazio {
  text-align: center;
  color: #9ca3af;
  padding: 32px;
}

/* ============================================
   Ações finais
   ============================================ */
.acoes-finais {
  display: flex;
  gap: 12px;
  justify-content: center;
  margin-top: 8px;
}

.btn-primario, .btn-secundario {
  padding: 12px 28px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-primario { background: #667eea; color: white; }
.btn-primario:hover { background: #5a6fd6; }

.btn-secundario { background: #f3f4f6; color: #374151; }
.btn-secundario:hover { background: #e5e7eb; }

/* ============================================
   Cores de score
   ============================================ */
.verde   { color: #22c55e; }
.amarelo { color: #f59e0b; }
.vermelho { color: #ef4444; }
.azul    { color: #667eea; }

/* ============================================
   Responsivo
   ============================================ */
@media (max-width: 640px) {
  .metricas { grid-template-columns: repeat(2, 1fr); }
  .materias-grid { grid-template-columns: repeat(2, 1fr); }
  .gabarito-header { flex-direction: column; align-items: flex-start; }
  .questao-resumo-compacto { display: none; }
  .navbar { flex-direction: column; gap: 12px; padding: 16px; }
}
</style>
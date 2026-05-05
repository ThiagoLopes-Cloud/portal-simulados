<template>
  <div class="prova-layout">

    <!-- Modal de confirmação de saída -->
    <div v-if="mostrarConfirmacaoSaida" class="exit-overlay">
      <div class="exit-modal">
        <div class="exit-icon">⚠</div>
        <h3 class="exit-title">Abandonar Missão?</h3>
        <p class="exit-sub">Seus dados de performance serão perdidos. Você terá que recomeçar do zero.</p>
        <div class="exit-actions">
          <button class="btn-retomar" @click="mostrarConfirmacaoSaida = false">Retomar Foco</button>
          <button class="btn-abortar" @click="confirmarSaida">Abortar</button>
        </div>
      </div>
    </div>

    <!-- Barra de foco -->
    <nav class="focus-bar">
      <div class="focus-logo">
        <span class="logo-orbit">SIMUS</span><span class="logo-star">LAB</span>
      </div>

      <div class="focus-progress">
        <span class="progress-label">
          Progresso: {{ questaoAtual + 1 }} / {{ simulado?.questoes?.length || 0 }}
        </span>
        <div class="progress-track">
          <div class="progress-fill"
               :style="{ width: ((questaoAtual + 1) / (simulado?.questoes?.length || 1) * 100) + '%' }" />
        </div>
      </div>

      <button class="btn-sair" @click="mostrarConfirmacaoSaida = true">Sair</button>
    </nav>

    <!-- Loading -->
    <div v-if="carregando" class="state-center">
      <div class="load-card skeleton" />
      <p class="state-text">Decodificando ambiente de prova...</p>
    </div>

    <!-- Erro -->
    <div v-else-if="erro" class="state-center">
      <div class="error-icon">⚠</div>
      <p class="state-text">{{ erro }}</p>
      <button class="btn-voltar" @click="$router.push('/simulados')">Retornar à Base</button>
    </div>

    <!-- Questão -->
    <div v-else class="prova-content">

      <header class="questao-header">
        <h2 class="simulado-titulo">{{ simulado.titulo }}</h2>
        <div v-if="simulado.questoes[questaoAtual]" class="questao-tags">
          <span class="tag tag--pulsar">{{ simulado.questoes[questaoAtual].materia || 'Questão' }}</span>
          <span class="tag">
            {{ { F: 'Básica', M: 'Intermediária', D: 'Avançada' }[simulado.questoes[questaoAtual].dificuldade] || '' }}
          </span>
        </div>
      </header>

      <div v-if="simulado.questoes[questaoAtual]" class="questao-card">
        <div class="questao-body">
          <p class="questao-num">Q. {{ questaoAtual + 1 }}</p>
          <p class="questao-texto">{{ simulado.questoes[questaoAtual].enunciado }}</p>
        </div>

        <img v-if="simulado.questoes[questaoAtual].imagem_enunciado"
             :src="simulado.questoes[questaoAtual].imagem_enunciado"
             class="questao-img" alt="Material de apoio" />

        <div class="opcoes">
          <div v-for="opcao in opcoesDaQuestao(simulado.questoes[questaoAtual])" :key="opcao.letra"
               class="opcao"
               :class="respostas[simulado.questoes[questaoAtual].id] === opcao.letra ? 'opcao--selected' : ''"
               @click="selecionar(simulado.questoes[questaoAtual].id, opcao.letra)">
            <div class="opcao-letra"
                 :class="respostas[simulado.questoes[questaoAtual].id] === opcao.letra ? 'opcao-letra--selected' : ''">
              {{ opcao.letra }}
            </div>
            <span class="opcao-texto">{{ opcao.texto }}</span>
          </div>
        </div>
      </div>

      <!-- Controles -->
      <div class="controles">
        <div class="controles-status">
          <span class="status-dot"
                :class="totalRespondidas === simulado.questoes.length ? 'status-dot--done' : ''" />
          {{ totalRespondidas }} de {{ simulado.questoes.length }} mapeadas
        </div>

        <div class="controles-btns">
          <button class="btn-anterior" @click="anterior" :disabled="questaoAtual === 0">Anterior</button>

          <button v-if="questaoAtual < simulado.questoes.length - 1"
                  class="btn-proxima" @click="proxima">
            Avançar
          </button>

          <button v-else class="btn-finalizar"
                  @click="enviar"
                  :disabled="enviando || totalRespondidas < simulado.questoes.length">
            <span v-if="enviando" class="spinner" />
            {{ enviando ? 'Compilando...' : 'Finalizar Simulação' }}
          </button>
        </div>
      </div>

      <div v-if="questaoAtual === simulado.questoes.length - 1 && totalRespondidas < simulado.questoes.length"
           class="alerta alerta--flare">
        ⚠ Existem {{ simulado.questoes.length - totalRespondidas }} questões sem resposta.
      </div>

      <div v-if="erroEnvio" class="alerta alerta--nova">{{ erroEnvio }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../services/api.js'

const router = useRouter()
const route = useRoute()
const simulado = ref(null)
const carregando = ref(true)
const erro = ref('')
const erroEnvio = ref('')
const enviando = ref(false)
const questaoAtual = ref(0)
const respostas = ref({})
const mostrarConfirmacaoSaida = ref(false)
const totalRespondidas = computed(() => Object.keys(respostas.value).length)

onMounted(async () => {
  try {
    const id = route.params.id
    const response = await api.get(`/api/simulados/${id}/`)
    simulado.value = response.data
  } catch {
    erro.value = 'Falha de comunicação com o servidor de provas.'
  } finally {
    carregando.value = false
  }
})

function opcoesDaQuestao(questao) {
  return [
    { letra: 'A', texto: questao.opcao_a },
    { letra: 'B', texto: questao.opcao_b },
    { letra: 'C', texto: questao.opcao_c },
    { letra: 'D', texto: questao.opcao_d },
    { letra: 'E', texto: questao.opcao_e },
  ].filter(o => o.texto && o.texto.trim() !== '')
}

function selecionar(questaoId, opcao) { respostas.value[questaoId] = opcao }
function proxima() { if (questaoAtual.value < simulado.value.questoes.length - 1) questaoAtual.value++ }
function anterior() { if (questaoAtual.value > 0) questaoAtual.value-- }
function confirmarSaida() { router.push({ name: 'simulados' }) }

async function enviar() {
  erroEnvio.value = ''
  enviando.value = true
  try {
    const listaRespostas = Object.entries(respostas.value).map(([questaoId, opcao]) => ({
      questao_id: parseInt(questaoId),
      opcao_escolhida: opcao,
    }))
    const response = await api.post('/api/responder/', {
      simulado_id: parseInt(route.params.id),
      respostas: listaRespostas,
    })
    router.push({ name: 'resultado', params: { id: response.data.resultado.resultado_id } })
  } catch (error) {
    erroEnvio.value = error.response?.data?.error || 'Falha na transmissão. Tente novamente.'
  } finally {
    enviando.value = false
  }
}
</script>

<style scoped>
.prova-layout {
  min-height: 100vh;
  background: var(--color-cosmos);
  font-family: var(--font-body);
  display: flex;
  flex-direction: column;
}

/* Exit modal */
.exit-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.7);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: var(--z-modal);
}
.exit-modal {
  background: var(--color-nebula);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-10);
  max-width: 360px;
  width: 90%;
  text-align: center;
}
.exit-icon { font-size: 2.5rem; color: var(--color-flare); margin-bottom: var(--space-5); }
.exit-title { font-family: var(--font-display); font-size: var(--text-xl); font-weight: var(--weight-bold); color: var(--color-star); margin-bottom: var(--space-3); }
.exit-sub { font-size: var(--text-sm); color: var(--color-comet); line-height: var(--leading-relaxed); margin-bottom: var(--space-8); }
.exit-actions { display: flex; gap: var(--space-3); justify-content: center; }
.btn-retomar { padding: var(--space-2) var(--space-5); border-radius: var(--radius-md); border: 1px solid var(--color-border); color: var(--color-comet); background: transparent; font-size: var(--text-sm); font-weight: var(--weight-semibold); cursor: pointer; transition: all var(--transition-fast); }
.btn-retomar:hover { background: rgba(255,255,255,0.05); }
.btn-abortar { padding: var(--space-2) var(--space-5); border-radius: var(--radius-md); background: var(--color-nova-dim); border: 1px solid var(--color-nova-border); color: var(--color-nova); font-size: var(--text-sm); font-weight: var(--weight-semibold); cursor: pointer; transition: all var(--transition-fast); }
.btn-abortar:hover { background: rgba(255,77,109,0.2); }

/* Focus bar */
.focus-bar {
  position: sticky;
  top: 0;
  z-index: var(--z-topbar);
  background: rgba(13,16,36,0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--color-border);
  height: var(--topbar-height);
  padding: 0 var(--space-6);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
}
.focus-logo { font-family: var(--font-display); font-size: var(--text-lg); font-weight: var(--weight-bold); }
.logo-orbit { color: var(--color-orbit); }
.logo-star  { color: var(--color-star); }

.focus-progress { flex: 1; max-width: 420px; display: flex; flex-direction: column; align-items: center; gap: var(--space-1); }
.progress-label { font-size: var(--text-2xs); font-family: var(--font-mono); font-weight: var(--weight-semibold); color: var(--color-dust); text-transform: uppercase; letter-spacing: 0.1em; }
.progress-track { width: 100%; height: 3px; background: rgba(255,255,255,0.08); border-radius: var(--radius-full); overflow: hidden; }
.progress-fill { height: 100%; background: var(--color-orbit); transition: width 0.4s ease-out; border-radius: var(--radius-full); }

.btn-sair { padding: var(--space-1) var(--space-3); border-radius: var(--radius-md); border: 1px solid var(--color-border); color: var(--color-dust); background: transparent; font-size: var(--text-sm); font-weight: var(--weight-semibold); cursor: pointer; transition: all var(--transition-fast); }
.btn-sair:hover { border-color: var(--color-nova-border); color: var(--color-nova); background: var(--color-nova-dim); }

/* States */
.state-center { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: var(--space-4); color: var(--color-comet); }
.state-text { font-size: var(--text-sm); }
.error-icon { font-size: 3rem; color: var(--color-nova); }
.btn-voltar { margin-top: var(--space-2); padding: var(--space-3) var(--space-6); border-radius: var(--radius-md); background: var(--color-orbit); color: var(--color-cosmos); font-family: var(--font-display); font-weight: var(--weight-semibold); font-size: var(--text-sm); text-transform: uppercase; letter-spacing: 0.1em; cursor: pointer; border: none; transition: all var(--transition-fast); }
.load-card { width: 160px; height: 192px; background: rgba(255,255,255,0.05); border-radius: var(--radius-xl); }
.skeleton { position: relative; overflow: hidden; }
.skeleton::after { content: ''; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent); animation: shimmer 1.5s infinite; }
@keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

/* Prova content */
.prova-content { max-width: 720px; width: 100%; margin: 0 auto; padding: var(--space-8) var(--space-4) var(--space-20); }

.questao-header { display: flex; align-items: flex-end; justify-content: space-between; margin-bottom: var(--space-6); padding-bottom: var(--space-5); border-bottom: 1px solid var(--color-border); gap: var(--space-4); }
.simulado-titulo { font-family: var(--font-display); font-size: var(--text-lg); font-weight: var(--weight-semibold); color: var(--color-star); }
.questao-tags { display: flex; gap: var(--space-2); flex-shrink: 0; }
.tag { display: inline-block; padding: 3px var(--space-2); border-radius: var(--radius-sm); background: rgba(255,255,255,0.05); border: 1px solid var(--color-border); color: var(--color-dust); font-size: var(--text-xs); font-weight: var(--weight-medium); white-space: nowrap; }
.tag--pulsar { background: rgba(124,110,255,0.1); border-color: rgba(124,110,255,0.2); color: var(--color-pulsar); }

.questao-card { background: var(--color-nebula); border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: var(--space-6) var(--space-8); margin-bottom: var(--space-6); }
@media (max-width: 640px) { .questao-card { padding: var(--space-5); } }

.questao-body { margin-bottom: var(--space-8); }
.questao-num { font-family: var(--font-mono); font-size: var(--text-xs); font-weight: var(--weight-bold); color: var(--color-orbit); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: var(--space-4); }
.questao-texto { color: var(--color-comet); font-size: var(--text-base); line-height: var(--leading-relaxed); }
.questao-img { max-width: 100%; border-radius: var(--radius-md); margin-bottom: var(--space-8); border: 1px solid var(--color-border); }

.opcoes { display: flex; flex-direction: column; gap: var(--space-3); }
.opcao {
  display: flex;
  align-items: stretch;
  border-radius: var(--radius-md);
  border: 2px solid var(--color-border);
  cursor: pointer;
  transition: all var(--transition-fast);
  overflow: hidden;
}
.opcao:hover { border-color: rgba(255,255,255,0.2); background: rgba(255,255,255,0.03); }
.opcao--selected { border-color: var(--color-orbit); background: rgba(0,229,255,0.05); }

.opcao-letra {
  width: 48px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  border-right: 1px solid var(--color-border);
  background: rgba(255,255,255,0.03);
  font-family: var(--font-display);
  font-weight: var(--weight-bold);
  font-size: var(--text-sm);
  color: var(--color-dust);
  transition: all var(--transition-fast);
}
.opcao-letra--selected { background: rgba(0,229,255,0.1); border-color: rgba(0,229,255,0.3); color: var(--color-orbit); }
.opcao-texto { flex: 1; padding: var(--space-4) var(--space-5); font-size: var(--text-sm); color: var(--color-comet); line-height: var(--leading-snug); }

/* Controles */
.controles {
  background: var(--color-nebula);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-4) var(--space-6);
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
  flex-wrap: wrap;
}
.controles-status { display: flex; align-items: center; gap: var(--space-2); font-size: var(--text-sm); font-weight: var(--weight-semibold); color: var(--color-dust); }
.status-dot { width: 8px; height: 8px; border-radius: 50%; background: rgba(255,255,255,0.15); transition: all var(--transition-fast); }
.status-dot--done { background: var(--color-stellar); box-shadow: 0 0 8px rgba(0,214,143,0.5); }
.controles-btns { display: flex; gap: var(--space-3); }

.btn-anterior { padding: var(--space-2) var(--space-5); border-radius: var(--radius-md); border: 1px solid var(--color-border); color: var(--color-comet); background: transparent; font-size: var(--text-sm); font-weight: var(--weight-semibold); cursor: pointer; transition: all var(--transition-fast); }
.btn-anterior:hover:not(:disabled) { background: rgba(255,255,255,0.05); }
.btn-anterior:disabled { opacity: 0.3; cursor: not-allowed; }

.btn-proxima { padding: var(--space-2) var(--space-6); border-radius: var(--radius-md); background: var(--color-orbit); color: var(--color-cosmos); font-family: var(--font-display); font-weight: var(--weight-semibold); font-size: var(--text-sm); text-transform: uppercase; letter-spacing: 0.08em; border: none; cursor: pointer; transition: all var(--transition-fast); }
.btn-proxima:hover { box-shadow: 0 0 15px rgba(0,229,255,0.3); transform: scale(1.02); }

.btn-finalizar { padding: var(--space-2) var(--space-6); border-radius: var(--radius-md); background: var(--color-stellar); color: white; font-family: var(--font-display); font-weight: var(--weight-semibold); font-size: var(--text-sm); text-transform: uppercase; letter-spacing: 0.08em; border: none; cursor: pointer; transition: all var(--transition-fast); display: flex; align-items: center; gap: var(--space-2); }
.btn-finalizar:hover:not(:disabled) { box-shadow: 0 0 15px rgba(0,214,143,0.3); transform: scale(1.02); }
.btn-finalizar:disabled { opacity: 0.4; cursor: not-allowed; transform: none; box-shadow: none; }

.spinner { width: 16px; height: 16px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Alertas */
.alerta { margin-top: var(--space-4); display: flex; align-items: center; gap: var(--space-3); padding: var(--space-3) var(--space-4); border-radius: var(--radius-md); font-size: var(--text-sm); }
.alerta--flare { background: rgba(255,184,48,0.08); border: 1px solid rgba(255,184,48,0.2); color: var(--color-flare); }
.alerta--nova  { background: var(--color-nova-dim); border: 1px solid var(--color-nova-border); color: var(--color-nova); }

@media (max-width: 640px) { .focus-progress { display: none; } }
</style>

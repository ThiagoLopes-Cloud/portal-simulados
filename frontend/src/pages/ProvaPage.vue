<template>
  <div class="prova-foco">

    <div v-if="mostrarConfirmacaoSaida" class="modal-overlay">
      <div class="modal-clean">
        <div class="modal-icon text-red">⚠️</div>
        <h3>Abandonar Missão?</h3>
        <p>Seus dados de performance serão perdidos. Você terá que recomeçar esta simulação do zero.</p>
        <div class="modal-actions">
          <button @click="mostrarConfirmacaoSaida = false" class="btn-cancel-clean">
            Retomar Foco
          </button>
          <button @click="confirmarSaida" class="btn-danger-clean">
            Abortar
          </button>
        </div>
      </div>
    </div>

    <nav class="focus-bar">
      <div class="focus-logo">
        <span class="logo-white">SIMUS</span><span class="logo-accent">LAB</span>
      </div>
      
      <div class="focus-center">
        <span class="progress-text">Progresso Tático: {{ questaoAtual + 1 }} / {{ simulado?.questoes?.length || 0 }}</span>
        <div class="progress-bar-thin">
          <div 
            class="progress-fill-thin" 
            :style="{ width: ((questaoAtual + 1) / (simulado?.questoes?.length || 1) * 100) + '%' }"
          ></div>
        </div>
      </div>

      <div class="focus-right">
        <button @click="mostrarConfirmacaoSaida = true" class="btn-exit-focus">
          Sair
        </button>
      </div>
    </nav>

    <div v-if="carregando" class="loading-state">
      <div class="shimmer-card"></div>
      <p>Decodificando ambiente de prova...</p>
    </div>

    <div v-else-if="erro" class="error-state">
      <div class="error-icon">⚠️</div>
      <p>{{ erro }}</p>
      <button @click="$router.push('/simulados')" class="btn-primary-action mt-4">Retornar à Base</button>
    </div>

    <div v-else class="exam-container">
      
      <header class="exam-header">
        <h2 class="exam-title">{{ simulado.titulo }}</h2>
        <div class="exam-badge" v-if="simulado.questoes[questaoAtual]">
          <span class="badge-materia">{{ simulado.questoes[questaoAtual].materia || 'Questão' }}</span>
          <span class="badge-dificuldade">{{ simulado.questoes[questaoAtual].dificuldade === 'F' ? 'Básica' : simulado.questoes[questaoAtual].dificuldade === 'M' ? 'Intermediária' : simulado.questoes[questaoAtual].dificuldade === 'D' ? 'Avançada' : '' }}</span>
        </div>
      </header>

      <div class="question-paper" v-if="simulado.questoes[questaoAtual]">
        
        <div class="q-statement">
          <p class="q-number-tag">Q. {{ questaoAtual + 1 }}</p>
          <p class="q-text">{{ simulado.questoes[questaoAtual].enunciado }}</p>
        </div>

        <img
          v-if="simulado.questoes[questaoAtual].imagem_enunciado"
          :src="simulado.questoes[questaoAtual].imagem_enunciado"
          class="q-image"
          alt="Material de apoio"
        />

        <div class="options-group">
          <div
            v-for="opcao in opcoesDaQuestao(simulado.questoes[questaoAtual])"
            :key="opcao.letra"
            class="option-row"
            :class="{ 'selected': respostas[simulado.questoes[questaoAtual].id] === opcao.letra }"
            @click="selecionar(simulado.questoes[questaoAtual].id, opcao.letra)"
          >
            <div class="opt-indicator">
              <span class="opt-letter">{{ opcao.letra }}</span>
            </div>
            <div class="opt-content">
              <span class="opt-text">{{ opcao.texto }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="exam-controls">
        <div class="status-counter">
          <span class="dot-indicator" :class="{ 'active': totalRespondidas === simulado.questoes.length }"></span>
          {{ totalRespondidas }} de {{ simulado.questoes.length }} mapeadas
        </div>

        <div class="nav-buttons">
          <button @click="anterior" :disabled="questaoAtual === 0" class="btn-nav-secondary">
            Anterior
          </button>

          <button v-if="questaoAtual < simulado.questoes.length - 1" @click="proxima" class="btn-nav-primary">
            Avançar
          </button>

          <button v-else @click="enviar" :disabled="enviando || totalRespondidas < simulado.questoes.length" class="btn-nav-submit">
            {{ enviando ? 'Compilando...' : 'Finalizar Simulação' }}
          </button>
        </div>
      </div>

      <div v-if="questaoAtual === simulado.questoes.length - 1 && totalRespondidas < simulado.questoes.length" class="alert-warning">
        <span class="alert-icon">⚠️</span> Existem {{ simulado.questoes.length - totalRespondidas }} pontos cegos (questões sem resposta).
      </div>

      <div v-if="erroEnvio" class="alert-error">
        {{ erroEnvio }}
      </div>

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
    const response = await api.get(`/api/simulados/${id}/`) // Atualizado para /api/
    simulado.value = response.data
  } catch (error) {
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
  ].filter(opcao => opcao.texto && opcao.texto.trim() !== '')
}

function selecionar(questaoId, opcao) {
  respostas.value[questaoId] = opcao
}

function proxima() {
  if (questaoAtual.value < simulado.value.questoes.length - 1) questaoAtual.value++
}

function anterior() {
  if (questaoAtual.value > 0) questaoAtual.value--
}

function confirmarSaida() {
  router.push({ name: 'simulados' })
}

async function enviar() {
  erroEnvio.value = ''
  enviando.value = true

  try {
    const listaRespostas = Object.entries(respostas.value).map(([questaoId, opcao]) => ({
      questao_id: parseInt(questaoId),
      opcao_escolhida: opcao,
    }))

    const response = await api.post('/api/responder/', { // Atualizado para /api/
      simulado_id: parseInt(route.params.id),
      respostas: listaRespostas,
    })

    router.push({
      name: 'resultado',
      params: { id: response.data.resultado.resultado_id },
    })

  } catch (error) {
    if (error.response?.data?.error) {
      erroEnvio.value = error.response.data.error
    } else {
      erroEnvio.value = 'Falha na transmissão dos dados. Tente novamente.'
    }
  } finally {
    enviando.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Focus Layout Base */
.prova-foco { min-height: 100vh; background-color: #F8FAFC; font-family: 'Inter', sans-serif; display: flex; flex-direction: column; }

/* Modal Clean */
.modal-overlay { position: fixed; inset: 0; background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 999; }
.modal-clean { background: white; border-radius: 16px; padding: 40px; max-width: 420px; width: 90%; text-align: center; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); }
.modal-icon { font-size: 3rem; margin-bottom: 20px; }
.text-red { color: #EF4444; }
.modal-clean h3 { font-size: 1.4rem; color: #0F172A; margin-bottom: 10px; font-weight: 700; }
.modal-clean p { color: #64748B; font-size: 0.95rem; margin-bottom: 30px; line-height: 1.5; }
.modal-actions { display: flex; gap: 15px; justify-content: center; }
.btn-cancel-clean { padding: 12px 24px; border-radius: 8px; border: 1px solid #CBD5E1; background: white; color: #334155; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-cancel-clean:hover { background: #F1F5F9; border-color: #94A3B8; }
.btn-danger-clean { padding: 12px 24px; border-radius: 8px; border: none; background: #EF4444; color: white; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-danger-clean:hover { background: #DC2626; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.2); }

/* Focus Bar Topo */
.focus-bar { background: #0A2540; color: white; padding: 0 30px; height: 64px; display: flex; justify-content: space-between; align-items: center; position: sticky; top: 0; z-index: 100; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
.logo-white { font-weight: 800; font-size: 1.2rem; letter-spacing: -0.5px; }
.logo-accent { color: #00D09C; font-weight: 800; font-size: 1.2rem; }

.focus-center { flex: 1; max-width: 500px; display: flex; flex-direction: column; align-items: center; gap: 6px; margin: 0 20px; }
.progress-text { font-size: 0.75rem; font-weight: 600; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.5px; }
.progress-bar-thin { width: 100%; height: 4px; background: rgba(255, 255, 255, 0.1); border-radius: 10px; overflow: hidden; }
.progress-fill-thin { height: 100%; background: #00D09C; transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1); }

.btn-exit-focus { background: transparent; border: 1px solid rgba(255,255,255,0.2); color: #94A3B8; padding: 6px 16px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-exit-focus:hover { border-color: #EF4444; color: #EF4444; background: rgba(239, 68, 68, 0.1); }

/* Status States */
.loading-state, .error-state { display: flex; flex-direction: column; align-items: center; justify-content: center; height: calc(100vh - 64px); color: #64748B; }
.shimmer-card { width: 600px; height: 400px; background: #E2E8F0; border-radius: 16px; position: relative; overflow: hidden; margin-bottom: 20px; }
.shimmer-card::after { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent); animation: loading 1.5s infinite; }
@keyframes loading { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }
.error-icon { font-size: 3rem; margin-bottom: 15px; }
.btn-primary-action { background: #0052FF; color: white; padding: 12px 24px; border-radius: 8px; font-weight: 600; border: none; cursor: pointer; }
.mt-4 { margin-top: 20px; }

/* AMBIENTE DE PROVA (Folha Digital) */
.exam-container { max-width: 800px; margin: 40px auto 80px auto; padding: 0 20px; }
.exam-header { display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 25px; padding-bottom: 15px; border-bottom: 2px solid #E2E8F0; }
.exam-title { font-size: 1.5rem; color: #0F172A; font-weight: 700; margin: 0; }
.exam-badge { display: flex; gap: 8px; }
.badge-materia { background: #E0E7FF; color: #4338CA; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; }
.badge-dificuldade { background: #F1F5F9; color: #475569; padding: 4px 10px; border-radius: 6px; font-size: 0.75rem; font-weight: 600; }

.question-paper { background: white; padding: 40px; border-radius: 16px; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.03); border: 1px solid #E2E8F0; margin-bottom: 30px; }
.q-statement { margin-bottom: 30px; }
.q-number-tag { color: #0052FF; font-weight: 800; font-size: 0.9rem; margin-bottom: 15px; text-transform: uppercase; letter-spacing: 0.5px; }
.q-text { font-size: 1.15rem; color: #1E293B; line-height: 1.7; font-weight: 400; margin: 0; }
.q-image { max-width: 100%; border-radius: 8px; margin-bottom: 30px; border: 1px solid #E2E8F0; }

/* Alternativas */
.options-group { display: flex; flex-direction: column; gap: 12px; }
.option-row { display: flex; align-items: stretch; border: 2px solid #F1F5F9; border-radius: 12px; cursor: pointer; transition: all 0.2s ease; overflow: hidden; background: white; }
.option-row:hover { border-color: #CBD5E1; background: #F8FAFC; }
.option-row.selected { border-color: #0052FF; background: #EFF6FF; box-shadow: 0 4px 12px rgba(0, 82, 255, 0.05); }

.opt-indicator { width: 50px; display: flex; align-items: center; justify-content: center; background: #F8FAFC; border-right: 2px solid #F1F5F9; transition: all 0.2s; }
.option-row.selected .opt-indicator { background: #0052FF; border-right-color: #0052FF; }

.opt-letter { font-weight: 800; font-size: 1rem; color: #64748B; }
.option-row.selected .opt-letter { color: white; }

.opt-content { flex: 1; padding: 16px 20px; display: flex; align-items: center; }
.opt-text { font-size: 1rem; color: #334155; line-height: 1.5; }
.option-row.selected .opt-text { font-weight: 500; color: #0F172A; }

/* Controles de Rodapé */
.exam-controls { display: flex; justify-content: space-between; align-items: center; background: white; padding: 20px 30px; border-radius: 12px; border: 1px solid #E2E8F0; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
.status-counter { display: flex; align-items: center; gap: 10px; font-size: 0.85rem; font-weight: 600; color: #64748B; }
.dot-indicator { width: 8px; height: 8px; border-radius: 50%; background: #CBD5E1; transition: background 0.3s; }
.dot-indicator.active { background: #10B981; box-shadow: 0 0 8px rgba(16, 185, 129, 0.4); }

.nav-buttons { display: flex; gap: 15px; }
.btn-nav-secondary { padding: 12px 24px; border-radius: 8px; border: 1px solid #CBD5E1; background: white; color: #334155; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-nav-secondary:hover:not(:disabled) { background: #F1F5F9; }
.btn-nav-secondary:disabled { opacity: 0.4; cursor: not-allowed; }

.btn-nav-primary { padding: 12px 30px; border-radius: 8px; border: none; background: #0052FF; color: white; font-weight: 600; cursor: pointer; transition: all 0.2s; }
.btn-nav-primary:hover { background: #0043D1; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 82, 255, 0.2); }

.btn-nav-submit { padding: 12px 30px; border-radius: 8px; border: none; background: #10B981; color: white; font-weight: 700; cursor: pointer; transition: all 0.2s; }
.btn-nav-submit:hover:not(:disabled) { background: #059669; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(16, 185, 129, 0.2); }
.btn-nav-submit:disabled { background: #A7F3D0; cursor: not-allowed; color: #064E3B; }

/* Alertas */
.alert-warning { background: #FFF7ED; border: 1px solid #FED7AA; color: #9A3412; padding: 15px; border-radius: 12px; margin-top: 20px; font-size: 0.9rem; font-weight: 500; display: flex; align-items: center; gap: 10px; justify-content: center; }
.alert-error { background: #FEF2F2; border: 1px solid #FECACA; color: #991B1B; padding: 15px; border-radius: 12px; margin-top: 20px; font-size: 0.9rem; font-weight: 500; text-align: center; }

@media (max-width: 768px) {
  .focus-center { display: none; }
  .exam-controls { flex-direction: column; gap: 20px; }
  .nav-buttons { width: 100%; display: grid; grid-template-columns: 1fr 1fr; }
  .btn-nav-submit { grid-column: 1 / -1; }
  .question-paper { padding: 25px 20px; }
}
</style>
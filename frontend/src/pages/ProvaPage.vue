<template>
  <div class="prova">

    <!-- Navbar -->
    <nav class="navbar">
      <h1>Portal de Simulados</h1>
      <span class="progresso">
        Questão {{ questaoAtual + 1 }} de {{ simulado?.questoes?.length || 0 }}
      </span>
    </nav>

    <!-- Carregando -->
    <div v-if="carregando" class="loading">Carregando prova...</div>

    <!-- Erro -->
    <div v-else-if="erro" class="erro-container">
      <p>{{ erro }}</p>
      <button @click="$router.push('/simulados')">Voltar</button>
    </div>

    <!-- Prova -->
    <div v-else class="container">

      <!-- Título do simulado -->
      <h2>{{ simulado.titulo }}</h2>

      <!-- Barra de progresso -->
      <div class="barra-progresso">
        <div
          class="barra-fill"
          :style="{ width: ((questaoAtual + 1) / simulado.questoes.length * 100) + '%' }"
        ></div>
      </div>

      <!-- Questão atual -->
      <div class="card-questao" v-if="simulado.questoes[questaoAtual]">

        <p class="numero-questao">Questão {{ questaoAtual + 1 }}</p>
        <p class="enunciado">{{ simulado.questoes[questaoAtual].enunciado }}</p>

        <!-- Imagem do enunciado se existir -->
        <img
          v-if="simulado.questoes[questaoAtual].imagem_enunciado"
          :src="simulado.questoes[questaoAtual].imagem_enunciado"
          class="imagem-questao"
        />

        <!-- Alternativas — 5 opções no formato ENEM -->
        <!-- opcoesDaQuestao filtra alternativas vazias automaticamente -->
        <div class="alternativas">
          <div
            v-for="opcao in opcoesDaQuestao(simulado.questoes[questaoAtual])"
            :key="opcao.letra"
            class="alternativa"
            :class="{ selecionada: respostas[simulado.questoes[questaoAtual].id] === opcao.letra }"
            @click="selecionar(simulado.questoes[questaoAtual].id, opcao.letra)"
          >
            <span class="letra">{{ opcao.letra }}</span>
            <span class="texto">{{ opcao.texto }}</span>
          </div>
        </div>

      </div>

      <!-- Botões de navegação -->
      <div class="navegacao">
        <button
          @click="anterior"
          :disabled="questaoAtual === 0"
          class="btn-secundario"
        >
          ← Anterior
        </button>

        <!-- Botão próxima ou enviar -->
        <button
          v-if="questaoAtual < simulado.questoes.length - 1"
          @click="proxima"
          class="btn-primario"
        >
          Próxima →
        </button>

        <button
          v-else
          @click="enviar"
          :disabled="enviando"
          class="btn-enviar"
        >
          {{ enviando ? 'Enviando...' : '✓ Enviar respostas' }}
        </button>
      </div>

      <!-- Erro ao enviar -->
      <div v-if="erroEnvio" class="erro">{{ erroEnvio }}</div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../services/api.js'

const router = useRouter()
const route = useRoute()

// Dados do simulado retornado pela API
const simulado = ref(null)
const carregando = ref(true)
const erro = ref('')
const erroEnvio = ref('')
const enviando = ref(false)

// Índice da questão atual
const questaoAtual = ref(0)

// Objeto que armazena as respostas do aluno
// { questao_id: 'A', questao_id: 'B', ... }
const respostas = ref({})

// Busca o simulado ao carregar a página
onMounted(async () => {
  try {
    // Pega o ID do simulado da URL ex: /simulado/1
    const id = route.params.id
    const response = await api.get(`/simulados/${id}/`)
    simulado.value = response.data
  } catch (error) {
    erro.value = 'Erro ao carregar o simulado.'
  } finally {
    carregando.value = false
  }
})

// Retorna apenas as alternativas que têm conteúdo preenchido
// Funciona tanto para questões de 4 quanto de 5 alternativas
function opcoesDaQuestao(questao) {
  const todasOpcoes = [
    { letra: 'A', texto: questao.opcao_a },
    { letra: 'B', texto: questao.opcao_b },
    { letra: 'C', texto: questao.opcao_c },
    { letra: 'D', texto: questao.opcao_d },
    { letra: 'E', texto: questao.opcao_e },
  ]

  // Filtra apenas alternativas com texto preenchido
  return todasOpcoes.filter(opcao => opcao.texto && opcao.texto.trim() !== '')
}

// Registra a resposta do aluno para uma questão
function selecionar(questaoId, opcao) {
  respostas.value[questaoId] = opcao
}

// Avança para a próxima questão
function proxima() {
  if (questaoAtual.value < simulado.value.questoes.length - 1) {
    questaoAtual.value++
  }
}

// Volta para a questão anterior
function anterior() {
  if (questaoAtual.value > 0) {
    questaoAtual.value--
  }
}

// Envia as respostas para a API
async function enviar() {
  erroEnvio.value = ''
  enviando.value = true

  try {
    // Monta a lista de respostas no formato que a API espera
    const listaRespostas = Object.entries(respostas.value).map(([questaoId, opcao]) => ({
      questao_id: parseInt(questaoId),
      opcao_escolhida: opcao,
    }))

    // Envia para a API
    const response = await api.post('/responder/', {
      simulado_id: parseInt(route.params.id),
      respostas: listaRespostas,
    })

    // Redireciona para a tela de resultado com os dados do score
    router.push({
      name: 'resultado',
      params: { id: route.params.id },
      query: {
        acertos: response.data.resultado.acertos,
        total: response.data.resultado.total_questoes,
        score: response.data.resultado.score,
      }
    })

  } catch (error) {
    if (error.response?.data?.error) {
      erroEnvio.value = error.response.data.error
    } else {
      erroEnvio.value = 'Erro ao enviar respostas. Tente novamente.'
    }
  } finally {
    enviando.value = false
  }
}
</script>

<style scoped>
.prova {
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

.progresso {
  font-size: 14px;
  opacity: 0.9;
  background: rgba(255,255,255,0.2);
  padding: 6px 14px;
  border-radius: 99px;
}

.loading {
  text-align: center;
  padding: 60px;
  color: #666;
}

.erro-container {
  text-align: center;
  padding: 60px;
}

.container {
  max-width: 700px;
  margin: 0 auto;
  padding: 40px 20px;
}

h2 {
  font-size: 22px;
  color: #333;
  margin-bottom: 16px;
}

.barra-progresso {
  height: 6px;
  background: #ddd;
  border-radius: 99px;
  margin-bottom: 32px;
  overflow: hidden;
}

.barra-fill {
  height: 100%;
  background: #667eea;
  border-radius: 99px;
  transition: width 0.3s ease;
}

.card-questao {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  margin-bottom: 24px;
}

.numero-questao {
  font-size: 13px;
  color: #667eea;
  font-weight: 600;
  margin-bottom: 12px;
  text-transform: uppercase;
}

.enunciado {
  font-size: 18px;
  color: #333;
  line-height: 1.6;
  margin-bottom: 24px;
}

.imagem-questao {
  width: 100%;
  border-radius: 8px;
  margin-bottom: 20px;
}

.alternativas {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.alternativa {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  border: 2px solid #eee;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.15s;
}

.alternativa:hover {
  border-color: #667eea;
  background: #f0f3ff;
}

.alternativa.selecionada {
  border-color: #667eea;
  background: #e8f0fe;
}

.letra {
  width: 32px;
  height: 32px;
  background: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
}

.alternativa.selecionada .letra {
  background: #4a5fd6;
}

.texto {
  font-size: 15px;
  color: #333;
}

.navegacao {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.btn-primario, .btn-secundario, .btn-enviar {
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-size: 15px;
  transition: background 0.2s;
}

.btn-primario {
  background: #667eea;
  color: white;
  margin-left: auto;
}

.btn-primario:hover { background: #5a6fd6; }

.btn-secundario {
  background: #eee;
  color: #555;
}

.btn-secundario:hover:not(:disabled) { background: #ddd; }
.btn-secundario:disabled { opacity: 0.4; cursor: not-allowed; }

.btn-enviar {
  background: #22c55e;
  color: white;
  margin-left: auto;
}

.btn-enviar:hover:not(:disabled) { background: #16a34a; }
.btn-enviar:disabled { opacity: 0.6; cursor: not-allowed; }

.erro {
  background: #fee;
  color: #c00;
  padding: 12px;
  border-radius: 6px;
  margin-top: 16px;
  font-size: 14px;
}
</style>
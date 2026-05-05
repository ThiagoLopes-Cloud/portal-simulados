<template>
  <div class="min-h-screen bg-simus-bg font-body flex flex-col">

    <!-- ── Modal de confirmação de saída ──────────────────────── -->
    <div v-if="mostrarConfirmacaoSaida"
         class="fixed inset-0 bg-black/70 backdrop-blur-sm flex items-center justify-center z-[999]">
      <div class="bg-simus-surface border border-white/10 rounded-simus p-10 max-w-sm w-[90%] text-center shadow-2xl">
        <div class="text-4xl mb-5">⚠️</div>
        <h3 class="font-display text-xl font-bold text-slate-50 mb-3">Abandonar Missão?</h3>
        <p class="text-slate-400 text-sm leading-relaxed mb-8">
          Seus dados de performance serão perdidos. Você terá que recomeçar esta simulação do zero.
        </p>
        <div class="flex gap-3 justify-center">
          <button @click="mostrarConfirmacaoSaida = false"
                  class="px-6 py-2.5 rounded-xl border border-white/10 text-slate-300 text-sm font-semibold
                         hover:bg-white/5 transition-colors">
            Retomar Foco
          </button>
          <button @click="confirmarSaida"
                  class="px-6 py-2.5 rounded-xl bg-red-500/10 border border-red-500/30 text-red-400 text-sm font-semibold
                         hover:bg-red-500/20 transition-colors">
            Abortar
          </button>
        </div>
      </div>
    </div>

    <!-- ── Barra de foco (topo) ───────────────────────────────── -->
    <nav class="sticky top-0 z-50 bg-simus-surface/80 backdrop-blur-md border-b border-white/5
                h-16 px-6 flex items-center justify-between gap-4">
      <div class="font-display font-bold text-lg">
        <span class="text-simus-cyan">SIMUS</span><span class="text-slate-50">LAB</span>
      </div>

      <div class="flex-1 max-w-md hidden sm:flex flex-col items-center gap-1.5">
        <span class="text-[0.65rem] font-semibold text-slate-500 uppercase tracking-widest">
          Progresso Tático: {{ questaoAtual + 1 }} / {{ simulado?.questoes?.length || 0 }}
        </span>
        <div class="w-full h-1 bg-white/10 rounded-full overflow-hidden">
          <div class="h-full bg-simus-cyan transition-all duration-400 ease-out"
               :style="{ width: ((questaoAtual + 1) / (simulado?.questoes?.length || 1) * 100) + '%' }" />
        </div>
      </div>

      <button @click="mostrarConfirmacaoSaida = true"
              class="px-4 py-1.5 rounded-lg border border-white/10 text-slate-400 text-sm font-semibold
                     hover:border-red-500/40 hover:text-red-400 hover:bg-red-500/5 transition-all">
        Sair
      </button>
    </nav>

    <!-- ── Loading ────────────────────────────────────────────── -->
    <div v-if="carregando" class="flex-1 flex flex-col items-center justify-center gap-4 text-slate-400">
      <div class="w-40 h-48 bg-white/5 rounded-simus shimmer" />
      <p class="text-sm">Decodificando ambiente de prova...</p>
    </div>

    <!-- ── Erro ───────────────────────────────────────────────── -->
    <div v-else-if="erro" class="flex-1 flex flex-col items-center justify-center gap-4">
      <div class="text-5xl">⚠️</div>
      <p class="text-slate-400">{{ erro }}</p>
      <button @click="$router.push('/simulados')"
              class="mt-2 px-6 py-3 rounded-xl bg-simus-cyan text-simus-bg font-display font-semibold text-sm uppercase tracking-widest
                     hover:shadow-[0_0_20px_rgba(0,229,255,0.3)] transition-all">
        Retornar à Base
      </button>
    </div>

    <!-- ── Ambiente de prova ──────────────────────────────────── -->
    <div v-else class="max-w-3xl w-full mx-auto px-4 sm:px-6 py-8 pb-20">

      <!-- Header da questão -->
      <header class="flex items-end justify-between mb-6 pb-5 border-b border-white/5">
        <h2 class="font-display text-lg font-semibold text-slate-50">{{ simulado.titulo }}</h2>
        <div class="flex gap-2" v-if="simulado.questoes[questaoAtual]">
          <span class="px-2.5 py-1 rounded-lg bg-simus-purple/10 border border-simus-purple/20
                       text-simus-purple text-xs font-semibold">
            {{ simulado.questoes[questaoAtual].materia || 'Questão' }}
          </span>
          <span class="px-2.5 py-1 rounded-lg bg-white/5 border border-white/10 text-slate-400 text-xs font-medium">
            {{ { F: 'Básica', M: 'Intermediária', D: 'Avançada' }[simulado.questoes[questaoAtual].dificuldade] || '' }}
          </span>
        </div>
      </header>

      <!-- Papel da questão -->
      <div v-if="simulado.questoes[questaoAtual]" class="bg-simus-surface border border-white/5 rounded-simus p-6 sm:p-8 mb-6">

        <div class="mb-8">
          <p class="text-simus-cyan text-xs font-display font-bold uppercase tracking-widest mb-4">
            Q. {{ questaoAtual + 1 }}
          </p>
          <p class="text-slate-200 text-base sm:text-lg leading-relaxed">
            {{ simulado.questoes[questaoAtual].enunciado }}
          </p>
        </div>

        <img v-if="simulado.questoes[questaoAtual].imagem_enunciado"
             :src="simulado.questoes[questaoAtual].imagem_enunciado"
             class="max-w-full rounded-xl mb-8 border border-white/5" alt="Material de apoio" />

        <div class="space-y-3">
          <div v-for="opcao in opcoesDaQuestao(simulado.questoes[questaoAtual])" :key="opcao.letra"
               class="flex items-stretch rounded-xl border-2 cursor-pointer transition-all duration-150 overflow-hidden"
               :class="respostas[simulado.questoes[questaoAtual].id] === opcao.letra
                 ? 'border-simus-cyan bg-simus-cyan/5'
                 : 'border-white/10 bg-white/[0.03] hover:border-white/20 hover:bg-white/[0.06]'"
               @click="selecionar(simulado.questoes[questaoAtual].id, opcao.letra)">
            <div class="w-12 shrink-0 flex items-center justify-center border-r"
                 :class="respostas[simulado.questoes[questaoAtual].id] === opcao.letra
                   ? 'border-simus-cyan/30 bg-simus-cyan/10'
                   : 'border-white/5 bg-white/[0.03]'">
              <span class="font-display font-bold text-sm"
                    :class="respostas[simulado.questoes[questaoAtual].id] === opcao.letra
                      ? 'text-simus-cyan' : 'text-slate-500'">
                {{ opcao.letra }}
              </span>
            </div>
            <div class="flex-1 px-5 py-4 flex items-center">
              <span class="text-slate-200 text-sm leading-snug">{{ opcao.texto }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Controles de rodapé -->
      <div class="bg-simus-surface border border-white/5 rounded-simus px-6 py-4 flex items-center justify-between gap-4 flex-wrap">
        <div class="flex items-center gap-2 text-sm font-semibold text-slate-400">
          <span class="w-2 h-2 rounded-full transition-colors"
                :class="totalRespondidas === simulado.questoes.length ? 'bg-emerald-400 shadow-[0_0_8px_rgba(52,211,153,0.4)]' : 'bg-white/20'" />
          {{ totalRespondidas }} de {{ simulado.questoes.length }} mapeadas
        </div>

        <div class="flex gap-3">
          <button @click="anterior" :disabled="questaoAtual === 0"
                  class="px-5 py-2.5 rounded-xl border border-white/10 text-slate-300 text-sm font-semibold
                         hover:bg-white/5 transition-colors disabled:opacity-30 disabled:cursor-not-allowed">
            Anterior
          </button>

          <button v-if="questaoAtual < simulado.questoes.length - 1" @click="proxima"
                  class="px-6 py-2.5 rounded-xl bg-simus-cyan text-simus-bg text-sm font-display font-semibold uppercase tracking-wider
                         hover:scale-[1.02] hover:shadow-[0_0_15px_rgba(0,229,255,0.3)] transition-all">
            Avançar
          </button>

          <button v-else @click="enviar"
                  :disabled="enviando || totalRespondidas < simulado.questoes.length"
                  class="px-6 py-2.5 rounded-xl bg-emerald-500 text-white text-sm font-display font-semibold uppercase tracking-wider
                         hover:scale-[1.02] hover:shadow-[0_0_15px_rgba(52,211,153,0.3)] transition-all
                         disabled:bg-emerald-500/40 disabled:cursor-not-allowed disabled:scale-100 disabled:shadow-none">
            <span v-if="enviando" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin inline-block mr-2" />
            {{ enviando ? 'Compilando...' : 'Finalizar Simulação' }}
          </button>
        </div>
      </div>

      <div v-if="questaoAtual === simulado.questoes.length - 1 && totalRespondidas < simulado.questoes.length"
           class="mt-4 flex items-center gap-3 bg-amber-500/10 border border-amber-500/30 rounded-xl px-4 py-3">
        <span class="text-amber-400 text-sm">
          ⚠️ Existem {{ simulado.questoes.length - totalRespondidas }} pontos cegos (questões sem resposta).
        </span>
      </div>

      <div v-if="erroEnvio"
           class="mt-4 flex items-center gap-3 bg-red-500/10 border border-red-500/30 rounded-xl px-4 py-3">
        <span class="text-red-400 text-sm">{{ erroEnvio }}</span>
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
    const response = await api.get(`/api/simulados/${id}/`)
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

    const response = await api.post('/api/responder/', {
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
@reference "../assets/main.css";

.shimmer {
  @apply relative overflow-hidden;
}
.shimmer::after {
  content: '';
  @apply absolute inset-0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent);
  animation: shimmer 1.5s infinite;
}
@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}
</style>

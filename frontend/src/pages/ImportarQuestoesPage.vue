<template>
  <!-- Container principal da página de importação -->
  <div class="importar">

    <!-- Navbar superior — mesma do resto do sistema -->
    <nav class="navbar">
      <h1>Portal de Simulados</h1>
      <div class="nav-links">
        <router-link to="/dashboard">Dashboard</router-link>
        <router-link to="/admin/alunos">Alunos</router-link>
        <button @click="logout" class="btn-logout">Sair</button>
      </div>
    </nav>

    <!-- Conteúdo principal -->
    <div class="container">

      <!-- Cabeçalho da página -->
      <div class="page-header">
        <h2>📥 Importar Questões via IA</h2>
        <p class="subtitulo">
          Gere questões com o ChatGPT ou Claude e importe em segundos.
          Você poderá revisar e aprovar cada questão antes de publicar.
        </p>
      </div>

      <!-- Layout de duas colunas -->
      <div class="grid">

        <!-- ==============================
             COLUNA ESQUERDA — Guia de uso
             ============================== -->
        <div class="card guia">
          <h3>Como gerar suas questões</h3>

          <!-- Passo 1 -->
          <div class="passo">
            <div class="passo-numero">1</div>
            <div class="passo-conteudo">
              <strong>Acesse o ChatGPT ou o Claude</strong>
              <p>Use qualquer uma das IAs abaixo. As duas funcionam bem com o nosso prompt.</p>
              <div class="links-ia">
                <!-- Link para o ChatGPT -->
                <a href="https://chat.openai.com" target="_blank" class="btn-ia">
                  ChatGPT ↗
                </a>
                <!-- Link para o Gemini -->
                 <a href="https://gemini.google.com" target="_blank" class="btn-ia">    
                </a>
              </div>
            </div>
          </div>

          <!-- Passo 2 -->
          <div class="passo">
            <div class="passo-numero">2</div>
            <div class="passo-conteudo">
              <strong>Copie o prompt abaixo</strong>
              <p>Clique no botão para copiar o prompt completo. Ele instrui a IA a gerar questões
                 no formato exato que o nosso sistema espera.</p>

              <!-- Prévia do prompt — mostra as primeiras linhas para o professor saber o que é -->
              <div class="prompt-preview">
                Você é um especialista em elaboração de questões no padrão ENEM...
                Gere [QUANTIDADE_DE_QUESTOES] questões da disciplina [MATERIA_NOME]...
              </div>

              <!-- Botão que copia o prompt completo para o clipboard -->
              <button @click="copiarPrompt" class="btn-copiar" :class="{ copiado: promptCopiado }">
                {{ promptCopiado ? '✓ Prompt copiado!' : '📋 Copiar prompt completo' }}
              </button>
            </div>
          </div>

          <!-- Passo 3 -->
          <div class="passo">
            <div class="passo-numero">3</div>
            <div class="passo-conteudo">
              <strong>Cole na IA e substitua os campos</strong>
              <p>
                Troque <code>[NÚMERO]</code> pela quantidade de questões
                e <code>[TEMA/DISCIPLINA]</code> pelo assunto desejado.
                Então envie a mensagem.
              </p>
            </div>
          </div>

          <!-- Passo 4 -->
          <div class="passo">
            <div class="passo-numero">4</div>
            <div class="passo-conteudo">
              <strong>Copie o JSON gerado</strong>
              <p>
                A IA vai responder com um bloco de código JSON.
                Copie tudo — desde o <code>{</code> inicial até o <code>}</code> final.
              </p>
            </div>
          </div>

          <!-- Passo 5 -->
          <div class="passo">
            <div class="passo-numero">5</div>
            <div class="passo-conteudo">
              <strong>Cole aqui ao lado e importe</strong>
              <p>
                Cole o JSON na área de texto ao lado e clique em "Importar".
                Após a importação, revise e aprove as questões no
                <a href="https://portal-simulados-production.up.railway.app/admin" target="_blank">
                  Django Admin ↗
                </a>
                antes de ativar o simulado.
              </p>
            </div>
          </div>

          <!-- Aviso sobre revisão -->
          <div class="aviso-revisao">
            ⚠️ As questões importadas ficam <strong>pendentes de revisão</strong>.
            O simulado só fica visível para os alunos após você revisar, aprovar
            as questões e ativar o simulado no Admin.
          </div>
        </div>

        <!-- ==============================
             COLUNA DIREITA — Área de import
             ============================== -->
        <div class="card importacao">
          <h3>Cole o JSON aqui</h3>

          <!-- Área de texto para o JSON -->
          <textarea
            v-model="jsonTexto"
            class="json-textarea"
            placeholder='{
  "simulado": {
    "titulo": "Simulado de Matemática",
    "descricao": "10 questões de funções",
    "data_inicio": null,
    "data_fim": null
  },
  "questoes": [
    {
      "ordem": 1,
      "enunciado": "...",
      ...
    }
  ]
}'
            spellcheck="false"
          ></textarea>

          <!-- Indicador de status do JSON (válido / inválido / vazio) -->
          <div class="json-status" :class="statusJson.tipo" v-if="jsonTexto.trim()">
            {{ statusJson.mensagem }}
          </div>

          <!-- Contador de questões detectadas no JSON -->
          <div class="contador-questoes" v-if="questoesDetectadas > 0">
            📊 {{ questoesDetectadas }} questão(ões) detectada(s) no JSON
          </div>

          <!-- Botão de importar -->
          <button
            @click="importar"
            class="btn-importar"
            :disabled="!podeImportar || importando"
          >
            <!-- Estado de carregamento -->
            <span v-if="importando" class="spinner"></span>
            {{ importando ? 'Importando...' : '🚀 Importar questões' }}
          </button>

          <!-- Erro de validação local (antes de enviar) -->
          <div v-if="erroValidacao" class="feedback erro">
            <strong>❌ Erro no JSON:</strong>
            <p>{{ erroValidacao }}</p>
          </div>

          <!-- Resultado do servidor após importação bem-sucedida -->
          <div v-if="resultado" class="feedback sucesso">
            <strong>✅ Importação concluída!</strong>

            <!-- Resumo da importação -->
            <div class="resultado-resumo">
              <div class="resumo-item">
                <span class="resumo-label">Simulado criado</span>
                <span class="resumo-valor">{{ resultado.simulado_titulo }}</span>
              </div>
              <div class="resumo-item">
                <span class="resumo-label">Questões importadas</span>
                <span class="resumo-valor">{{ resultado.total_importadas }}</span>
              </div>
              <div class="resumo-item">
                <span class="resumo-label">Status</span>
                <span class="resumo-valor badge-pendente">Pendente de revisão</span>
              </div>
            </div>

            <!-- Próximos passos após importar -->
            <div class="proximos-passos">
              <p><strong>Próximos passos:</strong></p>
              <ol>
                <li>
                  Acesse o
                  <a href="https://portal-simulados-production.up.railway.app/admin/questoes/questao/?revisado__exact=0"
                     target="_blank">
                    Django Admin → Questões não revisadas ↗
                  </a>
                </li>
                <li>Revise cada questão importada</li>
                <li>Selecione as aprovadas e use a ação "Aprovar questões selecionadas"</li>
                <li>
                  Acesse
                  <a href="https://portal-simulados-production.up.railway.app/admin/simulados/simulado/"
                     target="_blank">
                    Admin → Simulados ↗
                  </a>
                  e ative o simulado
                </li>
              </ol>
            </div>

            <!-- Botão para importar novo lote -->
            <button @click="reiniciar" class="btn-novo">
              + Importar novo lote
            </button>
          </div>

          <!-- Erro retornado pelo servidor -->
          <div v-if="erroServidor" class="feedback erro">
            <strong>❌ Erro na importação:</strong>
            <p>{{ erroServidor }}</p>
            <p class="dica-erro">
              Verifique se o JSON está no formato correto e tente novamente.
              Se o erro persistir, confira o prompt e gere o JSON novamente com a IA.
            </p>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
// Importa as funções reativas do Vue
import { ref, computed } from 'vue'

// Importa o router para navegação e logout
import { useRouter } from 'vue-router'

// Importa o serviço de API configurado com interceptors JWT
import api from '../services/api.js'

const router = useRouter()

// ==========================================
// Estado reativo da página
// ==========================================

// Texto digitado/colado na textarea
const jsonTexto = ref('')

// Estados de feedback
const importando = ref(false)      // Requisição em andamento
const erroValidacao = ref('')      // Erro de validação local (antes de enviar)
const erroServidor = ref('')       // Erro retornado pelo backend
const resultado = ref(null)        // Resultado da importação bem-sucedida
const promptCopiado = ref(false)   // Controla feedback do botão "Copiar prompt"

// ==========================================
// Prompt completo para copiar
// O professor cola isso no ChatGPT/Claude e preenche os campos
// ==========================================
const PROMPT_COMPLETO = `Você é um especialista em elaboração de questões no padrão ENEM, com foco em avaliação de competências e habilidades.
Gere [QUANTIDADE_DE_QUESTOES] questões da disciplina [MATERIA_NOME] com alto nível de qualidade pedagógica, seguindo rigorosamente o formato JSON especificado.

IMPORTANTE:
* Responda APENAS com o JSON, sem qualquer texto antes ou depois
* Não use blocos de código markdown
* Siga EXATAMENTE a estrutura do JSON fornecido
* Todas as questões devem ter 5 alternativas (A, B, C, D, E)
* Não deixe nenhum campo obrigatório vazio
* O JSON deve ser válido e pronto para inserção direta em banco de dados (sem erros de sintaxe)

PADRÃO ENEM (OBRIGATÓRIO):
* As questões devem ser contextualizadas, com situações reais, científicas ou do cotidiano
* Sempre que possível, utilizar pequenos textos-base, dados, experimentos ou problematizações
* Evitar perguntas diretas e puramente conceituais
* Priorizar interpretação, análise e aplicação de conhecimento

QUALIDADE DAS ALTERNATIVAS:
* Apenas UMA alternativa deve estar correta
* As alternativas incorretas devem ser plausíveis e próximas da correta
* Evitar alternativas óbvias ou absurdas
* Evitar padrões previsíveis de resposta (ex: sempre letra C)

DIFICULDADE (OBRIGATÓRIO):
* Distribuir entre F, M e D de forma equilibrada
* F (Fácil): reconhecimento direto de conceito em contexto
* M (Médio): exige interpretação ou aplicação
* D (Difícil): exige análise, integração de conceitos ou raciocínio crítico

DISTRIBUIÇÃO DE TEMAS:
* Garantir variedade dentro da disciplina [MATERIA_NOME]
* Cobrir diferentes tópicos relevantes da matéria
* Evitar repetição excessiva de um mesmo tema

EXPLICAÇÃO (MUITO IMPORTANTE):
* Explicar claramente por que a alternativa correta está certa
* Sempre que possível, explicar por que as outras estão incorretas
* Linguagem didática, como um professor explicando

PADRONIZAÇÃO:
* O enunciado deve ser claro, completo e independente (sem depender de contexto externo)
* Não repetir estruturas de questões
* Não usar linguagem ambígua
* Não usar termos vagos como "sempre" ou "nunca" sem justificativa científica

CAMPOS:
* Use corretamente o código da matéria em "materia": [CODIGO_MATERIA] (MAT, PORT, BIO, QUI, FIS, GEO, HIS, ART, EDF, INF)
* Preencha o campo "tema" de forma específica (ex: "Funções do 2º grau", "Interpretação de texto", "Revolução Francesa")
* "fonte" deve ser: "Questão gerada por IA"
* "ano_origem" deve ser null

FORMATO OBRIGATÓRIO:
{
  "simulado": {
    "titulo": "[TITULO_DO_SIMULADO]",
    "descricao": "[DESCRICAO_DO_SIMULADO]",
    "data_inicio": null,
    "data_fim": null
  },
  "questoes": [
    {
      "ordem": 1,
      "enunciado": "Texto completo da questão aqui.",
      "imagem_enunciado": null,
      "opcao_a": "Texto da alternativa A",
      "opcao_b": "Texto da alternativa B",
      "opcao_c": "Texto da alternativa C",
      "opcao_d": "Texto da alternativa D",
      "opcao_e": "Texto da alternativa E",
      "resposta_correta": "A",
      "explicacao": "Explicação detalhada do porquê a alternativa correta está certa.",
      "dificuldade": "M",
      "tema": "Nome do tema específico",
      "materia": "[CODIGO_MATERIA]",
      "fonte": "Questão gerada por IA",
      "ano_origem": null
    }
  ]
}

Gere as questões agora.`

// ==========================================
// Computed: analisa o JSON em tempo real
// ==========================================

// Tenta parsear o JSON da textarea e retorna status visual
const statusJson = computed(() => {
  if (!jsonTexto.value.trim()) {
    return { tipo: '', mensagem: '' }
  }
  try {
    JSON.parse(jsonTexto.value)
    return { tipo: 'valido', mensagem: '✓ JSON válido' }
  } catch (e) {
    return { tipo: 'invalido', mensagem: '✗ JSON inválido — verifique a formatação' }
  }
})

// Conta quantas questões foram detectadas no JSON
const questoesDetectadas = computed(() => {
  try {
    const parsed = JSON.parse(jsonTexto.value)
    return parsed?.questoes?.length || 0
  } catch {
    return 0
  }
})

// O botão de importar só fica ativo quando o JSON é válido e não há resultado ainda
const podeImportar = computed(() => {
  return statusJson.value.tipo === 'valido' && !resultado.value
})

// ==========================================
// Ações do usuário
// ==========================================

// Copia o prompt completo para o clipboard do usuário
async function copiarPrompt() {
  try {
    // navigator.clipboard só funciona em HTTPS ou localhost
    await navigator.clipboard.writeText(PROMPT_COMPLETO)

    // Feedback visual temporário no botão
    promptCopiado.value = true
    setTimeout(() => {
      promptCopiado.value = false
    }, 3000)

  } catch (e) {
    // Fallback caso o clipboard não funcione (alguns browsers bloqueiam)
    console.error('Erro ao copiar:', e)
    alert('Não foi possível copiar automaticamente. Selecione o texto do prompt manualmente.')
  }
}

// Valida o JSON localmente e envia para a API
async function importar() {
  // Limpa estados anteriores
  erroValidacao.value = ''
  erroServidor.value = ''
  resultado.value = null

  // Valida o JSON antes de enviar
  let parsedJson
  try {
    parsedJson = JSON.parse(jsonTexto.value)
  } catch (e) {
    erroValidacao.value = 'O texto colado não é um JSON válido. Verifique se copiou tudo corretamente.'
    return
  }

  // Validações estruturais básicas antes de enviar ao servidor
  // Isso poupa uma viagem desnecessária à API
  if (!parsedJson.simulado) {
    erroValidacao.value = 'O JSON precisa ter um campo "simulado" com título e descrição.'
    return
  }
  if (!parsedJson.simulado.titulo) {
    erroValidacao.value = 'O simulado precisa ter um "titulo".'
    return
  }
  if (!parsedJson.questoes || !Array.isArray(parsedJson.questoes)) {
    erroValidacao.value = 'O JSON precisa ter um campo "questoes" com uma lista de questões.'
    return
  }
  if (parsedJson.questoes.length === 0) {
    erroValidacao.value = 'A lista de questões está vazia.'
    return
  }

  // Ativa o estado de carregamento
  importando.value = true

  try {
    // Envia para o endpoint do importador
    // O backend valida cada campo e cria Simulado + Questoes + SimuladoQuestao
    const response = await api.post('/importar/', parsedJson)

    // Salva o relatório retornado pelo backend para exibir na tela
    resultado.value = response.data

  } catch (error) {
    // Extrai a mensagem de erro do backend se disponível
    if (error.response?.data?.error) {
      erroServidor.value = error.response.data.error
    } else if (error.response?.data?.detail) {
      erroServidor.value = error.response.data.detail
    } else if (typeof error.response?.data === 'string') {
      erroServidor.value = error.response.data
    } else {
      erroServidor.value = 'Erro inesperado. Tente novamente ou verifique o JSON.'
    }

  } finally {
    // Desativa o carregamento independente do resultado
    importando.value = false
  }
}

// Reinicia o formulário para uma nova importação
function reiniciar() {
  jsonTexto.value = ''
  resultado.value = null
  erroValidacao.value = ''
  erroServidor.value = ''
}

// Logout — remove tokens e redireciona para o login
function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_role')
  router.push({ name: 'login' })
}
</script>

<style scoped>
/* ============================================
   Layout base
   ============================================ */
.importar {
  min-height: 100vh;
  background: #f5f5f5;
}

/* Navbar — mesmo padrão do resto do sistema */
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
.nav-links {
  display: flex;
  align-items: center;
  gap: 24px;
}
.nav-links a {
  color: white;
  text-decoration: none;
  font-size: 14px;
  opacity: 0.9;
}
.btn-logout {
  background: rgba(255,255,255,0.2);
  color: white;
  border: 1px solid rgba(255,255,255,0.4);
  padding: 6px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

/* Container principal */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 20px;
}

/* Cabeçalho da página */
.page-header {
  margin-bottom: 32px;
}
.page-header h2 {
  font-size: 26px;
  color: #333;
  margin-bottom: 8px;
}
.subtitulo {
  color: #666;
  font-size: 15px;
  max-width: 700px;
  line-height: 1.6;
}

/* Grid de duas colunas */
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  align-items: start;
}

/* Cards base */
.card {
  background: white;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}
.card h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid #f0f0f0;
}

/* ============================================
   Coluna esquerda — guia de uso
   ============================================ */

/* Cada passo do guia */
.passo {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
}

/* Bolinha com o número do passo */
.passo-numero {
  width: 32px;
  height: 32px;
  background: #667eea;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 14px;
  flex-shrink: 0;
  margin-top: 2px;
}

.passo-conteudo strong {
  display: block;
  color: #333;
  margin-bottom: 6px;
  font-size: 15px;
}
.passo-conteudo p {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
}
.passo-conteudo code {
  background: #f0f3ff;
  color: #667eea;
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 13px;
}
.passo-conteudo a {
  color: #667eea;
  text-decoration: none;
}
.passo-conteudo a:hover {
  text-decoration: underline;
}

/* Botões de link para as IAs */
.links-ia {
  display: flex;
  gap: 8px;
  margin-top: 10px;
}
.btn-ia {
  background: #f0f3ff;
  color: #667eea;
  border: 1px solid #c7d2fe;
  padding: 6px 14px;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  text-decoration: none;
  transition: background 0.2s;
}
.btn-ia:hover {
  background: #e0e7ff;
}

/* Prévia do prompt — mostra as primeiras linhas para o professor saber o que é */
.prompt-preview {
  background: #f8f9ff;
  border: 1px solid #e0e7ff;
  border-radius: 6px;
  padding: 12px;
  font-size: 12px;
  color: #666;
  font-family: monospace;
  line-height: 1.5;
  margin: 10px 0;
  max-height: 60px;
  overflow: hidden;
  position: relative;
}
/* Efeito fade no final da prévia — indica que há mais conteúdo */
.prompt-preview::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 24px;
  background: linear-gradient(transparent, #f8f9ff);
}

/* Botão de copiar prompt */
.btn-copiar {
  display: block;
  width: 100%;
  padding: 10px 16px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  margin-top: 10px;
  transition: background 0.2s;
}
.btn-copiar:hover { background: #5a6fd6; }

/* Estado "copiado" — feedback verde temporário */
.btn-copiar.copiado {
  background: #22c55e;
}

/* Caixa de aviso sobre revisão */
.aviso-revisao {
  background: #fffbeb;
  border: 1px solid #fde68a;
  border-radius: 8px;
  padding: 14px 16px;
  font-size: 13px;
  color: #92400e;
  line-height: 1.6;
  margin-top: 8px;
}

/* ============================================
   Coluna direita — área de importação
   ============================================ */

/* Textarea para o JSON */
.json-textarea {
  width: 100%;
  min-height: 320px;
  padding: 16px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-family: 'Courier New', Consolas, monospace;
  font-size: 12px;
  line-height: 1.6;
  color: #333;
  resize: vertical;
  outline: none;
  transition: border-color 0.2s;
  box-sizing: border-box;
}
.json-textarea:focus {
  border-color: #667eea;
}
.json-textarea::placeholder {
  color: #aaa;
}

/* Indicador de validade do JSON */
.json-status {
  margin-top: 8px;
  font-size: 13px;
  font-weight: 500;
  padding: 6px 12px;
  border-radius: 6px;
}
.json-status.valido {
  background: #f0fdf4;
  color: #16a34a;
}
.json-status.invalido {
  background: #fef2f2;
  color: #dc2626;
}

/* Contador de questões detectadas */
.contador-questoes {
  margin-top: 8px;
  font-size: 13px;
  color: #667eea;
  font-weight: 500;
}

/* Botão principal de importar */
.btn-importar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  padding: 14px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
  font-weight: 600;
  margin-top: 16px;
  transition: background 0.2s;
}
.btn-importar:hover:not(:disabled) { background: #5a6fd6; }
.btn-importar:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Spinner de carregamento dentro do botão */
.spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.4);
  border-top-color: white;
  border-radius: 50%;
  animation: girar 0.7s linear infinite;
}
@keyframes girar {
  to { transform: rotate(360deg); }
}

/* ============================================
   Caixas de feedback (sucesso e erro)
   ============================================ */
.feedback {
  margin-top: 16px;
  padding: 16px;
  border-radius: 8px;
  font-size: 14px;
}
.feedback.sucesso {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #166534;
}
.feedback.erro {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #991b1b;
}
.feedback strong {
  display: block;
  font-size: 15px;
  margin-bottom: 12px;
}
.feedback p {
  margin: 0;
  line-height: 1.5;
}

/* Resumo da importação bem-sucedida */
.resultado-resumo {
  background: white;
  border-radius: 6px;
  padding: 12px;
  margin: 12px 0;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.resumo-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}
.resumo-label { color: #666; }
.resumo-valor { font-weight: 600; color: #333; }

/* Badge amarelo de status "pendente" */
.badge-pendente {
  background: #fef3c7;
  color: #92400e;
  padding: 2px 8px;
  border-radius: 99px;
  font-size: 12px;
}

/* Lista de próximos passos */
.proximos-passos {
  margin-top: 12px;
  font-size: 13px;
}
.proximos-passos p {
  margin-bottom: 8px;
  color: #166534;
}
.proximos-passos ol {
  padding-left: 20px;
  margin: 0;
  line-height: 1.8;
}
.proximos-passos a {
  color: #15803d;
  font-weight: 500;
}

/* Dica extra no erro */
.dica-erro {
  margin-top: 8px !important;
  font-size: 12px;
  opacity: 0.8;
}

/* Botão de importar novo lote */
.btn-novo {
  margin-top: 14px;
  padding: 8px 16px;
  background: #22c55e;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  font-weight: 500;
  transition: background 0.2s;
}
.btn-novo:hover { background: #16a34a; }

/* ============================================
   Responsivo — mobile/tablet
   ============================================ */
@media (max-width: 768px) {
  /* Uma coluna em telas pequenas */
  .grid {
    grid-template-columns: 1fr;
  }
  /* A guia vai em cima, o import embaixo */
  .guia { order: 1; }
  .importacao { order: 2; }

  .navbar {
    flex-direction: column;
    gap: 12px;
    padding: 16px;
  }
}
</style>
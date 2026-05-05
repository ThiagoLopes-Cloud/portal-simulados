<template>
  <div class="dashboard-layout">
    
    <aside class="sidebar admin-sidebar">
      <div class="sidebar-header">
        <h1 class="logo-text">
          <span class="logo-white">SIMUS</span><span class="logo-accent">LAB</span>
        </h1>
        <p class="tagline">Comando Admin</p>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/admin/alunos" class="nav-link">
          <span class="icon">👥</span> Gestão de Alunos
        </router-link>
        <router-link to="/admin/importar" class="nav-link active">
          <span class="icon">📥</span> Importar Questões
        </router-link>
        <router-link to="/simulados" class="nav-link">
          <span class="icon">🎯</span> Ver Avaliações
        </router-link>
        <router-link to="/ranking" class="nav-link">
          <span class="icon">🏆</span> Ranking Geral
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <button @click="logout" class="btn-logout-clean">Sair do Sistema</button>
      </div>
    </aside>

    <main class="main-content">
      
      <header class="top-bar">
        <div class="welcome-msg">
          <h2>Motor de Inteligência Artificial</h2>
          <p class="text-secondary">Gere baterias de questões utilizando LLMs (ChatGPT/Gemini) e importe os dados estruturados.</p>
        </div>
        <div class="admin-badge">Modo Administrador</div>
      </header>

      <div class="import-grid">

        <div class="pipeline-section">
          <div class="clean-card pipeline-card">
            <h3 class="section-title">Pipeline de Geração Automática</h3>
            
            <div class="pipeline-steps">
              <div class="step-box">
                <div class="step-indicator">1</div>
                <div class="step-content">
                  <h4 class="step-title">Selecionar Motor LLM</h4>
                  <p class="step-desc">Escolha uma inteligência artificial para processar o prompt de formatação.</p>
                  <div class="ai-buttons">
                    <a href="https://chat.openai.com" target="_blank" class="btn-ai chatgpt">
                      <span class="ai-icon">⎔</span> ChatGPT ↗
                    </a>
                    <a href="https://gemini.google.com" target="_blank" class="btn-ai gemini">
                      <span class="ai-icon">✧</span> Gemini ↗
                    </a>
                  </div>
                </div>
              </div>

              <div class="step-box">
                <div class="step-indicator">2</div>
                <div class="step-content">
                  <h4 class="step-title">Copiar Engenharia de Prompt</h4>
                  <p class="step-desc">Copie o prompt base do sistema. Ele garante que a IA gere as questões no formato JSON exato que o laboratório necessita.</p>
                  
                  <div class="prompt-preview">
                    <div class="prompt-code">Você é um especialista em elaboração de questões no padrão ENEM... Gere [QUANTIDADE] questões da disciplina [MATERIA_NOME]...</div>
                    <div class="fade-overlay"></div>
                  </div>
                  
                  <button @click="copiarPrompt" class="btn-copy-action" :class="{ 'copy-success': promptCopiado }">
                    {{ promptCopiado ? '✓ Copiado para Área de Transferência' : '📋 Copiar Prompt Base' }}
                  </button>
                </div>
              </div>

              <div class="step-box">
                <div class="step-indicator">3</div>
                <div class="step-content">
                  <h4 class="step-title">Injetar Parâmetros</h4>
                  <p class="step-desc">Cole o prompt na IA escolhida e substitua as variáveis <code>[QUANTIDADE]</code> e <code>[MATERIA_NOME]</code> pelos dados da bateria desejada. Execute a geração.</p>
                </div>
              </div>

              <div class="step-box">
                <div class="step-indicator">4</div>
                <div class="step-content">
                  <h4 class="step-title">Extração e Importação</h4>
                  <p class="step-desc">Copie exclusivamente o bloco de código JSON gerado pela IA (do `{` inicial ao `}` final) e cole no terminal de importação ao lado.</p>
                </div>
              </div>
            </div>

            <div class="system-warning">
              <span class="warning-icon">⚠️</span>
              <div class="warning-text">
                <strong>Protocolo de Revisão:</strong> Questões importadas entram no estado "Pendente". A avaliação só ficará visível aos alunos após revisão manual e ativação no painel do Django Admin.
              </div>
            </div>
          </div>
        </div>

        <div class="terminal-section">
          <div class="clean-card terminal-card">
            <h3 class="section-title">Terminal de Inserção JSON</h3>

            <div class="editor-wrapper">
              <div class="editor-header">
                <span class="editor-tab">data_payload.json</span>
                <span class="editor-status" :class="statusJson.tipo" v-if="jsonTexto.trim()">
                  {{ statusJson.mensagem }}
                </span>
              </div>
              <textarea
                v-model="jsonTexto"
                class="code-textarea"
                placeholder='{
  "simulado": {
    "titulo": "Nome da Bateria",
    "descricao": "Detalhes..."
  },
  "questoes": [ ... ]
}'
                spellcheck="false"
              ></textarea>
            </div>

            <div class="detection-badge" v-if="questoesDetectadas > 0">
              <span class="detection-icon">📊</span> {{ questoesDetectadas }} questão(ões) estruturada(s) detectada(s).
            </div>

            <button @click="importar" class="btn-import-action" :disabled="!podeImportar || importando">
              <span v-if="importando" class="spinner"></span>
              {{ importando ? 'Compilando Dados...' : '🚀 Iniciar Importação' }}
            </button>

            <div v-if="erroValidacao" class="alert-box error">
              <span class="alert-icon">❌</span>
              <div class="alert-content">
                <strong>Erro de Sintaxe:</strong>
                <p>{{ erroValidacao }}</p>
              </div>
            </div>

            <div v-if="erroServidor" class="alert-box error">
              <span class="alert-icon">❌</span>
              <div class="alert-content">
                <strong>Rejeitado pelo Servidor:</strong>
                <p>{{ erroServidor }}</p>
                <p class="alert-hint">Verifique a formatação do JSON ou regenere a resposta na IA.</p>
              </div>
            </div>

            <div v-if="resultado" class="alert-box success">
              <div class="success-header">
                <span class="alert-icon">✅</span>
                <strong>Importação Concluída com Sucesso!</strong>
              </div>

              <div class="summary-box">
                <div class="summary-row">
                  <span class="summary-label">Avaliação:</span>
                  <span class="summary-value">{{ resultado.simulado_titulo }}</span>
                </div>
                <div class="summary-row">
                  <span class="summary-label">Volume:</span>
                  <span class="summary-value">{{ resultado.total_importadas }} questões</span>
                </div>
                <div class="summary-row">
                  <span class="summary-label">Status:</span>
                  <span class="status-pill pending">Aguardando Auditoria</span>
                </div>
              </div>

              <div class="next-steps">
                <strong>Próximas Ações Requeridas:</strong>
                <ol>
                  <li>Acesse as <a href="https://portal-simulados-production.up.railway.app/admin/questoes/questao/?revisado__exact=0" target="_blank">Questões Não Revisadas no Admin ↗</a></li>
                  <li>Realize a auditoria e aprove as questões.</li>
                  <li>Ative a avaliação na tela de <a href="https://portal-simulados-production.up.railway.app/admin/simulados/simulado/" target="_blank">Simulados ↗</a></li>
                </ol>
              </div>

              <button @click="reiniciar" class="btn-reset-action">
                + Preparar Novo Lote
              </button>
            </div>

          </div>
        </div>

      </div>
    </main>

    <nav class="mobile-bottom-nav">
      <router-link to="/admin/alunos" class="mnav-item"><span class="mnav-icon">👥</span><span>Alunos</span></router-link>
      <router-link to="/admin/importar" class="mnav-item"><span class="mnav-icon">📥</span><span>Importar</span></router-link>
      <router-link to="/simulados" class="mnav-item"><span class="mnav-icon">🎯</span><span>Avaliações</span></router-link>
      <router-link to="/ranking" class="mnav-item"><span class="mnav-icon">🏆</span><span>Ranking</span></router-link>
    </nav>
  </div>
</template>

<script setup>
// LÓGICA INTACTA
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'

const router = useRouter()
const jsonTexto = ref('')
const importando = ref(false)
const erroValidacao = ref('')
const erroServidor = ref('')
const resultado = ref(null)
const promptCopiado = ref(false)

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

const statusJson = computed(() => {
  if (!jsonTexto.value.trim()) return { tipo: '', mensagem: '' }
  try {
    JSON.parse(jsonTexto.value)
    return { tipo: 'valid', mensagem: 'Sintaxe Válida' }
  } catch (e) {
    return { tipo: 'invalid', mensagem: 'Sintaxe Inválida' }
  }
})

const questoesDetectadas = computed(() => {
  try {
    const parsed = JSON.parse(jsonTexto.value)
    return parsed?.questoes?.length || 0
  } catch {
    return 0
  }
})

const podeImportar = computed(() => {
  return statusJson.value.tipo === 'valid' && !resultado.value
})

async function copiarPrompt() {
  try {
    await navigator.clipboard.writeText(PROMPT_COMPLETO)
    promptCopiado.value = true
    setTimeout(() => { promptCopiado.value = false }, 3000)
  } catch (e) {
    console.error('Erro ao copiar:', e)
    alert('Não foi possível copiar automaticamente. Selecione o texto do prompt manualmente no código fonte.')
  }
}

async function importar() {
  erroValidacao.value = ''
  erroServidor.value = ''
  resultado.value = null

  let parsedJson
  try {
    parsedJson = JSON.parse(jsonTexto.value)
  } catch (e) {
    erroValidacao.value = 'Estrutura JSON malformada.'
    return
  }

  if (!parsedJson.simulado) { erroValidacao.value = 'Chave ausente: "simulado".'; return }
  if (!parsedJson.simulado.titulo) { erroValidacao.value = 'Chave ausente: "simulado.titulo".'; return }
  if (!parsedJson.questoes || !Array.isArray(parsedJson.questoes)) { erroValidacao.value = 'Chave ausente: array "questoes".'; return }
  if (parsedJson.questoes.length === 0) { erroValidacao.value = 'Array "questoes" está vazio.'; return }

  importando.value = true

  try {
    const response = await api.post('/api/importar/', parsedJson) // Atualizado para /api/
    resultado.value = response.data
  } catch (error) {
    if (error.response?.data?.error) erroServidor.value = error.response.data.error
    else if (error.response?.data?.detail) erroServidor.value = error.response.data.detail
    else if (typeof error.response?.data === 'string') erroServidor.value = error.response.data
    else erroServidor.value = 'Erro de comunicação com a API.'
  } finally {
    importando.value = false
  }
}

function reiniciar() {
  jsonTexto.value = ''
  resultado.value = null
  erroValidacao.value = ''
  erroServidor.value = ''
}

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_role')
  router.push({ name: 'login' })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap');

/* Base & Layout */
.dashboard-layout { display: flex; min-height: 100vh; width: 100vw; position: absolute; top: 0; left: 0; background-color: #F8FAFC; font-family: 'Inter', sans-serif; }
.admin-sidebar { width: 220px; background: linear-gradient(180deg, #0F172A 0%, #1E293B 100%); color: white; display: flex; flex-direction: column; padding: 30px 20px; position: fixed; height: 100vh; z-index: 100; border-right: 1px solid #334155; }
.logo-white { color: #FFFFFF; font-weight: 800; font-size: 1.3rem; }
.logo-accent { color: #38BDF8; font-weight: 800; font-size: 1.3rem; }
.tagline { font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1.2px; color: #94A3B8; margin-top: 2px; }
.sidebar-nav { margin-top: 40px; flex: 1; }
.nav-link { display: flex; align-items: center; gap: 10px; color: #94A3B8; text-decoration: none; padding: 12px 14px; border-radius: 8px; margin-bottom: 5px; font-weight: 500; font-size: 0.9rem; transition: all 0.2s; }
.nav-link:hover, .nav-link.active { background: rgba(255, 255, 255, 0.1); color: white; }
.btn-logout-clean { background: transparent; border: 1px solid #475569; color: #CBD5E1; width: 100%; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.85rem; transition: all 0.2s; }
.btn-logout-clean:hover { background: #EF4444; border-color: #EF4444; color: white; }

.main-content { flex: 1; margin-left: 220px; padding: 30px 50px; }
.top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px; }
.welcome-msg h2 { font-size: 1.7rem; font-weight: 700; color: #0F172A; margin: 0; }
.text-secondary { color: #475569; font-size: 0.9rem; margin-top: 4px; }
.admin-badge { background: #1E293B; color: white; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; padding: 5px 12px; border-radius: 20px; }

/* Utils */
.clean-card { background: white; border: 1px solid #E2E8F0; border-radius: 12px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03); padding: 30px; }
.section-title { font-size: 1.2rem; font-weight: 700; color: #0F172A; margin: 0 0 25px 0; padding-bottom: 15px; border-bottom: 1px solid #F1F5F9; }

/* Grid de Importação */
.import-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 30px; align-items: start; }

/* ==================================
   COLUNA ESQUERDA (Pipeline)
   ================================== */
.pipeline-steps { display: flex; flex-direction: column; gap: 20px; margin-bottom: 30px; }
.step-box { display: flex; gap: 15px; }
.step-indicator { width: 30px; height: 30px; background: #0052FF; color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.85rem; flex-shrink: 0; margin-top: 2px; box-shadow: 0 4px 10px rgba(0, 82, 255, 0.2); }
.step-content { flex: 1; }
.step-title { font-size: 1rem; font-weight: 700; color: #1E293B; margin: 0 0 6px 0; }
.step-desc { color: #475569; font-size: 0.9rem; line-height: 1.5; margin: 0; }
.step-desc code { background: #F1F5F9; color: #0052FF; padding: 2px 6px; border-radius: 4px; font-family: 'Fira Code', monospace; font-size: 0.8rem; font-weight: 600; }

.ai-buttons { display: flex; gap: 10px; margin-top: 12px; }
.btn-ai { display: flex; align-items: center; gap: 6px; padding: 8px 16px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; text-decoration: none; transition: all 0.2s; }
.chatgpt { background: #ECFDF5; color: #047857; border: 1px solid #A7F3D0; } .chatgpt:hover { background: #D1FAE5; }
.gemini { background: #EFF6FF; color: #1D4ED8; border: 1px solid #BFDBFE; } .gemini:hover { background: #DBEAFE; }
.ai-icon { font-size: 1.1rem; }

.prompt-preview { background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 15px; margin: 15px 0 10px 0; position: relative; overflow: hidden; }
.prompt-code { font-family: 'Fira Code', monospace; font-size: 0.75rem; color: #64748B; line-height: 1.6; height: 40px; overflow: hidden; }
.fade-overlay { position: absolute; bottom: 0; left: 0; width: 100%; height: 30px; background: linear-gradient(transparent, #F8FAFC); }

.btn-copy-action { width: 100%; background: white; border: 1px solid #0052FF; color: #0052FF; padding: 10px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; cursor: pointer; transition: all 0.2s; display: flex; justify-content: center; align-items: center; gap: 8px; }
.btn-copy-action:hover { background: #EFF6FF; }
.copy-success { background: #10B981 !important; border-color: #10B981 !important; color: white !important; }

.system-warning { display: flex; gap: 12px; background: #FFFBEB; border: 1px solid #FDE68A; padding: 15px 20px; border-radius: 8px; align-items: flex-start; }
.warning-icon { font-size: 1.2rem; }
.warning-text { font-size: 0.85rem; color: #92400E; line-height: 1.5; }

/* ==================================
   COLUNA DIREITA (Terminal)
   ================================== */
.editor-wrapper { border: 1px solid #CBD5E1; border-radius: 8px; overflow: hidden; margin-bottom: 15px; }
.editor-header { background: #F1F5F9; border-bottom: 1px solid #CBD5E1; padding: 8px 15px; display: flex; justify-content: space-between; align-items: center; }
.editor-tab { font-family: 'Fira Code', monospace; font-size: 0.75rem; font-weight: 600; color: #475569; }
.editor-status { font-size: 0.7rem; font-weight: 700; padding: 2px 8px; border-radius: 4px; text-transform: uppercase; }
.editor-status.valid { background: #DCFCE7; color: #059669; }
.editor-status.invalid { background: #FEE2E2; color: #DC2626; }

.code-textarea { width: 100%; height: 350px; padding: 15px; border: none; background: #FAFAF9; font-family: 'Fira Code', monospace; font-size: 0.85rem; color: #1E293B; line-height: 1.6; resize: vertical; outline: none; }
.code-textarea:focus { background: white; }

.detection-badge { background: #EFF6FF; color: #0052FF; padding: 8px 15px; border-radius: 6px; font-size: 0.85rem; font-weight: 600; margin-bottom: 15px; display: inline-block; }

.btn-import-action { width: 100%; background: #0052FF; color: white; border: none; padding: 15px; border-radius: 8px; font-weight: 700; font-size: 1rem; cursor: pointer; transition: all 0.2s; display: flex; justify-content: center; align-items: center; gap: 10px; }
.btn-import-action:hover:not(:disabled) { background: #0043D1; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 82, 255, 0.2); }
.btn-import-action:disabled { background: #94A3B8; cursor: not-allowed; }

.spinner { width: 18px; height: 18px; border: 2px solid rgba(255,255,255,0.3); border-top-color: white; border-radius: 50%; animation: spin 0.8s linear infinite; }
@keyframes spin { to { transform: rotate(360deg); } }

/* Alertas de Resultado */
.alert-box { margin-top: 20px; padding: 20px; border-radius: 8px; display: flex; gap: 15px; align-items: flex-start; }
.error { background: #FEF2F2; border: 1px solid #FECACA; }
.error .alert-content strong { color: #991B1B; font-size: 0.95rem; display: block; margin-bottom: 5px; }
.error .alert-content p { margin: 0; color: #B91C1C; font-size: 0.85rem; line-height: 1.5; }
.alert-hint { margin-top: 10px !important; font-size: 0.8rem !important; color: #7F1D1D !important; font-style: italic; }

.success { background: white; border: 1px solid #A7F3D0; box-shadow: 0 10px 25px rgba(16, 185, 129, 0.1); flex-direction: column; }
.success-header { display: flex; align-items: center; gap: 10px; color: #065F46; font-size: 1.1rem; border-bottom: 1px solid #D1FAE5; padding-bottom: 15px; width: 100%; }

.summary-box { background: #F0FDF4; border-radius: 8px; padding: 15px; width: 100%; display: flex; flex-direction: column; gap: 10px; }
.summary-row { display: flex; justify-content: space-between; font-size: 0.9rem; }
.summary-label { color: #065F46; font-weight: 500; }
.summary-value { color: #064E3B; font-weight: 700; }
.status-pill { background: #FEF3C7; color: #92400E; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 700; }

.next-steps { font-size: 0.85rem; color: #334155; line-height: 1.6; }
.next-steps strong { color: #0F172A; }
.next-steps a { color: #0052FF; font-weight: 600; text-decoration: none; }
.next-steps a:hover { text-decoration: underline; }

.btn-reset-action { background: transparent; border: 1px solid #10B981; color: #10B981; padding: 10px 20px; border-radius: 6px; font-weight: 600; cursor: pointer; transition: all 0.2s; width: 100%; margin-top: 10px; }
.btn-reset-action:hover { background: #ECFDF5; }

@media (max-width: 1000px) {
  .admin-sidebar { width: 70px; padding: 30px 10px; }
  .logo-text, .tagline, .nav-link span:not(.icon), .btn-logout-clean { display: none; }
  .main-content { margin-left: 70px; padding: 20px; }
  .import-grid { grid-template-columns: 1fr; }
  .pipeline-card { order: 1; }
  .terminal-card { order: 2; }
}

/* Mobile Bottom Navigation */
.mobile-bottom-nav { display: none; position: fixed; bottom: 0; left: 0; right: 0; background: white; border-top: 1px solid #E2E8F0; z-index: 200; box-shadow: 0 -4px 12px rgba(0,0,0,0.06); padding-bottom: env(safe-area-inset-bottom, 0); }
.mnav-item { flex: 1; display: flex; flex-direction: column; align-items: center; gap: 3px; padding: 10px 4px; color: #64748B; text-decoration: none; font-size: 0.6rem; font-weight: 600; background: none; border: none; cursor: pointer; font-family: inherit; transition: color 0.2s; }
.mnav-icon { font-size: 1.2rem; line-height: 1; }
.mnav-item.router-link-active { color: #0052FF; }

@media (max-width: 768px) {
  .mobile-bottom-nav { display: flex; }
  .admin-sidebar { display: none !important; }
  .main-content { margin-left: 0 !important; padding: 20px 16px 84px !important; }
  .top-bar { flex-wrap: wrap; gap: 10px; }
  .admin-badge { display: none; }
  .welcome-msg h2 { font-size: 1.3rem; }
  .ai-buttons { flex-direction: column; }
  .btn-ai { justify-content: center; }
  .code-textarea { height: 250px; }
}

@media (max-width: 480px) {
  .clean-card { padding: 20px 16px; }
  .step-box { gap: 12px; }
  .step-indicator { width: 26px; height: 26px; font-size: 0.75rem; }
}
</style>
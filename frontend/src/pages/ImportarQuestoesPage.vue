<template>
  <DashboardLayout :username="username" :is-admin="true">
    <header class="page-header">
      <div>
        <h2 class="page-title">Motor de Inteligência Artificial</h2>
        <p class="page-sub">Gere baterias de questões via LLMs e importe os dados estruturados.</p>
      </div>
      <SimuslabBadge variant="pulsar">Admin</SimuslabBadge>
    </header>

    <div class="import-grid">

      <!-- Pipeline (esquerda) -->
      <div class="pipeline-card">
        <h3 class="card-title">Pipeline de Geração Automática</h3>

        <div class="steps">
          <div class="step">
            <div class="step-num">1</div>
            <div class="step-body">
              <h4 class="step-title">Selecionar Motor LLM</h4>
              <p class="step-desc">Escolha uma IA para processar o prompt de formatação.</p>
              <div class="ai-btns">
                <a href="https://chat.openai.com" target="_blank" class="ai-btn ai-btn--gpt">ChatGPT ↗</a>
                <a href="https://gemini.google.com" target="_blank" class="ai-btn ai-btn--gem">Gemini ↗</a>
              </div>
            </div>
          </div>

          <div class="step">
            <div class="step-num">2</div>
            <div class="step-body">
              <h4 class="step-title">Copiar Engenharia de Prompt</h4>
              <p class="step-desc">Copie o prompt base. Ele garante que a IA gere no formato JSON exato.</p>
              <div class="prompt-preview">
                <div class="prompt-code">Você é um especialista em elaboração de questões no padrão ENEM... Gere [QUANTIDADE] questões da disciplina [MATERIA_NOME]...</div>
                <div class="prompt-fade" />
              </div>
              <button class="btn-copy" :class="{ 'btn-copy--ok': promptCopiado }" @click="copiarPrompt">
                <svg v-if="!promptCopiado" width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
                <svg v-else width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
                {{ promptCopiado ? 'Copiado!' : 'Copiar Prompt Base' }}
              </button>
            </div>
          </div>

          <div class="step">
            <div class="step-num">3</div>
            <div class="step-body">
              <h4 class="step-title">Injetar Parâmetros</h4>
              <p class="step-desc">Cole na IA e substitua <code>[QUANTIDADE]</code> e <code>[MATERIA_NOME]</code>. Execute.</p>
            </div>
          </div>

          <div class="step">
            <div class="step-num">4</div>
            <div class="step-body">
              <h4 class="step-title">Extração e Importação</h4>
              <p class="step-desc">Copie só o bloco JSON gerado (do <code>{"{{"}</code> ao <code>{"}}"}</code>) e cole no terminal ao lado.</p>
            </div>
          </div>
        </div>

        <div class="warning-box">
          <span class="warning-icon">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/></svg>
          </span>
          <p class="warning-text">
            <strong>Protocolo de Revisão:</strong> Questões importadas entram como "Pendente". A avaliação só ficará visível após revisão manual no Django Admin.
          </p>
        </div>
      </div>

      <!-- Terminal (direita) -->
      <div class="terminal-card">
        <h3 class="card-title">Terminal de Inserção JSON</h3>

        <div class="editor-wrap">
          <div class="editor-bar">
            <span class="editor-tab">
              <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
              data_payload.json
            </span>
            <span v-if="jsonTexto.trim()" class="editor-status" :class="statusJson.tipo === 'valid' ? 'status--ok' : 'status--fail'">
              {{ statusJson.mensagem }}
            </span>
          </div>
          <textarea
            v-model="jsonTexto"
            class="code-editor"
            spellcheck="false"
            placeholder='{
  "simulado": {
    "titulo": "Nome da Bateria",
    "descricao": "Detalhes..."
  },
  "questoes": [ ... ]
}'
          />
        </div>

        <div v-if="questoesDetectadas > 0" class="detection-badge">
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
          {{ questoesDetectadas }} questão(ões) detectada(s)
        </div>

        <SimuslabButton
          variant="primary"
          size="lg"
          block
          :loading="importando"
          :disabled="!podeImportar || importando"
          @click="importar"
        >
          Iniciar Importação
        </SimuslabButton>

        <div v-if="erroValidacao" class="alert alert--error">
          <strong>Erro de Sintaxe:</strong> {{ erroValidacao }}
        </div>
        <div v-if="erroServidor" class="alert alert--error">
          <strong>Rejeitado pelo Servidor:</strong> {{ erroServidor }}
        </div>

        <div v-if="resultado" class="alert alert--success">
          <div class="success-header">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
            Importação Concluída!
          </div>
          <div class="summary">
            <div class="summary-row"><span>Avaliação</span><span>{{ resultado.simulado_titulo }}</span></div>
            <div class="summary-row"><span>Volume</span><span>{{ resultado.total_importadas }} questões</span></div>
            <div class="summary-row"><span>Status</span><span class="pending-badge">Aguardando Auditoria</span></div>
          </div>
          <div class="next-steps">
            <strong>Próximas Ações:</strong>
            <ol>
              <li><a href="https://portal-simulados-production.up.railway.app/admin/questoes/questao/?revisado__exact=0" target="_blank">Questões Não Revisadas ↗</a></li>
              <li>Audite e aprove as questões.</li>
              <li><a href="https://portal-simulados-production.up.railway.app/admin/simulados/simulado/" target="_blank">Ative a avaliação ↗</a></li>
            </ol>
          </div>
          <SimuslabButton variant="ghost" size="sm" @click="reiniciar" class="mt-4">+ Preparar Novo Lote</SimuslabButton>
        </div>
      </div>

    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import api from '../services/api.js'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import SimuslabButton from '../components/ui/SimuslabButton.vue'
import SimuslabBadge from '../components/ui/SimuslabBadge.vue'

const username = localStorage.getItem('username') || ''
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
  try { JSON.parse(jsonTexto.value); return { tipo: 'valid', mensagem: 'Sintaxe Válida' } }
  catch { return { tipo: 'invalid', mensagem: 'Sintaxe Inválida' } }
})

const questoesDetectadas = computed(() => {
  try { return JSON.parse(jsonTexto.value)?.questoes?.length || 0 }
  catch { return 0 }
})

const podeImportar = computed(() => statusJson.value.tipo === 'valid' && !resultado.value)

async function copiarPrompt() {
  try { await navigator.clipboard.writeText(PROMPT_COMPLETO); promptCopiado.value = true; setTimeout(() => { promptCopiado.value = false }, 3000) }
  catch { alert('Erro ao copiar. Selecione o prompt manualmente.') }
}

async function importar() {
  erroValidacao.value = ''; erroServidor.value = ''; resultado.value = null
  let parsed
  try { parsed = JSON.parse(jsonTexto.value) }
  catch { erroValidacao.value = 'Estrutura JSON malformada.'; return }
  if (!parsed.simulado) { erroValidacao.value = 'Chave ausente: "simulado".'; return }
  if (!parsed.simulado.titulo) { erroValidacao.value = 'Chave ausente: "simulado.titulo".'; return }
  if (!Array.isArray(parsed.questoes) || parsed.questoes.length === 0) { erroValidacao.value = 'Array "questoes" ausente ou vazio.'; return }
  importando.value = true
  try {
    const res = await api.post('/api/importar/', parsed)
    resultado.value = res.data
  } catch (error) {
    erroServidor.value = error.response?.data?.error || error.response?.data?.detail || 'Erro de comunicação com a API.'
  } finally { importando.value = false }
}

function reiniciar() { jsonTexto.value = ''; resultado.value = null; erroValidacao.value = ''; erroServidor.value = '' }
</script>

<style scoped>
.page-header { display: flex; align-items: flex-start; justify-content: space-between; margin-bottom: var(--space-8); }
.page-title { font-family: var(--font-display); font-size: var(--text-2xl); font-weight: var(--weight-bold); color: var(--color-star); }
.page-sub { font-size: var(--text-sm); color: var(--color-comet); margin-top: var(--space-1); }

.import-grid { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-7); align-items: start; }
@media (max-width: 900px) { .import-grid { grid-template-columns: 1fr; } }

/* Shared card */
.pipeline-card, .terminal-card {
  background: var(--color-nebula);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-7);
}
.card-title { font-family: var(--font-display); font-size: var(--text-base); font-weight: var(--weight-bold); color: var(--color-star); margin-bottom: var(--space-6); padding-bottom: var(--space-4); border-bottom: 1px solid var(--color-border); }

/* Steps */
.steps { display: flex; flex-direction: column; gap: var(--space-5); margin-bottom: var(--space-6); }
.step { display: flex; gap: var(--space-4); }
.step-num { width: 28px; height: 28px; border-radius: 50%; background: var(--color-orbit); color: var(--color-cosmos); display: flex; align-items: center; justify-content: center; font-weight: var(--weight-extrabold); font-size: var(--text-xs); flex-shrink: 0; margin-top: 2px; box-shadow: 0 0 10px rgba(0,229,255,0.25); }
.step-body { flex: 1; }
.step-title { font-size: var(--text-sm); font-weight: var(--weight-bold); color: var(--color-star); margin-bottom: var(--space-1); }
.step-desc { font-size: var(--text-sm); color: var(--color-comet); line-height: var(--leading-relaxed); }
.step-desc code { background: rgba(0,229,255,0.08); color: var(--color-orbit); padding: 1px var(--space-1); border-radius: 3px; font-family: var(--font-mono); font-size: var(--text-xs); }

.ai-btns { display: flex; gap: var(--space-2); margin-top: var(--space-3); }
.ai-btn { display: flex; align-items: center; gap: var(--space-2); padding: var(--space-2) var(--space-4); border-radius: var(--radius-sm); font-size: var(--text-sm); font-weight: var(--weight-semibold); text-decoration: none; transition: all var(--transition-fast); }
.ai-btn--gpt { background: rgba(0,214,143,0.08); color: var(--color-stellar); border: 1px solid rgba(0,214,143,0.2); }
.ai-btn--gpt:hover { background: rgba(0,214,143,0.15); }
.ai-btn--gem { background: rgba(0,229,255,0.08); color: var(--color-orbit); border: 1px solid rgba(0,229,255,0.15); }
.ai-btn--gem:hover { background: rgba(0,229,255,0.15); }

.prompt-preview { background: rgba(255,255,255,0.03); border: 1px solid var(--color-border); border-radius: var(--radius-sm); padding: var(--space-3); margin: var(--space-3) 0 var(--space-2); position: relative; overflow: hidden; }
.prompt-code { font-family: var(--font-mono); font-size: var(--text-xs); color: var(--color-dust); line-height: var(--leading-relaxed); height: 38px; overflow: hidden; }
.prompt-fade { position: absolute; bottom: 0; left: 0; width: 100%; height: 28px; background: linear-gradient(transparent, var(--color-nebula)); }

.btn-copy { width: 100%; background: rgba(255,255,255,0.04); border: 1px solid var(--color-orbit); color: var(--color-orbit); padding: var(--space-2) var(--space-4); border-radius: var(--radius-sm); font-size: var(--text-sm); font-weight: var(--weight-semibold); cursor: pointer; transition: all var(--transition-fast); display: flex; align-items: center; justify-content: center; gap: 6px; }
.btn-copy:hover { background: rgba(0,229,255,0.08); }
.btn-copy--ok { background: var(--color-stellar); border-color: var(--color-stellar); color: white; }

.warning-box { display: flex; gap: var(--space-3); background: rgba(255,184,48,0.06); border: 1px solid rgba(255,184,48,0.2); border-radius: var(--radius-md); padding: var(--space-4) var(--space-5); }
.warning-icon { color: var(--color-flare); flex-shrink: 0; display: flex; align-items: flex-start; padding-top: 1px; }
.warning-text { font-size: var(--text-sm); color: var(--color-comet); line-height: var(--leading-relaxed); }

/* Terminal */
.editor-wrap { border: 1px solid var(--color-border); border-radius: var(--radius-md); overflow: hidden; margin-bottom: var(--space-4); }
.editor-bar { background: rgba(255,255,255,0.04); border-bottom: 1px solid var(--color-border); padding: var(--space-2) var(--space-4); display: flex; justify-content: space-between; align-items: center; }
.editor-tab { font-family: var(--font-mono); font-size: var(--text-xs); font-weight: var(--weight-semibold); color: var(--color-dust); display: flex; align-items: center; gap: 5px; }
.editor-status { font-size: var(--text-2xs); font-family: var(--font-mono); font-weight: var(--weight-bold); padding: 2px var(--space-2); border-radius: 3px; text-transform: uppercase; }
.status--ok   { background: var(--color-stellar-dim); border: 1px solid var(--color-stellar-border); color: var(--color-stellar); }
.status--fail { background: var(--color-nova-dim); border: 1px solid var(--color-nova-border); color: var(--color-nova); }

.code-editor { width: 100%; height: 340px; padding: var(--space-4); border: none; background: rgba(255,255,255,0.02); font-family: var(--font-mono); font-size: var(--text-xs); color: var(--color-comet); line-height: var(--leading-relaxed); resize: vertical; outline: none; }
.code-editor:focus { background: rgba(255,255,255,0.03); }

.detection-badge { background: rgba(0,229,255,0.08); border: 1px solid rgba(0,229,255,0.15); color: var(--color-orbit); padding: var(--space-2) var(--space-4); border-radius: var(--radius-sm); font-size: var(--text-sm); font-family: var(--font-mono); font-weight: var(--weight-semibold); margin-bottom: var(--space-4); display: inline-flex; align-items: center; gap: 6px; }

/* Alerts */
.alert { margin-top: var(--space-5); padding: var(--space-5); border-radius: var(--radius-md); font-size: var(--text-sm); }
.alert--error { background: var(--color-nova-dim); border: 1px solid var(--color-nova-border); color: var(--color-nova); }
.alert--error strong { color: var(--color-nova); display: block; margin-bottom: var(--space-1); }
.alert--success { background: rgba(0,214,143,0.06); border: 1px solid rgba(0,214,143,0.2); color: var(--color-comet); }

.success-header { font-family: var(--font-display); font-weight: var(--weight-bold); color: var(--color-stellar); font-size: var(--text-base); margin-bottom: var(--space-4); display: flex; align-items: center; gap: 6px; }
.summary { background: rgba(0,214,143,0.06); border-radius: var(--radius-sm); padding: var(--space-4); display: flex; flex-direction: column; gap: var(--space-2); margin-bottom: var(--space-4); }
.summary-row { display: flex; justify-content: space-between; font-size: var(--text-sm); }
.summary-row span:first-child { color: var(--color-comet); }
.summary-row span:last-child { font-weight: var(--weight-semibold); color: var(--color-star); }
.pending-badge { background: rgba(255,184,48,0.1); border: 1px solid rgba(255,184,48,0.2); color: var(--color-flare); padding: 2px var(--space-2); border-radius: var(--radius-full); font-size: var(--text-xs); font-family: var(--font-mono); font-weight: var(--weight-bold); }

.next-steps { font-size: var(--text-sm); color: var(--color-comet); line-height: var(--leading-relaxed); margin-bottom: var(--space-2); }
.next-steps strong { color: var(--color-star); }
.next-steps a { color: var(--color-orbit); font-weight: var(--weight-semibold); text-decoration: none; }
.next-steps a:hover { text-decoration: underline; }
.next-steps ol { margin: var(--space-2) 0 0 var(--space-5); display: flex; flex-direction: column; gap: var(--space-1); }

.mt-4 { margin-top: var(--space-4); }
</style>

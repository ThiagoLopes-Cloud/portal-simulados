<template>
  <DashboardLayout :username="username" :is-admin="isAdmin">
    <header class="page-header">
      <div>
        <h2 class="page-title">Salas de Comando</h2>
        <p class="page-sub">Conecte-se ao seu instrutor e acesse missões exclusivas.</p>
      </div>

      <OrbynButton v-if="isAdmin" variant="primary" size="sm" @click="mostrarCriarTurma = true">
        + Nova Turma
      </OrbynButton>
    </header>

    <div class="turmas-grid">

      <!-- Painel: Ativar código -->
      <div class="join-card">
        <div class="join-icon">◉</div>
        <h3 class="join-title">Ativar Código de Acesso</h3>
        <p class="join-sub">Recebeu um código do seu professor? Insira abaixo para destravar a sala da sua turma.</p>

        <div class="join-form">
          <input
            v-model="codigoInput"
            placeholder="Ex: A1B2C3"
            maxlength="12"
            @keyup.enter="entrarNaTurma"
            class="code-input"
          />
          <OrbynButton
            variant="primary"
            size="md"
            block
            :disabled="!codigoInput"
            @click="entrarNaTurma"
          >
            Validar Acesso
          </OrbynButton>
        </div>

        <div v-if="mensagem" class="feedback feedback--success">✓ {{ mensagem }}</div>
        <div v-if="erro" class="feedback feedback--error">⚠ {{ erro }}</div>
      </div>

      <!-- Lista de turmas -->
      <div class="turmas-card">
        <h3 class="turmas-title">Turmas Ativas</h3>

        <div v-if="carregando" class="skeleton-list">
          <div v-for="n in 3" :key="n" class="skeleton-row" />
        </div>

        <div v-else-if="turmas.length === 0" class="empty-state">
          <span class="empty-icon">◉</span>
          <p class="empty-text">Você ainda não está vinculado a nenhuma sala de comando.</p>
        </div>

        <div v-else class="turmas-list">
          <div v-for="t in turmas" :key="t.id" class="turma-row">
            <div class="turma-avatar">{{ t.nome.charAt(0).toUpperCase() }}</div>
            <div class="turma-info">
              <p class="turma-nome">{{ t.nome }}</p>
              <p class="turma-meta">{{ t.total_alunos }} aluno{{ t.total_alunos !== 1 ? 's' : '' }}</p>
            </div>
            <span v-if="isAdmin" class="turma-code">{{ t.codigo }}</span>
            <span v-else class="turma-badge">Acesso Liberado</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Modal criar turma (admin) -->
    <OrbynModal v-model="mostrarCriarTurma" title="Criar Nova Turma" size="sm">
      <div class="modal-form">
        <OrbynInput v-model="novaTurmaNome" label="Nome da Turma" placeholder="Ex: Turma A — Manhã 2025" />
        <div v-if="erroCriar" class="feedback feedback--error mt-3">{{ erroCriar }}</div>
        <div v-if="turmaCriada" class="turma-criada-box">
          <p class="turma-criada-nome">{{ turmaCriada.nome }}</p>
          <p class="turma-criada-label">Código de convite:</p>
          <p class="turma-criada-code">{{ turmaCriada.codigo }}</p>
        </div>
      </div>
      <template #footer>
        <OrbynButton variant="ghost" @click="fecharModalTurma">Cancelar</OrbynButton>
        <OrbynButton variant="primary" :loading="criandoTurma" :disabled="!novaTurmaNome || !!turmaCriada" @click="criarTurma">
          Criar Turma
        </OrbynButton>
      </template>
    </OrbynModal>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api.js'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import OrbynButton from '../components/ui/OrbynButton.vue'
import OrbynInput from '../components/ui/OrbynInput.vue'
import OrbynModal from '../components/ui/OrbynModal.vue'

const username = localStorage.getItem('username') || ''
const isAdmin = localStorage.getItem('user_role') === 'admin'

const codigoInput = ref('')
const mensagem = ref('')
const erro = ref('')
const turmas = ref([])
const carregando = ref(true)
const mostrarCriarTurma = ref(false)
const novaTurmaNome = ref('')
const criandoTurma = ref(false)
const erroCriar = ref('')
const turmaCriada = ref(null)

async function entrarNaTurma() {
  if (!codigoInput.value) return
  mensagem.value = ''
  erro.value = ''
  try {
    const res = await api.post('/api/escolas/entrar/', { codigo: codigoInput.value })
    mensagem.value = res.data.message
    codigoInput.value = ''
    await carregarTurmas()
  } catch (e) {
    erro.value = e.response?.data?.error || 'Código inválido ou expirado.'
  }
}

async function carregarTurmas() {
  carregando.value = true
  try {
    const res = await api.get('/api/escolas/minhas-turmas/')
    turmas.value = res.data
  } catch {
    // silently ignore
  } finally {
    carregando.value = false
  }
}

async function criarTurma() {
  if (!novaTurmaNome.value) return
  erroCriar.value = ''
  criandoTurma.value = true
  try {
    const res = await api.post('/api/escolas/turmas/', { nome: novaTurmaNome.value })
    turmaCriada.value = res.data
    await carregarTurmas()
  } catch (e) {
    erroCriar.value = e.response?.data?.error || 'Erro ao criar turma.'
  } finally {
    criandoTurma.value = false
  }
}

function fecharModalTurma() {
  mostrarCriarTurma.value = false
  novaTurmaNome.value = ''
  erroCriar.value = ''
  turmaCriada.value = null
}

onMounted(carregarTurmas)
</script>

<style scoped>
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: var(--space-8);
}
.page-title {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: var(--weight-bold);
  color: var(--color-star);
}
.page-sub { font-size: var(--text-sm); color: var(--color-comet); margin-top: var(--space-1); }

.turmas-grid {
  display: grid;
  grid-template-columns: 1fr 1.6fr;
  gap: var(--space-6);
}
@media (max-width: 900px) { .turmas-grid { grid-template-columns: 1fr; } }

/* Join card */
.join-card {
  background: var(--color-nebula);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-7);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--space-4);
}
.join-icon { font-size: 2rem; color: var(--color-orbit); }
.join-title { font-family: var(--font-display); font-size: var(--text-lg); font-weight: var(--weight-bold); color: var(--color-star); }
.join-sub { font-size: var(--text-sm); color: var(--color-comet); line-height: var(--leading-relaxed); }
.join-form { width: 100%; display: flex; flex-direction: column; gap: var(--space-3); }
.code-input {
  width: 100%;
  background: rgba(255,255,255,0.05);
  border: 2px dashed var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-4);
  color: var(--color-star);
  text-align: center;
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  outline: none;
  transition: all var(--transition-fast);
}
.code-input::placeholder { color: var(--color-dust); font-weight: normal; text-transform: none; font-family: var(--font-body); font-size: var(--text-sm); }
.code-input:focus { border-color: var(--color-orbit); background: rgba(0,229,255,0.05); box-shadow: 0 0 0 3px rgba(0,229,255,0.1); }

.feedback {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
}
.feedback--success { background: var(--color-stellar-dim); border: 1px solid var(--color-stellar-border); color: var(--color-stellar); }
.feedback--error   { background: var(--color-nova-dim); border: 1px solid var(--color-nova-border); color: var(--color-nova); }

/* Turmas card */
.turmas-card {
  background: var(--color-nebula);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
}
.turmas-title { font-family: var(--font-display); font-size: var(--text-base); font-weight: var(--weight-bold); color: var(--color-star); margin-bottom: var(--space-5); }

.skeleton-list { display: flex; flex-direction: column; gap: var(--space-3); }
.skeleton-row { height: 64px; background: rgba(255,255,255,0.04); border-radius: var(--radius-md); position: relative; overflow: hidden; }
.skeleton-row::after { content: ''; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent); animation: shimmer 1.5s infinite; }
@keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

.empty-state { display: flex; flex-direction: column; align-items: center; text-align: center; padding: var(--space-10) var(--space-4); gap: var(--space-3); }
.empty-icon { font-size: 2.5rem; color: var(--color-dust); opacity: 0.3; }
.empty-text { font-size: var(--text-sm); color: var(--color-dust); max-width: 260px; }

.turmas-list { display: flex; flex-direction: column; gap: var(--space-3); }
.turma-row {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4);
  border-radius: var(--radius-md);
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--color-border);
  transition: border-color var(--transition-fast);
}
.turma-row:hover { border-color: rgba(255,255,255,0.1); }
.turma-avatar {
  width: 40px; height: 40px;
  background: rgba(124,110,255,0.1);
  border: 1px solid rgba(124,110,255,0.2);
  border-radius: var(--radius-md);
  display: flex; align-items: center; justify-content: center;
  color: var(--color-pulsar);
  font-family: var(--font-display);
  font-weight: var(--weight-bold);
  font-size: var(--text-base);
  flex-shrink: 0;
}
.turma-info { flex: 1; }
.turma-nome { font-size: var(--text-sm); font-weight: var(--weight-semibold); color: var(--color-star); }
.turma-meta { font-size: var(--text-xs); color: var(--color-dust); margin-top: 2px; }
.turma-badge {
  padding: 3px var(--space-2);
  border-radius: var(--radius-full);
  background: var(--color-stellar-dim);
  border: 1px solid var(--color-stellar-border);
  color: var(--color-stellar);
  font-size: var(--text-2xs);
  font-family: var(--font-mono);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  white-space: nowrap;
}
.turma-code {
  padding: 3px var(--space-2);
  border-radius: var(--radius-sm);
  background: rgba(0,229,255,0.08);
  border: 1px solid rgba(0,229,255,0.15);
  color: var(--color-orbit);
  font-size: var(--text-xs);
  font-family: var(--font-mono);
  font-weight: var(--weight-bold);
  letter-spacing: 0.05em;
  white-space: nowrap;
}

/* Modal form */
.modal-form { display: flex; flex-direction: column; gap: var(--space-4); }
.mt-3 { margin-top: var(--space-3); }
.turma-criada-box {
  background: var(--color-stellar-dim);
  border: 1px solid var(--color-stellar-border);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  text-align: center;
}
.turma-criada-nome { font-weight: var(--weight-bold); color: var(--color-stellar); font-size: var(--text-base); }
.turma-criada-label { font-size: var(--text-xs); color: var(--color-comet); margin-top: var(--space-2); }
.turma-criada-code { font-family: var(--font-mono); font-size: var(--text-2xl); font-weight: var(--weight-bold); color: var(--color-star); letter-spacing: 0.15em; }
</style>

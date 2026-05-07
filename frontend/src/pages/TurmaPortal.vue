<template>
  <DashboardLayout :username="username" :is-admin="isAdmin">
    <header class="page-header">
      <div>
        <h2 class="page-title">Salas de Comando</h2>
        <p class="page-sub">Conecte-se ao seu instrutor e acesse missões exclusivas.</p>
      </div>

      <SimuslabButton v-if="isAdmin" variant="primary" size="sm" @click="mostrarCriarTurma = true">
        + Nova Turma
      </SimuslabButton>
    </header>

    <div class="turmas-grid">

      <!-- Painel: Ativar código -->
      <div class="join-card">
        <div class="join-icon">
          <svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        </div>
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
          <SimuslabButton
            variant="primary"
            size="md"
            block
            :disabled="!codigoInput"
            @click="entrarNaTurma"
          >
            Validar Acesso
          </SimuslabButton>
        </div>

        <div v-if="mensagem" class="feedback feedback--success">{{ mensagem }}</div>
        <div v-if="erro" class="feedback feedback--error">{{ erro }}</div>
      </div>

      <!-- Lista de turmas -->
      <div class="turmas-card">
        <h3 class="turmas-title">Turmas Ativas</h3>

        <div v-if="carregando" class="skeleton-list">
          <div v-for="n in 3" :key="n" class="skeleton-row" />
        </div>

        <div v-else-if="turmas.length === 0" class="empty-state">
          <span class="empty-icon">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
          </span>
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
    <SimuslabModal v-model="mostrarCriarTurma" title="Criar Nova Turma" size="sm">
      <div class="modal-form">
        <SimuslabInput v-model="novaTurmaNome" label="Nome da Turma" placeholder="Ex: Turma A — Manhã 2025" />
        <div v-if="erroCriar" class="feedback feedback--error mt-3">{{ erroCriar }}</div>
        <div v-if="turmaCriada" class="turma-criada-box">
          <p class="turma-criada-nome">{{ turmaCriada.nome }}</p>
          <p class="turma-criada-label">Código de convite:</p>
          <p class="turma-criada-code">{{ turmaCriada.codigo }}</p>
        </div>
      </div>
      <template #footer>
        <SimuslabButton variant="ghost" @click="fecharModalTurma">Cancelar</SimuslabButton>
        <SimuslabButton variant="primary" :loading="criandoTurma" :disabled="!novaTurmaNome || !!turmaCriada" @click="criarTurma">
          Criar Turma
        </SimuslabButton>
      </template>
    </SimuslabModal>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api.js'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import SimuslabButton from '../components/ui/SimuslabButton.vue'
import SimuslabInput from '../components/ui/SimuslabInput.vue'
import SimuslabModal from '../components/ui/SimuslabModal.vue'

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

/* ── Join card ── */
.join-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  padding: var(--space-7);
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: var(--space-4);
  box-shadow: var(--card-shadow);
}
.join-icon { color: var(--color-orbit); opacity: 0.7; }
.join-title { font-family: var(--font-display); font-size: var(--text-lg); font-weight: var(--weight-bold); color: var(--color-star); }
.join-sub { font-size: var(--text-sm); color: var(--color-comet); line-height: var(--leading-snug); }
.join-form { width: 100%; display: flex; flex-direction: column; gap: var(--space-3); }

.code-input {
  width: 100%;
  background: var(--color-bg-elevated);
  border: 2px dashed var(--color-border);
  border-radius: var(--input-radius);
  padding: var(--space-3) var(--space-4);
  color: var(--color-star);
  text-align: center;
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  outline: none;
  transition: border-color var(--duration-fast) var(--ease-out), box-shadow var(--duration-fast) var(--ease-out), background-color var(--duration-fast) var(--ease-out);
}
.code-input::placeholder { color: var(--color-dust); font-weight: var(--weight-normal); text-transform: none; font-family: var(--font-body); font-size: var(--text-sm); }
.code-input:focus { border-color: var(--color-orbit); background: var(--color-orbit-dim); box-shadow: var(--shadow-focus); }

.feedback {
  width: 100%;
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
}
.feedback--success { background: var(--color-stellar-dim); border: 1px solid var(--color-stellar-border); color: var(--color-stellar-bright); }
.feedback--error   { background: var(--color-nova-dim);    border: 1px solid var(--color-nova-border);    color: var(--color-nova); }

/* ── Turmas card ── */
.turmas-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  padding: var(--space-6);
  box-shadow: var(--card-shadow);
}
.turmas-title { font-family: var(--font-display); font-size: var(--text-base); font-weight: var(--weight-bold); color: var(--color-star); margin-bottom: var(--space-5); }

.skeleton-list { display: flex; flex-direction: column; gap: var(--space-3); }
.skeleton-row { height: 64px; background: var(--color-bg-elevated); border-radius: var(--radius-md); position: relative; overflow: hidden; }
.skeleton-row::after { content: ''; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent); animation: shimmer 1.5s infinite; }
@keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

.empty-state { display: flex; flex-direction: column; align-items: center; text-align: center; padding: var(--space-10) var(--space-4); gap: var(--space-3); }
.empty-icon { color: var(--color-border); }
.empty-text { font-size: var(--text-sm); color: var(--color-dust); max-width: 260px; }

.turmas-list { display: flex; flex-direction: column; gap: var(--space-3); }
.turma-row {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-3-5) var(--space-4);
  border-radius: var(--radius-md);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  transition: border-color var(--duration-fast) var(--ease-out), background-color var(--duration-fast) var(--ease-out);
}
.turma-row:hover { border-color: var(--color-border-hover); background: var(--color-surface-hover); }
.turma-avatar {
  width: 40px; height: 40px;
  background: var(--color-pulsar-dim);
  border: 1px solid var(--color-pulsar-border);
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
  padding: 3px var(--space-2-5);
  border-radius: var(--radius-full);
  background: var(--color-stellar-dim);
  border: 1px solid var(--color-stellar-border);
  color: var(--color-stellar-bright);
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  white-space: nowrap;
}
.turma-code {
  padding: 3px var(--space-2-5);
  border-radius: var(--radius-sm);
  background: var(--color-orbit-dim);
  border: 1px solid var(--color-orbit-border);
  color: var(--color-orbit);
  font-size: var(--text-xs);
  font-family: var(--font-mono);
  font-weight: var(--weight-bold);
  letter-spacing: var(--tracking-wide);
  white-space: nowrap;
}

/* ── Modal form ── */
.modal-form { display: flex; flex-direction: column; gap: var(--space-4); }
.mt-3 { margin-top: var(--space-3); }
.turma-criada-box {
  background: var(--color-stellar-dim);
  border: 1px solid var(--color-stellar-border);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  text-align: center;
}
.turma-criada-nome { font-weight: var(--weight-bold); color: var(--color-stellar-bright); font-size: var(--text-base); }
.turma-criada-label { font-size: var(--text-xs); color: var(--color-comet); margin-top: var(--space-2); }
.turma-criada-code { font-family: var(--font-mono); font-size: var(--text-2xl); font-weight: var(--weight-bold); color: var(--color-star); letter-spacing: 0.15em; margin-top: var(--space-1); }
</style>

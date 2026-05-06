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
  margin-bottom: 32px;
}
.page-title {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: #0f172a;
}
.page-sub { font-size: 0.875rem; color: #64748b; margin-top: 4px; }

.turmas-grid {
  display: grid;
  grid-template-columns: 1fr 1.6fr;
  gap: 24px;
}
@media (max-width: 900px) { .turmas-grid { grid-template-columns: 1fr; } }

/* Join card */
.join-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 16px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}
.join-icon { color: #93c5fd; }
.join-title { font-family: var(--font-display); font-size: 1.125rem; font-weight: 700; color: #0f172a; }
.join-sub { font-size: 0.875rem; color: #64748b; line-height: 1.55; }
.join-form { width: 100%; display: flex; flex-direction: column; gap: 12px; }
.code-input {
  width: 100%;
  background: #ffffff;
  border: 2px dashed #cbd5e1;
  border-radius: 10px;
  padding: 12px 16px;
  color: #0f172a;
  text-align: center;
  font-family: var(--font-display);
  font-size: 1.125rem;
  font-weight: 700;
  text-transform: uppercase;
  outline: none;
  transition: all 0.15s ease;
}
.code-input::placeholder { color: #94a3b8; font-weight: 400; text-transform: none; font-family: var(--font-body); font-size: 0.875rem; }
.code-input:focus { border-color: #3b82f6; background: #eff6ff; box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.15); }

.feedback {
  width: 100%;
  padding: 12px 16px;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 500;
}
.feedback--success { background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; }
.feedback--error   { background: #fef2f2; border: 1px solid #fecaca; color: #b91c1c; }

/* Turmas card */
.turmas-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}
.turmas-title { font-family: var(--font-display); font-size: 1rem; font-weight: 700; color: #0f172a; margin-bottom: 20px; }

.skeleton-list { display: flex; flex-direction: column; gap: 12px; }
.skeleton-row { height: 64px; background: #f1f5f9; border-radius: 10px; position: relative; overflow: hidden; }
.skeleton-row::after { content: ''; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent); animation: shimmer 1.5s infinite; }
@keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

.empty-state { display: flex; flex-direction: column; align-items: center; text-align: center; padding: 40px 16px; gap: 12px; }
.empty-icon { color: #cbd5e1; }
.empty-text { font-size: 0.875rem; color: #94a3b8; max-width: 260px; }

.turmas-list { display: flex; flex-direction: column; gap: 12px; }
.turma-row {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 14px 16px;
  border-radius: 10px;
  background: #f8fafc;
  border: 1px solid #e2e8f0;
  transition: border-color 0.15s ease, background 0.15s ease;
}
.turma-row:hover { border-color: #cbd5e1; background: #f1f5f9; }
.turma-avatar {
  width: 40px; height: 40px;
  background: #f5f3ff;
  border: 1px solid #ddd6fe;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  color: #7c3aed;
  font-family: var(--font-display);
  font-weight: 700;
  font-size: 1rem;
  flex-shrink: 0;
}
.turma-info { flex: 1; }
.turma-nome { font-size: 0.875rem; font-weight: 600; color: #0f172a; }
.turma-meta { font-size: 0.75rem; color: #94a3b8; margin-top: 2px; }
.turma-badge {
  padding: 3px 10px;
  border-radius: 999px;
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  color: #166534;
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  white-space: nowrap;
}
.turma-code {
  padding: 3px 10px;
  border-radius: 6px;
  background: #eff6ff;
  border: 1px solid #bfdbfe;
  color: #1d4ed8;
  font-size: 0.75rem;
  font-family: var(--font-mono);
  font-weight: 700;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

/* Modal form */
.modal-form { display: flex; flex-direction: column; gap: 16px; }
.mt-3 { margin-top: 12px; }
.turma-criada-box {
  background: #f0fdf4;
  border: 1px solid #bbf7d0;
  border-radius: 10px;
  padding: 16px;
  text-align: center;
}
.turma-criada-nome { font-weight: 700; color: #166534; font-size: 1rem; }
.turma-criada-label { font-size: 0.75rem; color: #64748b; margin-top: 8px; }
.turma-criada-code { font-family: var(--font-mono); font-size: 1.5rem; font-weight: 700; color: #0f172a; letter-spacing: 0.15em; }
</style>

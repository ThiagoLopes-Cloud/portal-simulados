<template>
  <div class="page-layout">

    <aside class="sidebar">
      <div class="mb-8">
        <h1 class="font-display text-xl font-bold">
          <span class="text-simus-cyan">SIMUS</span><span class="text-slate-50">LAB</span>
        </h1>
        <p class="tagline-text">Performance Lab</p>
      </div>
      <nav class="flex-1 space-y-1">
        <router-link to="/dashboard" class="nav-link"><span>📊</span><span class="nav-label">Dashboard</span></router-link>
        <router-link to="/simulados" class="nav-link"><span>🎯</span><span class="nav-label">Avaliações</span></router-link>
        <router-link to="/turmas" class="nav-link"><span>👥</span><span class="nav-label">Minhas Turmas</span></router-link>
        <router-link to="/ranking" class="nav-link"><span>🏆</span><span class="nav-label">Ranking</span></router-link>
      </nav>
      <button @click="logout" class="logout-btn"><span class="nav-label">Sair</span></button>
    </aside>

    <main class="main-content">
      <header class="mb-8">
        <h2 class="font-display text-2xl font-bold text-slate-50">Salas de Comando</h2>
        <p class="text-slate-400 text-sm mt-1">Conecte-se ao seu instrutor e acesse missões exclusivas.</p>
      </header>

      <div class="grid grid-cols-1 lg:grid-cols-[1fr_1.6fr] gap-6">

        <!-- Painel de código -->
        <div class="card flex flex-col items-center text-center">
          <div class="w-14 h-14 bg-simus-cyan/10 border border-simus-cyan/20 rounded-full flex items-center justify-center text-3xl mb-5">🔑</div>
          <h3 class="font-display font-bold text-slate-50 text-lg mb-2">Ativar Código de Acesso</h3>
          <p class="text-slate-400 text-sm leading-relaxed mb-7">
            Recebeu um código do seu professor? Insira abaixo para destravar a sala da sua turma.
          </p>

          <div class="w-full space-y-3">
            <input v-model="codigoInput" placeholder="Ex: A1B2C3D4" maxlength="12"
                   @keyup.enter="entrarNaTurma"
                   class="code-input" />
            <button @click="entrarNaTurma" :disabled="!codigoInput"
                    class="w-full py-3.5 rounded-xl bg-simus-cyan text-simus-bg font-display font-semibold text-sm uppercase tracking-wider
                           hover:shadow-[0_0_15px_rgba(0,229,255,0.3)] hover:scale-[1.01] transition-all
                           disabled:opacity-40 disabled:pointer-events-none">
              Validar Acesso
            </button>
          </div>

          <div v-if="mensagem" class="mt-5 w-full flex items-center justify-center gap-2 bg-emerald-500/10 border border-emerald-500/30 rounded-xl px-4 py-3">
            <span class="text-emerald-400 text-sm font-medium">✓ {{ mensagem }}</span>
          </div>
          <div v-if="erro" class="mt-5 w-full flex items-center justify-center gap-2 bg-red-500/10 border border-red-500/30 rounded-xl px-4 py-3">
            <span class="text-red-400 text-sm">⚠ {{ erro }}</span>
          </div>
        </div>

        <!-- Lista de turmas -->
        <div class="card">
          <h3 class="font-display font-bold text-slate-50 mb-5">Turmas Ativas</h3>

          <div v-if="carregando" class="space-y-3">
            <div class="shimmer h-16 rounded-xl" v-for="n in 3" :key="n" />
          </div>

          <div v-else-if="turmas.length === 0" class="flex flex-col items-center text-center py-8 gap-3">
            <span class="text-4xl opacity-30">🏫</span>
            <p class="text-slate-500 text-sm">Você ainda não está vinculado a nenhuma sala de comando.</p>
          </div>

          <div v-else class="space-y-3">
            <div v-for="t in turmas" :key="t.id"
                 class="flex items-center justify-between p-4 rounded-xl bg-white/[0.03] border border-white/5 hover:border-white/10 transition-colors">
              <div class="flex items-center gap-4">
                <div class="w-10 h-10 bg-simus-purple/10 border border-simus-purple/20 rounded-xl flex items-center justify-center
                            text-simus-purple font-display font-bold">
                  {{ t.nome.charAt(0).toUpperCase() }}
                </div>
                <div>
                  <p class="text-slate-200 font-semibold text-sm">{{ t.nome }}</p>
                  <p class="text-slate-500 text-xs mt-0.5">Prof: {{ t.professor_nome }}</p>
                </div>
              </div>
              <span class="px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20
                           text-emerald-400 text-[0.65rem] font-bold uppercase tracking-wide">
                Acesso Liberado
              </span>
            </div>
          </div>
        </div>

      </div>
    </main>

    <nav class="mobile-nav">
      <router-link to="/dashboard" class="mnav-item"><span class="text-xl">📊</span><span>Dashboard</span></router-link>
      <router-link to="/simulados" class="mnav-item"><span class="text-xl">🎯</span><span>Avaliações</span></router-link>
      <router-link to="/turmas" class="mnav-item"><span class="text-xl">👥</span><span>Turmas</span></router-link>
      <router-link to="/ranking" class="mnav-item"><span class="text-xl">🏆</span><span>Ranking</span></router-link>
    </nav>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const codigoInput = ref('')
const mensagem = ref('')
const erro = ref('')
const turmas = ref([])
const carregando = ref(true)

async function entrarNaTurma() {
  try {
    const res = await api.post('/api/escolas/entrar/', { codigo: codigoInput.value })
    mensagem.value = res.data.message
    erro.value = ''
    codigoInput.value = ''
    carregarTurmas()
  } catch (e) {
    erro.value = e.response?.data?.error || 'Código inválido ou expirado.'
    mensagem.value = ''
  }
}

async function carregarTurmas() {
  carregando.value = true
  try {
    const res = await api.get('/api/escolas/minhas-turmas/')
    turmas.value = res.data
  } catch (error) {
    console.error("Erro ao carregar turmas", error)
  } finally {
    carregando.value = false
  }
}

function logout() {
  localStorage.clear()
  router.push('/login')
}

onMounted(carregarTurmas)
</script>

<style scoped>
@reference "../assets/main.css";

.page-layout { @apply flex min-h-screen bg-simus-bg font-body; }
.sidebar {
  @apply fixed top-0 left-0 h-screen w-[220px] bg-simus-surface border-r border-white/5
         flex flex-col px-5 py-8 z-50;
}
.tagline-text { @apply text-[0.6rem] uppercase tracking-widest text-slate-500 mt-0.5; }
.nav-link {
  @apply flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm font-medium
         text-slate-400 no-underline transition-all duration-150;
}
.nav-link:hover { @apply text-slate-50 bg-white/5; }
.nav-link.router-link-exact-active {
  @apply text-simus-cyan bg-simus-cyan/10;
  border-left: 2px solid #00E5FF;
  padding-left: calc(0.75rem - 2px);
}
.logout-btn {
  @apply w-full flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl
         border border-white/10 text-slate-400 text-sm font-semibold cursor-pointer transition-colors bg-transparent;
}
.logout-btn:hover { @apply border-red-500/30 text-red-400 bg-red-500/5; }
.main-content { @apply flex-1 ml-[220px] px-8 py-8; }
.card { @apply bg-simus-surface border border-white/5 rounded-simus p-6; }

.code-input {
  @apply w-full bg-white/5 border-2 border-dashed border-white/10 rounded-xl px-4 py-3.5
         text-slate-50 text-center text-lg font-display font-bold uppercase placeholder:text-slate-600 placeholder:font-normal placeholder:normal-case
         outline-none transition-all;
}
.code-input:focus {
  @apply border-simus-cyan bg-simus-cyan/5;
  box-shadow: 0 0 0 3px rgba(0, 229, 255, 0.1);
}

.shimmer { @apply bg-white/5 relative overflow-hidden; }
.shimmer::after { content: ''; @apply absolute inset-0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent); animation: shimmer 1.5s infinite; }
@keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

.mobile-nav {
  @apply hidden fixed bottom-0 left-0 right-0 bg-simus-surface border-t border-white/5 z-50;
  padding-bottom: env(safe-area-inset-bottom, 0);
}
.mnav-item {
  @apply flex-1 flex flex-col items-center gap-1 py-2.5 px-1
         text-slate-500 no-underline text-[0.6rem] font-semibold transition-colors;
}
.mnav-item.router-link-exact-active { @apply text-simus-cyan; }

@media (max-width: 768px) {
  .mobile-nav { display: flex; }
  .sidebar { display: none !important; }
  .main-content { margin-left: 0 !important; padding: 20px 16px 84px !important; }
}
@media (min-width: 769px) and (max-width: 1024px) {
  .sidebar { width: 72px; }
  .nav-label, .tagline-text, .logout-btn span { display: none; }
  .nav-link { justify-content: center; }
  .main-content { margin-left: 72px; }
}
</style>

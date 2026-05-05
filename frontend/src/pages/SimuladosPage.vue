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
        <h2 class="font-display text-2xl font-bold text-slate-50">Central de Avaliações</h2>
        <p class="text-slate-400 text-sm mt-1">Escolha uma bateria de testes e inicie o mapeamento.</p>
      </header>

      <!-- Tabs -->
      <div class="flex gap-1 mb-8 border-b border-white/5 pb-px">
        <button class="tab-btn" :class="{ 'tab-active': activeTab === 'globais' }" @click="activeTab = 'globais'">
          🌍 Banco Global
        </button>
        <button class="tab-btn tab-vip" :class="{ 'tab-active-vip': activeTab === 'exclusivos' }" @click="activeTab = 'exclusivos'">
          🔒 Missões de Turma
          <span v-if="simuladosExclusivos.length"
                class="ml-2 px-2 py-0.5 rounded-full bg-simus-purple text-white text-[0.65rem] font-bold">
            {{ simuladosExclusivos.length }}
          </span>
        </button>
      </div>

      <!-- Skeleton -->
      <div v-if="carregando" class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
        <div class="shimmer h-52 rounded-simus" v-for="n in 3" :key="n" />
      </div>

      <div v-else>

        <!-- Global -->
        <div v-if="activeTab === 'globais'" class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
          <div v-if="simuladosGlobais.length === 0"
               class="col-span-full card flex flex-col items-center text-center py-14 border-dashed">
            <div class="w-14 h-14 bg-white/5 rounded-full flex items-center justify-center text-3xl mb-5">🌍</div>
            <h3 class="font-display text-lg font-bold text-slate-50 mb-2">Banco Global Vazio</h3>
            <p class="text-slate-400 text-sm max-w-sm">Nenhuma avaliação pública disponível no momento. O laboratório está preparando novos materiais.</p>
          </div>

          <div v-for="simulado in simuladosGlobais" :key="simulado.id"
               class="card flex flex-col justify-between hover:border-white/10 transition-colors">
            <div>
              <span class="inline-block px-2.5 py-1 rounded-lg bg-white/5 text-slate-500 text-[0.65rem] font-bold uppercase tracking-wider mb-4">
                Simulação Global
              </span>
              <h3 class="font-display text-base font-bold text-slate-50 mb-3">{{ simulado.titulo }}</h3>
              <p class="text-slate-400 text-sm leading-relaxed">
                {{ simulado.descricao || 'Bateria padrão para nivelamento de conhecimento.' }}
              </p>
            </div>
            <button @click="$router.push(`/simulado/${simulado.id}`)"
                    class="mt-6 w-full py-3 rounded-xl bg-simus-cyan text-simus-bg font-display font-semibold text-sm uppercase tracking-wider
                           hover:shadow-[0_0_15px_rgba(0,229,255,0.3)] hover:scale-[1.01] transition-all">
              Iniciar Avaliação
            </button>
          </div>
        </div>

        <!-- Exclusivos -->
        <div v-if="activeTab === 'exclusivos'" class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
          <div v-if="simuladosExclusivos.length === 0"
               class="col-span-full card flex flex-col items-center text-center py-14 border-dashed">
            <div class="w-14 h-14 bg-simus-purple/10 rounded-full flex items-center justify-center text-3xl mb-5">👥</div>
            <h3 class="font-display text-lg font-bold text-slate-50 mb-2">Acesso Restrito</h3>
            <p class="text-slate-400 text-sm max-w-sm mb-6">
              Você ainda não possui missões fechadas. Junte-se a uma turma usando um código de convite do seu professor.
            </p>
            <button @click="$router.push('/turmas')"
                    class="px-6 py-2.5 rounded-xl border border-simus-purple/30 text-simus-purple text-sm font-semibold hover:bg-simus-purple/10 transition-colors">
              Procurar Turmas
            </button>
          </div>

          <div v-for="simulado in simuladosExclusivos" :key="simulado.id"
               class="card relative overflow-hidden flex flex-col justify-between border-simus-purple/20 hover:border-simus-purple/40 transition-colors">
            <div class="absolute top-0 right-0 w-32 h-32 bg-simus-purple/[0.06] rounded-full blur-2xl pointer-events-none -translate-y-1/2 translate-x-1/2" />
            <div class="absolute top-4 right-4">
              <span class="px-2.5 py-1 rounded-full bg-simus-purple text-white text-[0.65rem] font-bold uppercase shadow-[0_0_10px_rgba(138,43,226,0.3)]">
                ⭐ Exclusivo
              </span>
            </div>
            <div class="mt-8">
              <h3 class="font-display text-base font-bold text-slate-50 mb-3">{{ simulado.titulo }}</h3>
              <p class="text-slate-400 text-sm leading-relaxed">
                {{ simulado.descricao || 'Simulação tática direcionada especificamente para o seu grupo de estudos.' }}
              </p>
            </div>
            <button @click="$router.push(`/simulado/${simulado.id}`)"
                    class="mt-6 w-full py-3 rounded-xl bg-simus-purple text-white font-display font-semibold text-sm uppercase tracking-wider
                           hover:shadow-[0_0_15px_rgba(138,43,226,0.3)] hover:scale-[1.01] transition-all">
              Acessar Missão Fechada
            </button>
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
import api from '../services/api.js'

const router = useRouter()
const carregando = ref(true)
const activeTab = ref('globais')
const simuladosGlobais = ref([])
const simuladosExclusivos = ref([])

onMounted(async () => {
  try {
    const res = await api.get('/api/simulados/')
    simuladosGlobais.value = res.data.globais || []
    simuladosExclusivos.value = res.data.exclusivos || []
  } catch (error) {
    console.error("Erro ao carregar laboratório:", error)
  } finally {
    carregando.value = false
  }
})

function logout() {
  localStorage.clear()
  router.push('/login')
}
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
         border border-white/10 text-slate-400 text-sm font-semibold
         cursor-pointer transition-colors bg-transparent;
}
.logout-btn:hover { @apply border-red-500/30 text-red-400 bg-red-500/5; }

.main-content { @apply flex-1 ml-[220px] px-8 py-8; }

.card { @apply bg-simus-surface border border-white/5 rounded-simus p-5; }

.tab-btn {
  @apply flex items-center px-4 py-3 text-sm font-semibold text-slate-500
         border-b-2 border-transparent cursor-pointer transition-all duration-150 bg-transparent;
}
.tab-btn:hover { @apply text-slate-300; }
.tab-active { @apply text-simus-cyan border-b-simus-cyan; }
.tab-vip.tab-active-vip { @apply text-simus-purple border-b-simus-purple; }

.shimmer { @apply bg-white/5 relative overflow-hidden; }
.shimmer::after {
  content: '';
  @apply absolute inset-0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent);
  animation: shimmer 1.5s infinite;
}
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

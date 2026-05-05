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
        <router-link to="/ranking" class="nav-link"><span>🏆</span><span class="nav-label">Ranking Geral</span></router-link>
        <router-link v-if="isAdmin" to="/admin/alunos" class="nav-link nav-admin"><span>🛡️</span><span class="nav-label">Admin</span></router-link>
      </nav>
      <button @click="logout" class="logout-btn"><span class="nav-label">Sair</span></button>
    </aside>

    <main class="main-content">
      <header class="mb-8">
        <h2 class="font-display text-2xl font-bold text-slate-50">Ranking Geral</h2>
        <p class="text-slate-400 text-sm mt-1">Os melhores desempenhos do laboratório.</p>
      </header>

      <div v-if="erro" class="bg-red-500/10 border border-red-500/30 text-red-400 rounded-xl px-4 py-3 text-sm">{{ erro }}</div>

      <div v-else-if="carregando" class="space-y-2">
        <div class="shimmer h-14 rounded-xl" v-for="n in 6" :key="n" />
      </div>

      <div v-else>

        <div v-if="ranking.length === 0"
             class="card flex flex-col items-center text-center py-14 border-dashed">
          <div class="w-14 h-14 bg-simus-cyan/10 rounded-full flex items-center justify-center text-3xl mb-5">🏆</div>
          <h3 class="font-display text-lg font-bold text-slate-50 mb-2">Ranking em formação.</h3>
          <p class="text-slate-400 text-sm">Seja o primeiro a completar uma avaliação e conquiste o topo do laboratório.</p>
        </div>

        <div v-else class="card overflow-hidden p-0">
          <!-- Desktop table -->
          <table class="w-full hidden sm:table">
            <thead>
              <tr class="border-b border-white/5">
                <th class="th w-16">Pos.</th>
                <th class="th">Candidato</th>
                <th class="th">Avaliação</th>
                <th class="th text-center">Acertos</th>
                <th class="th text-center">Precisão</th>
                <th class="th text-right">Data</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(item, index) in ranking" :key="index"
                  class="border-b border-white/[0.04] transition-colors hover:bg-white/[0.03]"
                  :class="{
                    'bg-[rgba(255,214,0,0.03)]': index === 0,
                    'bg-[rgba(203,213,225,0.02)]': index === 1,
                    'bg-[rgba(194,120,63,0.03)]': index === 2,
                  }">
                <td class="td text-center">
                  <div v-if="index < 3" class="w-8 h-8 rounded-full mx-auto flex items-center justify-center text-lg"
                       :class="{ 'bg-yellow-400/10': index===0, 'bg-slate-400/10': index===1, 'bg-orange-400/10': index===2 }">
                    <span v-if="index===0">🥇</span>
                    <span v-else-if="index===1">🥈</span>
                    <span v-else>🥉</span>
                  </div>
                  <span v-else class="text-slate-500 font-bold text-sm">{{ index + 1 }}º</span>
                </td>
                <td class="td">
                  <div class="flex items-center gap-3">
                    <div class="w-8 h-8 rounded-full bg-simus-cyan/10 border border-simus-cyan/20
                                flex items-center justify-center text-simus-cyan text-sm font-bold">
                      {{ item.aluno_username.charAt(0).toUpperCase() }}
                    </div>
                    <span class="text-slate-200 font-semibold text-sm">{{ item.aluno_username }}</span>
                  </div>
                </td>
                <td class="td text-slate-400 text-sm">{{ item.simulado_titulo }}</td>
                <td class="td text-center text-slate-300 font-semibold text-sm">{{ item.acertos }} / {{ item.total_questoes }}</td>
                <td class="td text-center">
                  <span class="px-2.5 py-1 rounded-full text-white text-xs font-bold" :class="corScore(item.score)">
                    {{ item.score }}%
                  </span>
                </td>
                <td class="td text-right text-slate-500 text-sm">{{ formatarData(item.realizado_em) }}</td>
              </tr>
            </tbody>
          </table>

          <!-- Mobile list -->
          <div class="sm:hidden divide-y divide-white/5">
            <div v-for="(item, index) in ranking" :key="index"
                 class="px-5 py-4 flex items-center gap-4">
              <div class="w-8 h-8 shrink-0 rounded-full flex items-center justify-center text-lg"
                   v-if="index < 3"
                   :class="{ 'bg-yellow-400/10': index===0, 'bg-slate-400/10': index===1, 'bg-orange-400/10': index===2 }">
                <span v-if="index===0">🥇</span>
                <span v-else-if="index===1">🥈</span>
                <span v-else>🥉</span>
              </div>
              <span v-else class="w-8 text-center text-slate-500 font-bold text-sm shrink-0">{{ index + 1 }}º</span>
              <div class="flex-1 min-w-0">
                <p class="text-slate-200 font-semibold text-sm">{{ item.aluno_username }}</p>
                <p class="text-slate-500 text-xs truncate">{{ item.simulado_titulo }}</p>
              </div>
              <span class="px-2.5 py-1 rounded-full text-white text-xs font-bold shrink-0" :class="corScore(item.score)">
                {{ item.score }}%
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
      <router-link v-if="isAdmin" to="/admin/alunos" class="mnav-item"><span class="text-xl">🛡️</span><span>Admin</span></router-link>
    </nav>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'

const router = useRouter()
const ranking = ref([])
const carregando = ref(true)
const erro = ref('')
const isAdmin = ref(localStorage.getItem('user_role') === 'admin')

onMounted(async () => {
  try {
    const response = await api.get('/api/resultados/ranking/')
    ranking.value = response.data
  } catch (error) {
    erro.value = 'Erro de conexão com o laboratório.'
  } finally {
    carregando.value = false
  }
})

function corScore(score) {
  const valor = parseFloat(score)
  if (valor >= 70) return 'bg-emerald-500'
  if (valor >= 50) return 'bg-amber-500'
  return 'bg-red-500'
}

function formatarData(data) {
  return new Date(data).toLocaleDateString('pt-BR')
}

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_role')
  router.push({ name: 'login' })
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
.nav-admin.router-link-exact-active { @apply text-simus-purple bg-simus-purple/10; border-left-color: #8A2BE2; }
.logout-btn {
  @apply w-full flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl
         border border-white/10 text-slate-400 text-sm font-semibold cursor-pointer transition-colors bg-transparent;
}
.logout-btn:hover { @apply border-red-500/30 text-red-400 bg-red-500/5; }
.main-content { @apply flex-1 ml-[220px] px-8 py-8; }
.card { @apply bg-simus-surface border border-white/5 rounded-simus p-5; }
.th { @apply px-5 py-3.5 text-left text-[0.7rem] font-bold text-slate-500 uppercase tracking-wider; }
.td { @apply px-5 py-4; vertical-align: middle; }

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

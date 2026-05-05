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

        <template v-if="isAdmin">
          <p class="nav-divider">Comando Admin</p>
          <router-link to="/admin/alunos" class="nav-link nav-admin"><span>🛡️</span><span class="nav-label">Gestão Alunos</span></router-link>
          <router-link to="/admin/importar" class="nav-link nav-admin"><span>📥</span><span class="nav-label">Importar Bateria</span></router-link>
        </template>
      </nav>

      <button @click="logout" class="logout-btn"><span class="nav-label">Sair</span></button>
    </aside>

    <main class="main-content">

      <!-- Header -->
      <header class="flex items-center justify-between mb-8 flex-wrap gap-4">
        <div>
          <h2 class="font-display text-2xl font-bold text-slate-50">Olá, {{ username || 'Candidato' }}</h2>
          <p class="text-slate-400 text-sm mt-1">Análise tática e evolução constante.</p>
        </div>
        <div v-if="!carregando && dados.gamificacao" class="flex items-center gap-4">
          <div class="flex flex-col items-end gap-1">
            <span class="px-2.5 py-1 rounded-lg bg-simus-cyan/10 border border-simus-cyan/20
                         text-simus-cyan text-xs font-display font-bold uppercase tracking-wider">
              NÍVEL {{ nivelAtual }}
            </span>
            <div class="w-20 h-1.5 bg-white/10 rounded-full overflow-hidden">
              <div class="h-full bg-simus-cyan" :style="{ width: progressoNivel + '%' }" />
            </div>
          </div>
          <span class="px-3 py-1.5 rounded-xl bg-orange-500/10 border border-orange-500/20 text-orange-400 text-xs font-bold">
            🔥 {{ dados.gamificacao?.ofensiva || 0 }} Dias
          </span>
        </div>
      </header>

      <!-- Erro -->
      <div v-if="erro" class="bg-red-500/10 border border-red-500/30 text-red-400 rounded-xl px-4 py-3 mb-6 text-sm">{{ erro }}</div>

      <!-- Skeleton -->
      <div v-else-if="carregando" class="space-y-6">
        <div class="shimmer h-40 rounded-simus" />
        <div class="grid grid-cols-3 gap-5">
          <div class="shimmer h-28 rounded-simus" v-for="n in 3" :key="n" />
        </div>
      </div>

      <div v-else>

        <!-- Banner Admin -->
        <section v-if="isAdmin" class="mb-8">
          <div class="card flex items-center justify-between gap-6 flex-wrap">
            <div class="flex items-center gap-4">
              <div class="w-14 h-14 bg-simus-purple/10 border border-simus-purple/20 rounded-xl flex items-center justify-center text-3xl">🛡️</div>
              <div>
                <h3 class="font-display font-bold text-slate-50 text-lg mb-1">Painel de Comando Ativo</h3>
                <p class="text-slate-400 text-sm">Acesso rápido às ferramentas de gestão e conteúdo do laboratório.</p>
              </div>
            </div>
            <div class="flex gap-3 flex-wrap">
              <button @click="$router.push('/admin/alunos')"
                      class="px-5 py-2.5 rounded-xl border border-white/10 text-slate-300 text-sm font-semibold hover:bg-white/5 transition-colors">
                👥 Base de Alunos
              </button>
              <button @click="$router.push('/admin/importar')"
                      class="px-5 py-2.5 rounded-xl bg-simus-cyan text-simus-bg text-sm font-display font-semibold uppercase tracking-wider
                             hover:shadow-[0_0_15px_rgba(0,229,255,0.3)] hover:scale-[1.02] transition-all">
                📥 Importar Questões (IA)
              </button>
            </div>
          </div>
        </section>

        <!-- Empty state -->
        <div v-if="dados.total_simulados === 0 && !isAdmin"
             class="card flex flex-col items-center text-center py-14 border-dashed">
          <div class="w-16 h-16 bg-simus-cyan/10 border border-simus-cyan/20 rounded-full flex items-center justify-center text-3xl mb-6">🎯</div>
          <h3 class="font-display text-xl font-bold text-slate-50 mb-3">Seu diagnóstico tático começa aqui.</h3>
          <p class="text-slate-400 text-sm leading-relaxed max-w-md mb-8">
            O laboratório de inteligência precisa de dados para calibrar sua estratégia.
            Realize sua primeira avaliação para destrancar seu painel de performance.
          </p>
          <button @click="$router.push('/simulados')"
                  class="px-7 py-3 rounded-xl bg-simus-cyan text-simus-bg font-display font-semibold text-sm uppercase tracking-wider
                         hover:shadow-[0_0_20px_rgba(0,229,255,0.35)] hover:scale-[1.02] transition-all">
            Iniciar Primeira Simulação
          </button>
        </div>

        <div v-if="dados.total_simulados > 0 || isAdmin" class="space-y-6">

          <!-- Recomendação tática -->
          <section v-if="recomendacaoPrincipal.titulo">
            <div class="card border-l-2 border-l-simus-cyan">
              <div class="flex items-center justify-between mb-3 flex-wrap gap-2">
                <span class="px-2.5 py-1 rounded-lg bg-simus-cyan/10 border border-simus-cyan/20
                             text-simus-cyan text-[0.65rem] font-display font-bold uppercase tracking-widest">
                  FASE 7: RECOMENDAÇÃO TÁTICA
                </span>
                <span class="flex items-center gap-1.5 text-xs font-semibold text-emerald-400">
                  <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                  Inteligência Ativa
                </span>
              </div>
              <div class="flex items-end justify-between gap-8 flex-wrap">
                <div>
                  <h3 class="font-display text-lg font-bold text-slate-50 mb-2">{{ recomendacaoPrincipal.titulo }}</h3>
                  <p class="text-slate-400 text-sm leading-relaxed max-w-xl">{{ recomendacaoPrincipal.descricao }}</p>
                </div>
                <button @click="$router.push('/simulados')"
                        class="shrink-0 px-5 py-2.5 rounded-xl bg-simus-cyan text-simus-bg text-sm font-display font-semibold uppercase tracking-wider
                               hover:shadow-[0_0_15px_rgba(0,229,255,0.3)] transition-all">
                  Executar Plano de Ação
                </button>
              </div>
            </div>
          </section>

          <!-- KPIs -->
          <div class="grid grid-cols-3 gap-5">
            <div class="card text-center">
              <span class="text-4xl font-display font-extrabold block mb-1" :class="corScoreText(dados.score_geral)">{{ dados.score_geral }}%</span>
              <span class="text-slate-500 text-xs font-semibold uppercase tracking-wider">Precisão Geral</span>
            </div>
            <div class="card text-center">
              <span class="text-4xl font-display font-extrabold text-simus-cyan block mb-1">{{ dados.total_simulados }}</span>
              <span class="text-slate-500 text-xs font-semibold uppercase tracking-wider">Simulações</span>
            </div>
            <div class="card text-center">
              <span class="text-4xl font-display font-extrabold text-simus-purple block mb-1">{{ dados.por_materia.length }}</span>
              <span class="text-slate-500 text-xs font-semibold uppercase tracking-wider">Disciplinas</span>
            </div>
          </div>

          <!-- Diagnóstico + Histórico -->
          <div class="grid grid-cols-1 lg:grid-cols-[3fr_2fr] gap-5">

            <section>
              <h3 class="text-sm font-display font-bold text-slate-400 uppercase tracking-widest mb-4">Diagnóstico de Performance</h3>
              <div class="space-y-3">
                <div v-for="materia in dados.por_materia" :key="materia.codigo"
                     class="card py-4">
                  <div class="flex items-center justify-between gap-4">
                    <div class="flex items-center gap-3 min-w-0">
                      <span class="shrink-0 px-2 py-0.5 rounded-md bg-white/5 text-slate-500 text-[0.65rem] font-bold uppercase border border-white/5">
                        {{ materia.codigo }}
                      </span>
                      <span class="text-slate-200 text-sm font-medium truncate">{{ materia.materia }}</span>
                    </div>
                    <div class="flex items-center gap-3 shrink-0">
                      <div class="w-24 h-1.5 bg-white/10 rounded-full overflow-hidden">
                        <div class="h-full rounded-full" :class="corScoreBg(materia.percentual)"
                             :style="{ width: materia.percentual + '%' }" />
                      </div>
                      <span class="text-sm font-bold w-10 text-right" :class="corScoreText(materia.percentual)">
                        {{ materia.percentual }}%
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            <section>
              <h3 class="text-sm font-display font-bold text-slate-400 uppercase tracking-widest mb-4">Atividades Recentes</h3>

              <div v-if="dados.historico.length === 0" class="card text-center py-8 text-slate-500 text-sm">
                Nenhuma atividade recente encontrada.
              </div>

              <div v-else class="card divide-y divide-white/5 overflow-hidden p-0">
                <div v-for="item in historicoComTendencia" :key="item.resultado_id"
                     class="flex items-center justify-between px-5 py-3.5 cursor-pointer group
                            hover:bg-white/[0.03] transition-colors"
                     @click="$router.push({ name: 'resultado', params: { id: item.resultado_id } })">
                  <div class="min-w-0 mr-4">
                    <p class="text-slate-200 text-sm font-medium truncate">{{ item.simulado }}</p>
                    <p class="text-slate-500 text-xs mt-0.5">{{ item.data }}</p>
                  </div>
                  <div class="flex items-center gap-3 shrink-0">
                    <span class="text-sm font-bold" :class="corScoreText(item.score)">{{ item.score }}%</span>
                    <span class="text-simus-cyan opacity-0 group-hover:opacity-100 transition-opacity text-sm font-bold">→</span>
                  </div>
                </div>
              </div>
            </section>

          </div>
        </div>
      </div>
    </main>

    <!-- Mobile nav -->
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
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'

const router = useRouter()
const username = ref('')
const carregando = ref(true)
const erro = ref('')
const isAdmin = ref(localStorage.getItem('user_role') === 'admin')

const dados = ref({
  score_geral: 0,
  total_simulados: 0,
  por_materia: [],
  historico: [],
  gamificacao: { xp: 0, ofensiva: 0 }
})

const recomendacaoPrincipal = computed(() => {
  if (!dados.value.por_materia || dados.value.por_materia.length === 0) return {}
  const piorMateria = [...dados.value.por_materia].sort((a, b) => a.percentual - b.percentual)[0]
  return {
    titulo: `Foco Estratégico: ${piorMateria.materia}`,
    descricao: `O teu desempenho nesta área está em ${piorMateria.percentual}%. Recomendamos uma bateria de exercícios focada em mapear as tuas lacunas nesta disciplina hoje.`
  }
})

const XP_POR_NIVEL = 500
const nivelAtual = computed(() => Math.floor((dados.value.gamificacao?.xp || 0) / XP_POR_NIVEL) + 1)
const xpProgresso = computed(() => (dados.value.gamificacao?.xp || 0) % XP_POR_NIVEL)
const progressoNivel = computed(() => (xpProgresso.value / XP_POR_NIVEL) * 100)

const historicoComTendencia = computed(() => {
  const mapPorSimulado = {};
  const historicoCronologico = [...dados.value.historico].reverse();
  const historicoEnriquecido = historicoCronologico.map(item => {
    let trend = null;
    if (mapPorSimulado[item.simulado_id] !== undefined) {
      const scoreAnterior = mapPorSimulado[item.simulado_id];
      const diff = parseFloat((item.score - scoreAnterior).toFixed(1));
      if (diff > 0) trend = 'up'; else if (diff < 0) trend = 'down';
    }
    mapPorSimulado[item.simulado_id] = item.score;
    return { ...item, trend };
  });
  return historicoEnriquecido.reverse();
});

onMounted(async () => {
  try {
    const [perfil, dashboard] = await Promise.all([
      api.get('/api/profile/'),
      api.get('/api/resultados/dashboard/'),
    ])
    username.value = perfil.data.username
    dados.value = dashboard.data
  } catch (error) {
    erro.value = 'Erro de conexão.'
  } finally {
    carregando.value = false
  }
})

function corScoreText(v) { return v >= 70 ? 'text-emerald-400' : v >= 50 ? 'text-amber-400' : 'text-red-400'; }
function corScoreBg(v) { return v >= 70 ? 'bg-emerald-400' : v >= 50 ? 'bg-amber-400' : 'bg-red-400'; }
function logout() { localStorage.clear(); router.push('/login'); }
</script>

<style scoped>
@reference "../assets/main.css";

.page-layout { @apply flex min-h-screen bg-simus-bg font-body; }

.sidebar {
  @apply fixed top-0 left-0 h-screen w-[220px] bg-simus-surface border-r border-white/5
         flex flex-col px-5 py-8 z-50 transition-all;
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
.nav-admin { @apply text-slate-500; }
.nav-admin.router-link-exact-active { @apply text-simus-purple bg-simus-purple/10; border-left-color: #8A2BE2; }

.nav-divider {
  @apply text-[0.6rem] uppercase tracking-widest text-slate-600 font-bold px-3 pt-5 pb-1;
}

.logout-btn {
  @apply w-full flex items-center justify-center gap-2 px-3 py-2.5 rounded-xl
         border border-white/10 text-slate-400 text-sm font-semibold
         cursor-pointer transition-colors bg-transparent;
}
.logout-btn:hover { @apply border-red-500/30 text-red-400 bg-red-500/5; }

.main-content { @apply flex-1 ml-[220px] px-8 py-8 pb-6; }

.card {
  @apply bg-simus-surface border border-white/5 rounded-simus p-5;
}

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
  .nav-label, .tagline-text, .logout-btn span, .nav-divider { display: none; }
  .nav-link { justify-content: center; }
  .main-content { margin-left: 72px; }
}
@media (max-width: 640px) {
  .grid { grid-template-columns: 1fr !important; }
}
</style>

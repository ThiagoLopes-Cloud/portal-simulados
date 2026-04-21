<template>
  <div class="dashboard-layout">
    
    <aside class="sidebar">
      <div class="sidebar-header">
        <h1 class="logo-text">
          <span class="logo-white">SIMUS</span><span class="logo-accent">LAB</span>
        </h1>
        <p class="tagline">Performance Lab</p>
      </div>

      <nav class="sidebar-nav">
        <router-link to="/dashboard" class="nav-link">
          <span class="icon">📊</span> Dashboard
        </router-link>
        <router-link to="/simulados" class="nav-link active">
          <span class="icon">🎯</span> Avaliações
        </router-link>
        <router-link to="/turmas" class="nav-link">
          <span class="icon">👥</span> Minhas Turmas
        </router-link>
        <router-link to="/ranking" class="nav-link">
          <span class="icon">🏆</span> Ranking
        </router-link>
      </nav>

      <div class="sidebar-footer">
        <button @click="logout" class="btn-logout-clean">Sair</button>
      </div>
    </aside>

    <main class="main-content">
      <header class="top-bar">
        <div class="welcome-msg">
          <h2>Central de Avaliações</h2>
          <p class="text-secondary">Escolha uma bateria de testes e inicie o mapeamento.</p>
        </div>
      </header>

      <div class="tabs-container">
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'globais' }" 
          @click="activeTab = 'globais'"
        >
          <span class="tab-icon">🌍</span> Banco Global
        </button>
        <button 
          class="tab-btn tab-exclusiva" 
          :class="{ active: activeTab === 'exclusivos' }" 
          @click="activeTab = 'exclusivos'"
        >
          <span class="tab-icon">🔒</span> Missões de Turma
          <span v-if="simuladosExclusivos.length" class="badge-count">{{ simuladosExclusivos.length }}</span>
        </button>
      </div>

      <div v-if="carregando" class="skeleton-wrapper">
        <div class="grid-simulados">
          <div class="skeleton-card shimmer" v-for="n in 3" :key="n"></div>
        </div>
      </div>
      
      <div v-else class="tab-content">
        
        <div v-if="activeTab === 'globais'" class="grid-simulados">
          <div v-if="simuladosGlobais.length === 0" class="empty-state-card clean-card">
            <div class="empty-icon-wrapper"><span class="empty-icon">🌍</span></div>
            <h3 class="empty-title">Banco Global Vazio</h3>
            <p class="empty-subtitle">Nenhuma avaliação pública disponível no momento. O laboratório está preparando novos materiais.</p>
          </div>
          
          <div v-for="simulado in simuladosGlobais" :key="simulado.id" class="eval-card clean-card">
            <div class="card-body">
              <div class="card-badge">Simulação Global</div>
              <h3 class="card-title">{{ simulado.titulo }}</h3>
              <p class="card-desc">{{ simulado.descricao || 'Bateria padrão para nivelamento de conhecimento.' }}</p>
            </div>
            <div class="card-footer">
              <button @click="$router.push(`/simulado/${simulado.id}`)" class="btn-primary-action w-100">
                Iniciar Avaliação
              </button>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'exclusivos'" class="grid-simulados">
          <div v-if="simuladosExclusivos.length === 0" class="empty-state-card clean-card">
            <div class="empty-icon-wrapper"><span class="empty-icon">👥</span></div>
            <h3 class="empty-title">Acesso Restrito</h3>
            <p class="empty-subtitle">Você ainda não possui missões fechadas. Junte-se a uma turma usando um código de convite do seu professor.</p>
            <button @click="$router.push('/turmas')" class="btn-secondary-action mt-4">Procurar Turmas</button>
          </div>
          
          <div v-for="simulado in simuladosExclusivos" :key="simulado.id" class="eval-card vip-card">
            <div class="vip-glow"></div>
            <div class="vip-tag">⭐ Exclusivo da Turma</div>
            <div class="card-body">
              <h3 class="card-title text-vip">{{ simulado.titulo }}</h3>
              <p class="card-desc">{{ simulado.descricao || 'Simulação tática direcionada especificamente para o seu grupo de estudos.' }}</p>
            </div>
            <div class="card-footer">
              <button @click="$router.push(`/simulado/${simulado.id}`)" class="btn-vip-action w-100">
                Acessar Missão Fechada
              </button>
            </div>
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup>
// LÓGICA INTACTA
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
    const res = await api.get('/api/simulados/') // Garantindo a rota /api/
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* Base & Layout */
.dashboard-layout { display: flex; min-height: 100vh; width: 100vw; position: absolute; top: 0; left: 0; background-color: #F1F5F9; font-family: 'Inter', sans-serif; }
.sidebar { width: 220px; background: linear-gradient(180deg, #0A2540 0%, #0052FF 100%); color: white; display: flex; flex-direction: column; padding: 30px 20px; position: fixed; height: 100vh; z-index: 100; }
.logo-white { color: #FFFFFF; font-weight: 800; font-size: 1.3rem; }
.logo-accent { color: #00D09C; font-weight: 800; font-size: 1.3rem; }
.tagline { font-size: 0.6rem; text-transform: uppercase; letter-spacing: 1.2px; opacity: 0.7; margin-top: 2px; }
.sidebar-nav { margin-top: 40px; flex: 1; }
.nav-link { display: flex; align-items: center; gap: 10px; color: rgba(255, 255, 255, 0.8); text-decoration: none; padding: 12px 14px; border-radius: 8px; margin-bottom: 5px; font-weight: 500; font-size: 0.9rem; transition: all 0.2s; }
.nav-link:hover, .nav-link.active { background: rgba(255, 255, 255, 0.15); color: white; }
.btn-logout-clean { background: rgba(255, 255, 255, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); color: white; width: 100%; padding: 10px; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.85rem; }

/* Main Content */
.main-content { flex: 1; margin-left: 220px; padding: 40px 50px; }
.top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
.welcome-msg h2 { font-size: 1.7rem; font-weight: 700; color: #0F172A; margin: 0; }
.text-secondary { color: #475569; font-size: 0.9rem; margin-top: 4px; }

/* Tabs */
.tabs-container { display: flex; gap: 30px; margin-bottom: 30px; border-bottom: 1px solid #E2E8F0; padding-bottom: 0; }
.tab-btn { background: none; border: none; font-size: 0.95rem; font-weight: 600; color: #64748B; padding: 12px 0; cursor: pointer; position: relative; transition: all 0.2s; display: flex; align-items: center; gap: 8px; }
.tab-icon { font-size: 1.1rem; }
.tab-btn:hover { color: #0F172A; }
.tab-btn.active { color: #0052FF; }
.tab-btn.active::after { content: ''; position: absolute; bottom: -1px; left: 0; width: 100%; height: 3px; background: #0052FF; border-radius: 3px 3px 0 0; }
.tab-exclusiva.active { color: #7C3AED; }
.tab-exclusiva.active::after { background: #7C3AED; }
.badge-count { background: #7C3AED; color: white; font-size: 0.7rem; padding: 2px 8px; border-radius: 99px; margin-left: 4px; font-weight: 800; }

/* Utilitários & Botoes */
.clean-card { background: white; border: 1px solid #E2E8F0; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
.w-100 { width: 100%; }
.mt-4 { margin-top: 20px; }
.btn-primary-action { background: #0052FF; color: white; padding: 12px 24px; border-radius: 8px; font-weight: 600; border: none; cursor: pointer; transition: all 0.2s; }
.btn-primary-action:hover { background: #0043D1; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 82, 255, 0.2); }
.btn-secondary-action { background: white; border: 1px solid #CBD5E1; padding: 10px 20px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.2s; color: #334155; }
.btn-secondary-action:hover { border-color: #0052FF; color: #0052FF; }

/* Skeleton */
.skeleton-wrapper { width: 100%; }
.shimmer { position: relative; overflow: hidden; background-color: #E2E8F0; border-radius: 16px; }
.shimmer::after { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent); animation: loading 1.5s infinite; }
@keyframes loading { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }
.skeleton-card { height: 200px; }

/* Empty States */
.empty-state-card { grid-column: 1 / -1; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center; padding: 60px; }
.empty-icon-wrapper { width: 80px; height: 80px; background: #F1F5F9; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin-bottom: 24px; }
.empty-icon { font-size: 2.5rem; }
.empty-title { font-size: 1.4rem; font-weight: 700; color: #0F172A; margin-bottom: 12px; }
.empty-subtitle { color: #64748B; max-width: 500px; font-size: 0.95rem; line-height: 1.5; }

/* Cards de Avaliação */
.grid-simulados { display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 24px; }
.eval-card { display: flex; flex-direction: column; justify-content: space-between; padding: 25px; transition: transform 0.2s, box-shadow 0.2s; }
.eval-card:hover { transform: translateY(-4px); box-shadow: 0 12px 20px -5px rgba(0, 0, 0, 0.08); }
.card-badge { display: inline-block; background: #F1F5F9; color: #475569; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; padding: 4px 10px; border-radius: 4px; margin-bottom: 15px; letter-spacing: 0.5px; }
.card-title { font-size: 1.2rem; font-weight: 700; color: #0F172A; margin: 0 0 10px 0; }
.card-desc { color: #64748B; font-size: 0.9rem; line-height: 1.5; margin: 0 0 25px 0; flex-grow: 1; }

/* VIP Card (Missão da Turma) */
.vip-card { background: white; border: 1px solid #DDD6FE; border-radius: 16px; position: relative; overflow: hidden; padding: 25px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 15px rgba(124, 58, 237, 0.05); }
.vip-glow { position: absolute; top: 0; right: 0; width: 150px; height: 150px; background: radial-gradient(circle, rgba(124,58,237,0.1) 0%, transparent 70%); border-radius: 50%; transform: translate(30%, -30%); }
.vip-tag { position: absolute; top: 15px; right: 15px; background: #7C3AED; color: white; font-size: 0.65rem; font-weight: 800; text-transform: uppercase; padding: 4px 10px; border-radius: 20px; z-index: 2; box-shadow: 0 2px 8px rgba(124, 58, 237, 0.3); }
.text-vip { color: #5B21B6; }
.btn-vip-action { background: #7C3AED; color: white; padding: 12px 24px; border-radius: 8px; font-weight: 600; border: none; cursor: pointer; transition: all 0.2s; position: relative; z-index: 2; }
.btn-vip-action:hover { background: #6D28D9; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(124, 58, 237, 0.3); }

/* Responsivo */
@media (max-width: 1000px) {
  .sidebar { width: 70px; padding: 30px 10px; }
  .logo-text, .tagline, .nav-link span:not(.icon), .btn-logout-clean { display: none; }
  .main-content { margin-left: 70px; padding: 20px; }
}
</style>
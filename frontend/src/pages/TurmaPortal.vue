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
        <router-link to="/simulados" class="nav-link">
          <span class="icon">🎯</span> Avaliações
        </router-link>
        <router-link to="/turmas" class="nav-link active">
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
          <h2>Salas de Comando</h2>
          <p class="text-secondary">Conecte-se ao seu instrutor e acesse missões exclusivas.</p>
        </div>
      </header>

      <div class="portal-grid">
        
        <div class="action-panel clean-card">
          <div class="panel-icon">🔑</div>
          <h3 class="panel-title">Ativar Código de Acesso</h3>
          <p class="panel-desc">Recebeu um código do seu professor? Insira abaixo para destravar a sala da sua turma.</p>
          
          <div class="input-action-group">
            <input 
              v-model="codigoInput" 
              placeholder="Ex: A1B2C3D4" 
              maxlength="12"
              class="code-input"
              @keyup.enter="entrarNaTurma"
            />
            <button @click="entrarNaTurma" :disabled="!codigoInput" class="btn-primary-action">
              Validar Acesso
            </button>
          </div>
          
          <div v-if="mensagem" class="alert-success">
            <span class="alert-icon">✓</span> {{ mensagem }}
          </div>
          <div v-if="erro" class="alert-error">
            <span class="alert-icon">⚠</span> {{ erro }}
          </div>
        </div>

        <div class="list-panel clean-card">
          <h3 class="section-title">Turmas Ativas</h3>
          
          <div v-if="carregando" class="skeleton-list">
            <div class="shimmer-box" v-for="n in 3" :key="n"></div>
          </div>
          
          <div v-else-if="turmas.length === 0" class="empty-list">
            <div class="empty-icon-muted">🏫</div>
            <p>Você ainda não está vinculado a nenhuma sala de comando.</p>
          </div>

          <div v-else class="turmas-list">
            <div v-for="t in turmas" :key="t.id" class="turma-card">
              <div class="turma-meta">
                <div class="turma-avatar">{{ t.nome.charAt(0).toUpperCase() }}</div>
                <div class="turma-info">
                  <span class="turma-nome">{{ t.nome }}</span>
                  <span class="turma-prof">Professor: {{ t.professor_nome }}</span>
                </div>
              </div>
              <div class="turma-status">
                <span class="status-badge">Acesso Liberado</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </main>
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
    const res = await api.post('/api/escolas/entrar/', { codigo: codigoInput.value }) // Ajustado para /api/
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
    const res = await api.get('/api/escolas/minhas-turmas/') // Ajustado para /api/
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

/* Grids e Cards */
.portal-grid { display: grid; grid-template-columns: 1fr 1.5fr; gap: 30px; }
.clean-card { background: white; border: 1px solid #E2E8F0; border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); padding: 30px; }
.section-title { font-size: 1.1rem; font-weight: 700; color: #1E293B; margin-top: 0; margin-bottom: 20px; }

/* Painel de Ação (Código) */
.action-panel { display: flex; flex-direction: column; align-items: center; text-align: center; }
.panel-icon { width: 60px; height: 60px; background: #EFF6FF; color: #0052FF; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 1.8rem; margin-bottom: 20px; }
.panel-title { font-size: 1.2rem; font-weight: 700; color: #0F172A; margin-bottom: 10px; }
.panel-desc { color: #64748B; font-size: 0.9rem; line-height: 1.5; margin-bottom: 25px; }

.input-action-group { display: flex; flex-direction: column; gap: 12px; width: 100%; }
.code-input { padding: 14px; border: 2px dashed #CBD5E1; border-radius: 8px; font-size: 1.1rem; font-weight: 600; text-align: center; color: #0F172A; text-transform: uppercase; outline: none; transition: all 0.2s; }
.code-input:focus { border-color: #0052FF; background: #F8FAFC; }
.code-input::placeholder { font-weight: 500; color: #94A3B8; text-transform: none; }

.btn-primary-action { background: #0052FF; color: white; padding: 14px; border-radius: 8px; font-weight: 600; border: none; cursor: pointer; transition: all 0.2s; font-size: 1rem; }
.btn-primary-action:hover:not(:disabled) { background: #0043D1; transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0, 82, 255, 0.2); }
.btn-primary-action:disabled { opacity: 0.5; cursor: not-allowed; }

/* Alertas */
.alert-success { width: 100%; margin-top: 20px; background: #ECFDF5; border: 1px solid #A7F3D0; color: #065F46; padding: 12px; border-radius: 8px; font-size: 0.85rem; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; }
.alert-error { width: 100%; margin-top: 20px; background: #FEF2F2; border: 1px solid #FECACA; color: #991B1B; padding: 12px; border-radius: 8px; font-size: 0.85rem; font-weight: 600; display: flex; align-items: center; justify-content: center; gap: 8px; }
.alert-icon { font-weight: 800; }

/* Painel da Lista */
.empty-list { text-align: center; padding: 40px 20px; color: #94A3B8; display: flex; flex-direction: column; align-items: center; gap: 15px; }
.empty-icon-muted { font-size: 2.5rem; opacity: 0.5; }
.turmas-list { display: flex; flex-direction: column; gap: 12px; }

.turma-card { display: flex; justify-content: space-between; align-items: center; padding: 16px 20px; border: 1px solid #E2E8F0; border-radius: 12px; transition: all 0.2s; background: #F8FAFC; }
.turma-card:hover { border-color: #CBD5E1; background: white; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }

.turma-meta { display: flex; align-items: center; gap: 15px; }
.turma-avatar { width: 40px; height: 40px; background: #E0E7FF; color: #4338CA; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 1.1rem; }
.turma-info { display: flex; flex-direction: column; gap: 4px; }
.turma-nome { font-weight: 700; color: #1E293B; font-size: 1rem; }
.turma-prof { font-size: 0.8rem; color: #64748B; font-weight: 500; }

.status-badge { background: #DCFCE7; color: #16A34A; padding: 4px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; text-transform: uppercase; }

/* Skeleton */
.skeleton-list { display: flex; flex-direction: column; gap: 12px; }
.shimmer-box { height: 75px; background: #E2E8F0; border-radius: 12px; position: relative; overflow: hidden; }
.shimmer-box::after { content: ''; position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.5), transparent); animation: loading 1.5s infinite; }
@keyframes loading { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

/* Responsivo */
@media (max-width: 1000px) {
  .sidebar { width: 70px; padding: 30px 10px; }
  .logo-text, .tagline, .nav-link span:not(.icon), .btn-logout-clean { display: none; }
  .main-content { margin-left: 70px; padding: 20px; }
  .portal-grid { grid-template-columns: 1fr; }
}
</style>
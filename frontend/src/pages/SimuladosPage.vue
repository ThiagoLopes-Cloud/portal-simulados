<template>
  <DashboardLayout :username="username" :is-admin="isAdmin">
    <header class="page-header">
      <div>
        <h2 class="page-title">Central de Avaliações</h2>
        <p class="page-sub">Escolha uma bateria de testes e inicie o mapeamento.</p>
      </div>
    </header>

    <!-- Tabs -->
    <div class="tabs">
      <button class="tab" :class="{ 'tab--active': activeTab === 'globais' }" @click="activeTab = 'globais'">
        <span class="tab-icon">◎</span> Banco Global
      </button>
      <button class="tab tab--vip" :class="{ 'tab--active-vip': activeTab === 'exclusivos' }" @click="activeTab = 'exclusivos'">
        <span class="tab-icon">◆</span> Missões de Turma
        <span v-if="simuladosExclusivos.length" class="tab-badge">{{ simuladosExclusivos.length }}</span>
      </button>
    </div>

    <!-- Skeleton -->
    <div v-if="carregando" class="grid-cards">
      <div v-for="n in 3" :key="n" class="skeleton-card" />
    </div>

    <div v-else>
      <!-- Global -->
      <div v-if="activeTab === 'globais'" class="grid-cards">
        <div v-if="simuladosGlobais.length === 0" class="empty-state">
          <div class="empty-icon">◎</div>
          <h3 class="empty-title">Banco Global Vazio</h3>
          <p class="empty-sub">Nenhuma avaliação pública disponível no momento.</p>
        </div>

        <div v-for="simulado in simuladosGlobais" :key="simulado.id" class="simulado-card">
          <div>
            <span class="card-tag">Simulação Global</span>
            <h3 class="card-title">{{ simulado.titulo }}</h3>
            <p class="card-desc">{{ simulado.descricao || 'Bateria padrão para nivelamento de conhecimento.' }}</p>
          </div>
          <SimuslabButton
            variant="primary"
            size="md"
            block
            class="card-cta"
            @click="$router.push(`/simulado/${simulado.id}`)"
          >
            Iniciar Avaliação
          </SimuslabButton>
        </div>
      </div>

      <!-- Exclusivos -->
      <div v-if="activeTab === 'exclusivos'" class="grid-cards">
        <div v-if="simuladosExclusivos.length === 0" class="empty-state">
          <div class="empty-icon" style="color: #7c3aed">◆</div>
          <h3 class="empty-title">Acesso Restrito</h3>
          <p class="empty-sub">
            Você ainda não possui missões fechadas. Junte-se a uma turma com um código de convite.
          </p>
          <SimuslabButton variant="ghost" size="sm" @click="$router.push('/turmas')" class="mt-5">
            Procurar Turmas
          </SimuslabButton>
        </div>

        <div v-for="simulado in simuladosExclusivos" :key="simulado.id" class="simulado-card simulado-card--vip">
          <div class="vip-glow" />
          <div class="vip-badge">⭐ Exclusivo</div>
          <div>
            <h3 class="card-title mt-6">{{ simulado.titulo }}</h3>
            <p class="card-desc">{{ simulado.descricao || 'Simulação tática direcionada ao seu grupo de estudos.' }}</p>
          </div>
          <SimuslabButton
            variant="secondary"
            size="md"
            block
            class="card-cta"
            @click="$router.push(`/simulado/${simulado.id}`)"
          >
            Acessar Missão
          </SimuslabButton>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api.js'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import SimuslabButton from '../components/ui/SimuslabButton.vue'

const username = localStorage.getItem('username') || ''
const isAdmin = localStorage.getItem('user_role') === 'admin'
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
    console.error('Erro ao carregar simulados:', error)
  } finally {
    carregando.value = false
  }
})
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

/* Tabs */
.tabs {
  display: flex;
  gap: 4px;
  border-bottom: 1px solid #e2e8f0;
  margin-bottom: 32px;
}
.tab {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  font-size: 0.875rem;
  font-weight: 600;
  color: #94a3b8;
  border: none;
  border-bottom: 2px solid transparent;
  background: transparent;
  cursor: pointer;
  transition: all 0.15s ease;
  margin-bottom: -1px;
}
.tab:hover { color: #475569; }
.tab--active { color: #2563eb; border-bottom-color: #2563eb; }
.tab--vip { }
.tab--active-vip { color: #7c3aed; border-bottom-color: #7c3aed; }
.tab-icon { font-size: 1rem; }
.tab-badge {
  margin-left: 4px;
  padding: 2px 8px;
  border-radius: 999px;
  background: #7c3aed;
  color: white;
  font-size: 0.65rem;
  font-weight: 700;
}

/* Grid */
.grid-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

/* Card */
.simulado-card {
  background: #ffffff;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  padding: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: 16px;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.04);
}
.simulado-card:hover { border-color: #cbd5e1; box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08); }
.simulado-card--vip { border-color: #ddd6fe; }
.simulado-card--vip:hover { border-color: #a78bfa; }

.card-tag {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 6px;
  background: #f1f5f9;
  color: #64748b;
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  margin-bottom: 16px;
}
.card-title {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 10px;
}
.card-desc { font-size: 0.875rem; color: #64748b; line-height: 1.55; }
.card-cta { margin-top: 8px; }

.vip-glow {
  position: absolute;
  top: 0; right: 0;
  width: 120px; height: 120px;
  background: rgba(124, 58, 237, 0.05);
  border-radius: 50%;
  filter: blur(20px);
  transform: translate(50%, -50%);
  pointer-events: none;
}
.vip-badge {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 3px 10px;
  border-radius: 999px;
  background: #7c3aed;
  color: white;
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
}

/* Empty state */
.empty-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 56px 32px;
  background: #ffffff;
  border: 1px dashed #e2e8f0;
  border-radius: 16px;
}
.empty-icon { font-size: 2.5rem; color: #2563eb; margin-bottom: 20px; }
.empty-title {
  font-family: var(--font-display);
  font-size: 1.125rem;
  font-weight: 700;
  color: #0f172a;
  margin-bottom: 8px;
}
.empty-sub { font-size: 0.875rem; color: #64748b; max-width: 360px; }

/* Skeleton */
.skeleton-card {
  height: 200px;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 16px;
  position: relative;
  overflow: hidden;
}
.skeleton-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.6), transparent);
  animation: shimmer 1.5s infinite;
}
@keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

.mt-5 { margin-top: 20px; }
.mt-6 { margin-top: 24px; }
</style>

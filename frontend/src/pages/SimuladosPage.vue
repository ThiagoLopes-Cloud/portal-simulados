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
          <div class="empty-icon" style="color: var(--color-pulsar)">◆</div>
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
  margin-bottom: var(--space-8);
}
.page-title {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: var(--weight-bold);
  color: var(--color-star);
}
.page-sub { font-size: var(--text-sm); color: var(--color-comet); margin-top: var(--space-1); }

/* Tabs */
.tabs {
  display: flex;
  gap: var(--space-1);
  border-bottom: 1px solid var(--color-border);
  margin-bottom: var(--space-8);
}
.tab {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-dust);
  border: none;
  border-bottom: 2px solid transparent;
  background: transparent;
  cursor: pointer;
  transition: all var(--transition-fast);
  margin-bottom: -1px;
}
.tab:hover { color: var(--color-comet); }
.tab--active { color: var(--color-orbit); border-bottom-color: var(--color-orbit); }
.tab--vip { }
.tab--active-vip { color: var(--color-pulsar); border-bottom-color: var(--color-pulsar); }
.tab-icon { font-size: 1rem; }
.tab-badge {
  margin-left: var(--space-1);
  padding: 2px var(--space-2);
  border-radius: var(--radius-full);
  background: var(--color-pulsar);
  color: white;
  font-size: var(--text-2xs);
  font-family: var(--font-mono);
  font-weight: var(--weight-bold);
}

/* Grid */
.grid-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-5);
}

/* Card */
.simulado-card {
  background: var(--color-nebula);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: var(--space-4);
  transition: border-color var(--transition-fast);
  position: relative;
  overflow: hidden;
}
.simulado-card:hover { border-color: rgba(255,255,255,0.1); }
.simulado-card--vip { border-color: var(--color-pulsar-border); }
.simulado-card--vip:hover { border-color: rgba(124,110,255,0.4); }

.card-tag {
  display: inline-block;
  padding: 3px var(--space-2);
  border-radius: var(--radius-sm);
  background: rgba(255,255,255,0.05);
  color: var(--color-dust);
  font-size: var(--text-2xs);
  font-family: var(--font-mono);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  margin-bottom: var(--space-4);
}
.card-title {
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  margin-bottom: var(--space-3);
}
.card-desc { font-size: var(--text-sm); color: var(--color-comet); line-height: var(--leading-relaxed); }
.card-cta { margin-top: var(--space-2); }

.vip-glow {
  position: absolute;
  top: 0; right: 0;
  width: 120px; height: 120px;
  background: rgba(124,110,255,0.06);
  border-radius: 50%;
  filter: blur(20px);
  transform: translate(50%, -50%);
  pointer-events: none;
}
.vip-badge {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  padding: 3px var(--space-2);
  border-radius: var(--radius-full);
  background: var(--color-pulsar);
  color: white;
  font-size: var(--text-2xs);
  font-family: var(--font-mono);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  box-shadow: 0 0 10px rgba(124,110,255,0.4);
}

/* Empty state */
.empty-state {
  grid-column: 1 / -1;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: var(--space-14) var(--space-8);
  background: var(--color-nebula);
  border: 1px dashed var(--color-border);
  border-radius: var(--radius-xl);
}
.empty-icon { font-size: 2.5rem; color: var(--color-orbit); margin-bottom: var(--space-5); }
.empty-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  margin-bottom: var(--space-2);
}
.empty-sub { font-size: var(--text-sm); color: var(--color-comet); max-width: 360px; }

/* Skeleton */
.skeleton-card {
  height: 200px;
  background: var(--color-nebula);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
}
.skeleton-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent);
  animation: shimmer 1.5s infinite;
}
@keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

.mt-5 { margin-top: var(--space-5); }
.mt-6 { margin-top: var(--space-6); }
</style>

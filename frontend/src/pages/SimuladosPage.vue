<template>
  <DashboardLayout :username="username" :is-admin="isAdmin">
    <header class="page-header">
      <div>
        <h2 class="page-title">Central de Avaliações</h2>
        <p class="page-sub">Escolha uma bateria de testes e inicie o mapeamento.</p>
      </div>
    </header>

    <!-- Tabs -->
    <SimuslabTabs
      v-model="activeTab"
      :tabs="tabs"
      class="page-tabs"
    />

    <!-- Skeleton -->
    <div v-if="carregando" class="grid-cards">
      <SimuslabSkeleton v-for="n in 3" :key="n" variant="rect" height="200px" />
    </div>

    <div v-else>
      <!-- Global -->
      <div v-if="activeTab === 'globais'" class="grid-cards">
        <SimuslabEmptyState
          v-if="simuladosGlobais.length === 0"
          icon="document"
          title="Banco Global Vazio"
          description="Nenhuma avaliação pública disponível no momento."
          color="orbit"
          card
          class="grid-full"
        />

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
        <SimuslabEmptyState
          v-if="simuladosExclusivos.length === 0"
          icon="trophy"
          title="Acesso Restrito"
          description="Você ainda não possui missões fechadas. Junte-se a uma turma com um código de convite."
          color="pulsar"
          action-label="Procurar Turmas"
          action-variant="ghost"
          action-size="sm"
          card
          class="grid-full"
          @action="$router.push('/turmas')"
        />

        <div v-for="simulado in simuladosExclusivos" :key="simulado.id" class="simulado-card simulado-card--vip">
          <div class="vip-glow" />
          <div class="vip-badge">Exclusivo</div>
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
import { ref, computed, onMounted } from 'vue'
import api from '../services/api.js'
import DashboardLayout    from '../layouts/DashboardLayout.vue'
import SimuslabButton     from '../components/ui/SimuslabButton.vue'
import SimuslabTabs       from '../components/ui/SimuslabTabs.vue'
import SimuslabSkeleton   from '../components/ui/SimuslabSkeleton.vue'
import SimuslabEmptyState from '../components/ui/SimuslabEmptyState.vue'

const username = localStorage.getItem('username') || ''
const isAdmin  = localStorage.getItem('user_role') === 'admin'
const carregando = ref(true)
const activeTab  = ref('globais')
const simuladosGlobais    = ref([])
const simuladosExclusivos = ref([])

const svgDocument = `<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/>`
const svgTrophy  = `<circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/>`

const iconOf = (paths) =>
  `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${paths}</svg>`

const tabs = computed(() => [
  { id: 'globais',    label: 'Banco Global',    icon: iconOf(svgDocument), color: 'orbit' },
  { id: 'exclusivos', label: 'Missões de Turma', icon: iconOf(svgTrophy),  color: 'pulsar',
    badge: simuladosExclusivos.value.length || undefined },
])

onMounted(async () => {
  try {
    const res = await api.get('/api/simulados/')
    simuladosGlobais.value    = res.data.globais    || []
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
  margin-bottom: var(--space-6);
}
.page-title {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: var(--weight-bold);
  color: var(--color-star);
}
.page-sub { font-size: var(--text-sm); color: var(--color-comet); margin-top: var(--space-1); }

.page-tabs { margin-bottom: var(--space-8); }

/* ── Grid ── */
.grid-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-5);
}
.grid-full { grid-column: 1 / -1; }

/* ── Card ── */
.simulado-card {
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  padding: var(--space-5);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  gap: var(--space-4);
  transition: border-color var(--duration-fast) var(--ease-out), box-shadow var(--duration-normal) var(--ease-out);
  position: relative;
  overflow: hidden;
  box-shadow: var(--card-shadow);
}
.simulado-card:hover { border-color: var(--color-border-hover); box-shadow: var(--shadow-lg); }
.simulado-card--vip { border-color: var(--color-pulsar-border); }
.simulado-card--vip:hover { border-color: var(--color-pulsar); }

.card-tag {
  display: inline-block;
  padding: 3px var(--space-2);
  border-radius: var(--radius-sm);
  background: var(--color-bg-elevated);
  color: var(--color-comet);
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  margin-bottom: var(--space-4);
}
.card-title {
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  margin-bottom: var(--space-2-5);
}
.mt-6 { margin-top: var(--space-6); }
.card-desc { font-size: var(--text-sm); color: var(--color-comet); line-height: var(--leading-snug); }
.card-cta  { margin-top: var(--space-2); }

.vip-glow {
  position: absolute;
  top: 0; right: 0;
  width: 120px; height: 120px;
  background: var(--color-pulsar-glow);
  border-radius: 50%;
  filter: blur(20px);
  transform: translate(50%, -50%);
  pointer-events: none;
}
.vip-badge {
  position: absolute;
  top: var(--space-4);
  right: var(--space-4);
  padding: 3px var(--space-2-5);
  border-radius: var(--radius-full);
  background: var(--color-pulsar);
  color: var(--color-cosmos);
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
}
</style>

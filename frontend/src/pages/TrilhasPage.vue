<template>
  <DashboardLayout :username="username" :is-admin="isAdmin">

    <!-- Header -->
    <header class="trilhas-header">
      <div>
        <h1 class="trilhas-title">Trilhas de Evolução</h1>
        <p class="trilhas-sub">Aprenda no seu ritmo. Cada aula concluída te aproxima do resultado.</p>
      </div>
      <div v-if="totalConcluidas > 0" class="trilhas-xp-badge" aria-label="`${totalConcluidas} aulas concluídas`">
        <span class="trilhas-xp-value">{{ totalConcluidas }}</span>
        <span class="trilhas-xp-label">aulas</span>
      </div>
    </header>

    <!-- Progresso geral -->
    <SimuslabProgress
      v-if="totalAulas > 0"
      :value="totalConcluidas"
      :max="totalAulas"
      label="Progresso geral"
      show-value
      color="orbit"
      size="md"
      class="trilhas-progress-wrap"
    />

    <!-- Loading -->
    <div v-if="carregando" class="trilhas-grid">
      <SimuslabSkeleton v-for="i in 6" :key="i" variant="rect" height="180px" />
    </div>

    <!-- Empty -->
    <SimuslabEmptyState
      v-else-if="!trilhas.length"
      icon="book"
      title="Nenhuma trilha disponível ainda"
      description="O professor está preparando o conteúdo para você."
      color="orbit"
      card
    />

    <!-- Grid -->
    <section v-else class="trilhas-grid">
      <TrilhaCard
        v-for="trilha in trilhas"
        :key="trilha.id"
        :trilha="trilha"
        @click="abrirTrilha(trilha)"
      />
    </section>

  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import DashboardLayout    from '../layouts/DashboardLayout.vue'
import TrilhaCard         from '../components/ui/TrilhaCard.vue'
import SimuslabProgress   from '../components/ui/SimuslabProgress.vue'
import SimuslabSkeleton   from '../components/ui/SimuslabSkeleton.vue'
import SimuslabEmptyState from '../components/ui/SimuslabEmptyState.vue'
import { aulasService }   from '../services/aulasService.js'

const router   = useRouter()
const username = localStorage.getItem('username') || ''
const isAdmin  = localStorage.getItem('user_role') === 'admin'

const trilhas    = ref([])
const carregando = ref(true)

const totalAulas      = computed(() => trilhas.value.reduce((acc, t) => acc + (t.total_aulas || 0), 0))
const totalConcluidas = computed(() => trilhas.value.reduce((acc, t) => acc + (t.aulas_concluidas || 0), 0))

onMounted(async () => {
  try {
    const { data } = await aulasService.listarTrilhas()
    trilhas.value = data
  } catch (e) {
    console.error(e)
  } finally {
    carregando.value = false
  }
})

function abrirTrilha(trilha) {
  router.push({ name: 'trilha-detalhe', params: { id: trilha.id } })
}
</script>

<style scoped>
.trilhas-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: var(--space-4);
  margin-bottom: var(--space-5);
}

.trilhas-title {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  margin-bottom: var(--space-1);
}
.trilhas-sub { font-size: var(--text-sm); color: var(--color-comet); }

.trilhas-xp-badge {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: var(--radius-xl);
  background: var(--color-orbit-dim);
  border: 1px solid var(--color-orbit-border);
}
.trilhas-xp-value {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  color: var(--color-orbit);
  line-height: 1;
}
.trilhas-xp-label {
  font-size: var(--text-2xs);
  color: var(--color-comet);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
}

.trilhas-progress-wrap {
  margin-bottom: var(--space-6);
}

.trilhas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--space-4);
  padding-bottom: var(--space-12, 48px);
}
</style>

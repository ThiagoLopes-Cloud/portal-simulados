<template>
  <DashboardLayout :username="username" :is-admin="isAdmin">

    <!-- Header -->
    <header class="page-header">
      <div>
        <h2 class="page-greeting">{{ greeting }}, {{ username || 'Candidato' }}</h2>
        <p class="page-date">{{ formattedDate }}</p>
      </div>
      <div v-if="!carregando && dados.gamificacao" class="page-badges">
        <SimuslabBadge variant="orbit">
          NÍVEL {{ nivelAtual }}
        </SimuslabBadge>
        <SimuslabBadge variant="flare" :dot="true">
          🔥 {{ dados.gamificacao?.ofensiva || 0 }} dias
        </SimuslabBadge>
        <div class="xp-bar">
          <div class="xp-fill" :style="{ width: progressoNivel + '%' }" />
        </div>
      </div>
    </header>

    <!-- Error -->
    <div v-if="erro" class="error-banner" role="alert">{{ erro }}</div>

    <!-- KPI Cards skeleton -->
    <div class="kpi-grid">
      <SimuslabKPICard
        label="Precisão Geral"
        :value="carregando ? '' : dados.score_geral + '%'"
        :loading="carregando"
        :change="scoreDelta"
        accent="orbit"
      />
      <SimuslabKPICard
        label="Simulações"
        :value="carregando ? '' : dados.total_simulados"
        :loading="carregando"
        accent="pulsar"
      />
      <SimuslabKPICard
        label="Disciplinas"
        :value="carregando ? '' : dados.por_materia.length"
        :loading="carregando"
        accent="stellar"
      />
    </div>

    <div v-if="!carregando">

      <!-- Admin panel -->
      <section v-if="isAdmin" class="section">
        <SimuslabCard accent-color="pulsar" hoverable>
          <div class="admin-panel">
            <div class="admin-panel-info">
              <SimuslabBadge variant="pulsar" size="sm">Admin</SimuslabBadge>
              <h3 class="admin-title">Painel de Comando Ativo</h3>
              <p class="admin-sub">Acesso rápido às ferramentas de gestão e conteúdo do laboratório.</p>
            </div>
            <div class="admin-actions">
              <SimuslabButton variant="ghost" size="sm" @click="$router.push('/admin/alunos')">
                Base de Alunos
              </SimuslabButton>
              <SimuslabButton variant="primary" size="sm" @click="$router.push('/admin/importar')">
                Importar Questões
              </SimuslabButton>
            </div>
          </div>
        </SimuslabCard>
      </section>

      <!-- Empty state -->
      <div v-if="dados.total_simulados === 0 && !isAdmin" class="empty-state">
        <SimuslabCard>
          <div class="empty-content">
            <div class="empty-icon">◎</div>
            <h3 class="empty-title">Seu diagnóstico tático começa aqui.</h3>
            <p class="empty-text">
              O laboratório precisa de dados para calibrar sua estratégia.
              Realize sua primeira avaliação para destrancar seu painel de performance.
            </p>
            <SimuslabButton variant="primary" @click="$router.push('/simulados')">
              Iniciar Primeira Simulação
            </SimuslabButton>
          </div>
        </SimuslabCard>
      </div>

      <div v-if="dados.total_simulados > 0 || isAdmin" class="content-grid">

        <!-- Tactical recommendation -->
        <section v-if="recomendacaoPrincipal.titulo" class="section">
          <SimuslabCard accent-color="orbit">
            <div class="recomendacao">
              <div class="recomendacao-top">
                <SimuslabBadge variant="orbit" :dot="true">FASE 7: Recomendação Tática</SimuslabBadge>
                <SimuslabBadge variant="stellar">Inteligência Ativa</SimuslabBadge>
              </div>
              <div class="recomendacao-body">
                <div>
                  <h3 class="rec-title">{{ recomendacaoPrincipal.titulo }}</h3>
                  <p class="rec-desc">{{ recomendacaoPrincipal.descricao }}</p>
                </div>
                <SimuslabButton variant="secondary" size="sm" @click="$router.push('/simulados')">
                  Executar Plano
                </SimuslabButton>
              </div>
            </div>
          </SimuslabCard>
        </section>

        <!-- Performance diagnosis + Recent activity -->
        <div class="two-col">

          <!-- Performance by subject -->
          <section>
            <h3 class="section-heading">Diagnóstico de Performance</h3>
            <div class="materia-list">
              <SimuslabCard
                v-for="materia in dados.por_materia"
                :key="materia.codigo"
                padding="sm"
                hoverable
              >
                <div class="materia-row">
                  <div class="materia-info">
                    <span class="materia-code">{{ materia.codigo }}</span>
                    <span class="materia-name">{{ materia.materia }}</span>
                  </div>
                  <div class="materia-score-row">
                    <div class="score-bar-track">
                      <div
                        class="score-bar-fill"
                        :class="scoreBg(materia.percentual)"
                        :style="{ width: materia.percentual + '%' }"
                      />
                    </div>
                    <span class="score-pct" :class="scoreText(materia.percentual)">
                      {{ materia.percentual }}%
                    </span>
                  </div>
                </div>
              </SimuslabCard>
            </div>
          </section>

          <!-- Recent activity -->
          <section>
            <h3 class="section-heading">Atividades Recentes</h3>

            <div v-if="dados.historico.length === 0" class="empty-activity">
              Nenhuma atividade recente encontrada.
            </div>

            <SimuslabCard v-else padding="none">
              <div
                v-for="item in historicoComTendencia"
                :key="item.resultado_id"
                class="activity-row"
                @click="$router.push({ name: 'resultado', params: { id: item.resultado_id } })"
              >
                <div class="activity-info">
                  <p class="activity-name">{{ item.simulado }}</p>
                  <p class="activity-date">{{ item.data }}</p>
                </div>
                <div class="activity-right">
                  <span class="activity-score" :class="scoreText(item.score)">{{ item.score }}%</span>
                  <span class="activity-arrow">→</span>
                </div>
              </div>
            </SimuslabCard>
          </section>

        </div>
      </div>
    </div>

  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import SimuslabCard       from '../components/ui/SimuslabCard.vue'
import SimuslabBadge      from '../components/ui/SimuslabBadge.vue'
import SimuslabButton     from '../components/ui/SimuslabButton.vue'
import SimuslabKPICard    from '../components/ui/SimuslabKPICard.vue'

const router   = useRouter()
const username = ref('')
const carregando = ref(true)
const erro       = ref('')
const isAdmin    = ref(localStorage.getItem('user_role') === 'admin')

const dados = ref({
  score_geral: 0,
  total_simulados: 0,
  por_materia: [],
  historico: [],
  gamificacao: { xp: 0, ofensiva: 0 },
})

const XP_POR_NIVEL   = 500
const nivelAtual     = computed(() => Math.floor((dados.value.gamificacao?.xp || 0) / XP_POR_NIVEL) + 1)
const xpProgresso    = computed(() => (dados.value.gamificacao?.xp || 0) % XP_POR_NIVEL)
const progressoNivel = computed(() => (xpProgresso.value / XP_POR_NIVEL) * 100)
const scoreDelta     = computed(() => undefined) // expandir com dados de histórico

const greeting = computed(() => {
  const h = new Date().getHours()
  if (h < 12) return 'Bom dia'
  if (h < 18) return 'Boa tarde'
  return 'Boa noite'
})

const formattedDate = computed(() =>
  new Date().toLocaleDateString('pt-BR', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
)

const recomendacaoPrincipal = computed(() => {
  if (!dados.value.por_materia?.length) return {}
  const pior = [...dados.value.por_materia].sort((a, b) => a.percentual - b.percentual)[0]
  return {
    titulo: `Foco Estratégico: ${pior.materia}`,
    descricao: `Seu desempenho nesta área está em ${pior.percentual}%. Recomendamos uma bateria focada em mapear suas lacunas nesta disciplina hoje.`,
  }
})

const historicoComTendencia = computed(() => {
  const map = {}
  const crono = [...dados.value.historico].reverse()
  return crono.map(item => {
    let trend = null
    if (map[item.simulado_id] !== undefined) {
      const diff = item.score - map[item.simulado_id]
      if (diff > 0) trend = 'up'; else if (diff < 0) trend = 'down'
    }
    map[item.simulado_id] = item.score
    return { ...item, trend }
  }).reverse()
})

onMounted(async () => {
  try {
    const [perfil, dashboard] = await Promise.all([
      api.get('/api/profile/'),
      api.get('/api/resultados/dashboard/'),
    ])
    username.value = perfil.data.username
    dados.value    = dashboard.data
  } catch {
    erro.value = 'Erro de conexão com a API.'
  } finally {
    carregando.value = false
  }
})

function scoreText(v) { return v >= 70 ? 'score--good' : v >= 50 ? 'score--mid' : 'score--low' }
function scoreBg(v)   { return v >= 70 ? 'fill--good' : v >= 50 ? 'fill--mid' : 'fill--low' }
</script>

<style scoped>
/* ── Page header ── */
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-4);
  margin-bottom: var(--space-7);
}

.page-greeting {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  margin-bottom: var(--space-1);
}

.page-date {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  color: var(--color-comet);
  text-transform: capitalize;
}

.page-badges {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-wrap: wrap;
}

.xp-bar {
  width: 64px;
  height: 4px;
  background: var(--color-border);
  border-radius: var(--radius-full);
  overflow: hidden;
}
.xp-fill {
  height: 100%;
  background: var(--color-orbit);
  border-radius: var(--radius-full);
  transition: width var(--transition-slow);
}

/* ── Error ── */
.error-banner {
  background: var(--color-nova-dim);
  border: 1px solid var(--color-nova-border);
  color: var(--color-nova);
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-base);
  margin-bottom: var(--space-6);
}

/* ── KPI grid ── */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-5);
  margin-bottom: var(--space-7);
}

/* ── Sections ── */
.section { margin-bottom: var(--space-6); }

.section-heading {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--color-dust);
  margin-bottom: var(--space-4);
}

/* ── Admin panel ── */
.admin-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: var(--space-5);
}
.admin-panel-info { display: flex; flex-direction: column; gap: var(--space-2); }
.admin-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  color: var(--color-star);
}
.admin-sub { font-size: var(--text-base); color: var(--color-comet); }
.admin-actions { display: flex; gap: var(--space-3); flex-wrap: wrap; }

/* ── Empty state ── */
.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: var(--space-10) var(--space-5);
  gap: var(--space-4);
}
.empty-icon {
  font-size: 2.5rem;
  color: var(--color-orbit);
  opacity: 0.5;
}
.empty-title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: var(--weight-bold);
  color: var(--color-star);
}
.empty-text {
  font-size: var(--text-base);
  color: var(--color-comet);
  line-height: var(--leading-relaxed);
  max-width: 420px;
}

/* ── Recomendação ── */
.recomendacao { display: flex; flex-direction: column; gap: var(--space-4); }
.recomendacao-top { display: flex; gap: var(--space-3); flex-wrap: wrap; align-items: center; }
.recomendacao-body {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: var(--space-6);
  flex-wrap: wrap;
}
.rec-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  margin-bottom: var(--space-2);
}
.rec-desc { font-size: var(--text-base); color: var(--color-comet); line-height: var(--leading-relaxed); max-width: 520px; }

/* ── Two column layout ── */
.two-col {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: var(--space-5);
}

/* ── Matéria list ── */
.materia-list { display: flex; flex-direction: column; gap: var(--space-2); }
.materia-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-4);
}
.materia-info {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  min-width: 0;
  flex: 1;
}
.materia-code {
  flex-shrink: 0;
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: var(--weight-bold);
  color: var(--color-dust);
  background: var(--color-void);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xs);
  padding: 2px 6px;
}
.materia-name {
  font-size: var(--text-base);
  color: var(--color-star);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.materia-score-row {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  flex-shrink: 0;
}
.score-bar-track {
  width: 80px;
  height: 4px;
  background: var(--color-border);
  border-radius: var(--radius-full);
  overflow: hidden;
}
.score-bar-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width var(--transition-slow);
}
.fill--good { background: var(--color-stellar); }
.fill--mid  { background: var(--color-flare); }
.fill--low  { background: var(--color-nova); }

.score-pct {
  font-family: var(--font-mono);
  font-size: var(--text-sm);
  font-weight: var(--weight-bold);
  width: 36px;
  text-align: right;
}
.score--good { color: var(--color-stellar); }
.score--mid  { color: var(--color-flare); }
.score--low  { color: var(--color-nova); }

/* ── Activity feed ── */
.empty-activity {
  font-size: var(--text-base);
  color: var(--color-dust);
  text-align: center;
  padding: var(--space-8);
}

.activity-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-5);
  border-bottom: 1px solid var(--color-border);
  cursor: pointer;
  transition: background var(--transition-fast);
}
.activity-row:last-child { border-bottom: none; }
.activity-row:hover { background: var(--color-surface-hover); }

.activity-info { flex: 1; min-width: 0; margin-right: var(--space-4); }
.activity-name {
  font-size: var(--text-base);
  color: var(--color-star);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 2px;
}
.activity-date { font-family: var(--font-mono); font-size: var(--text-xs); color: var(--color-dust); }

.activity-right { display: flex; align-items: center; gap: var(--space-3); flex-shrink: 0; }
.activity-score { font-family: var(--font-mono); font-size: var(--text-base); font-weight: var(--weight-bold); }
.activity-arrow {
  color: var(--color-orbit);
  font-weight: var(--weight-bold);
  opacity: 0;
  transition: opacity var(--transition-fast);
}
.activity-row:hover .activity-arrow { opacity: 1; }

/* ── Responsive ── */
@media (max-width: 1024px) { .two-col { grid-template-columns: 1fr; } }
@media (max-width: 768px)  {
  .kpi-grid { grid-template-columns: 1fr; }
  .page-header { flex-direction: column; }
}
</style>

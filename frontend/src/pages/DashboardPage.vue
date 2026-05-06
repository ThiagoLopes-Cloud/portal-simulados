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
                    <span class="score-pill" :class="scorePill(materia.percentual)">
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
                  <span class="score-pill" :class="scorePill(item.score)">{{ item.score }}%</span>
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

function scorePill(v) { return v >= 70 ? 'pill--green' : v >= 50 ? 'pill--amber' : 'pill--red' }
function scoreBg(v)   { return v >= 70 ? 'fill--good' : v >= 50 ? 'fill--mid'  : 'fill--low'  }
</script>

<style scoped>
/* ── Page header ── */
.page-header {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 28px;
}

.page-greeting {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.025em;
  margin-bottom: 4px;
}

.page-date {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  color: #64748b;
  text-transform: capitalize;
}

.page-badges {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.xp-bar {
  width: 56px;
  height: 4px;
  background: #e2e8f0;
  border-radius: 99px;
  overflow: hidden;
}
.xp-fill {
  height: 100%;
  background: #3b82f6;
  border-radius: 99px;
  transition: width 0.6s ease;
}

/* ── Error ── */
.error-banner {
  background: #fef2f2;
  border: 1px solid #fecaca;
  color: #b91c1c;
  border-radius: 12px;
  padding: 12px 16px;
  font-size: 0.875rem;
  margin-bottom: 24px;
}

/* ── KPI grid ── */
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 28px;
}

/* ── Sections ── */
.section { margin-bottom: 24px; }

.section-heading {
  font-family: var(--font-body);
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: #94a3b8;
  margin-bottom: 12px;
}

/* ── Admin panel ── */
.admin-panel {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 20px;
}
.admin-panel-info { display: flex; flex-direction: column; gap: 6px; }
.admin-title {
  font-family: var(--font-display);
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
}
.admin-sub { font-size: 0.875rem; color: #64748b; }
.admin-actions { display: flex; gap: 10px; flex-wrap: wrap; }

/* ── Empty state ── */
.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 48px 20px;
  gap: 16px;
}
.empty-icon { font-size: 2.5rem; color: #3b82f6; opacity: 0.4; }
.empty-title {
  font-family: var(--font-display);
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
}
.empty-text {
  font-size: 0.875rem;
  color: #64748b;
  line-height: 1.6;
  max-width: 420px;
}

/* ── Recomendação ── */
.recomendacao { display: flex; flex-direction: column; gap: 16px; }
.recomendacao-top { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
.recomendacao-body {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 24px;
  flex-wrap: wrap;
}
.rec-title {
  font-family: var(--font-display);
  font-size: 1.125rem;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 6px;
}
.rec-desc { font-size: 0.875rem; color: #475569; line-height: 1.6; max-width: 520px; }

/* ── Two column layout ── */
.two-col {
  display: grid;
  grid-template-columns: 3fr 2fr;
  gap: 20px;
}

/* ── Matéria list ── */
.materia-list { display: flex; flex-direction: column; gap: 8px; }
.materia-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}
.materia-info {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
  flex: 1;
}
.materia-code {
  flex-shrink: 0;
  font-family: var(--font-body);
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #64748b;
  background: #f1f5f9;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  padding: 2px 7px;
}
.materia-name {
  font-size: 0.875rem;
  color: #334155;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.materia-score-row {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}
.score-bar-track {
  width: 80px;
  height: 5px;
  background: #f1f5f9;
  border-radius: 99px;
  overflow: hidden;
}
.score-bar-fill {
  height: 100%;
  border-radius: 99px;
  transition: width 0.6s ease;
}
.fill--good { background: #10b981; }
.fill--mid  { background: #f59e0b; }
.fill--low  { background: #ef4444; }

/* ── Score pill badges ── */
.score-pill {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-family: var(--font-body);
  font-size: 0.7rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 99px;
  border: 1px solid transparent;
  min-width: 44px;
}
.pill--green { background: #f0fdf4; color: #166534; border-color: #bbf7d0; }
.pill--amber { background: #fffbeb; color: #92400e; border-color: #fde68a; }
.pill--red   { background: #fef2f2; color: #b91c1c; border-color: #fecaca; }

/* ── Activity feed ── */
.empty-activity {
  font-size: 0.875rem;
  color: #94a3b8;
  text-align: center;
  padding: 32px;
}

.activity-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  border-bottom: 1px solid #f8fafc;
  cursor: pointer;
  transition: background 0.12s ease;
}
.activity-row:last-child { border-bottom: none; }
.activity-row:hover { background: #f8fafc; }

.activity-info { flex: 1; min-width: 0; margin-right: 16px; }
.activity-name {
  font-size: 0.875rem;
  color: #1e293b;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-bottom: 2px;
}
.activity-date { font-size: 0.75rem; color: #94a3b8; }

.activity-right { display: flex; align-items: center; gap: 10px; flex-shrink: 0; }
.activity-arrow {
  color: #3b82f6;
  font-size: 0.75rem;
  opacity: 0;
  transition: opacity 0.12s ease;
}
.activity-row:hover .activity-arrow { opacity: 1; }

/* ── Responsive ── */
@media (max-width: 1024px) { .two-col { grid-template-columns: 1fr; } }
@media (max-width: 768px)  {
  .kpi-grid { grid-template-columns: 1fr 1fr; gap: 12px; }
  .page-header { flex-direction: column; }
  .page-greeting { font-size: 1.25rem; }
}
@media (max-width: 480px) {
  .kpi-grid { grid-template-columns: 1fr; }
}
</style>

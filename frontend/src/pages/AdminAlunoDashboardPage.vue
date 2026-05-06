<template>
  <DashboardLayout :username="username" :is-admin="true">

    <!-- Skeleton -->
    <div v-if="carregando" class="skeleton-stack">
      <div class="sk-row"><div class="sk-box" style="width:160px;height:36px;" /></div>
      <div class="sk-box sk-profile" />
      <div class="sk-kpis">
        <div v-for="n in 4" :key="n" class="sk-box sk-kpi" />
      </div>
    </div>

    <!-- Erro -->
    <div v-else-if="erro" class="empty-state">
      <div class="empty-icon nova">⚠</div>
      <h3 class="empty-title">Falha de Leitura</h3>
      <p class="empty-sub">{{ erro }}</p>
      <SimuslabButton variant="primary" size="sm" class="mt-5" @click="$router.push('/admin/alunos')">
        Voltar para Base de Alunos
      </SimuslabButton>
    </div>

    <div v-else>
      <!-- Breadcrumb -->
      <div class="page-header">
        <SimuslabButton variant="ghost" size="sm" @click="$router.push('/admin/alunos')">← Voltar para Base</SimuslabButton>
        <SimuslabBadge variant="pulsar">Admin</SimuslabBadge>
      </div>

      <!-- Perfil do aluno -->
      <div class="profile-card">
        <div class="profile-avatar">{{ dados.aluno.username.charAt(0).toUpperCase() }}</div>
        <div class="profile-info">
          <h2 class="profile-name">{{ dados.aluno.username }}</h2>
          <p class="profile-email">{{ dados.aluno.email }}</p>
        </div>
        <SimuslabBadge variant="stellar" dot>Ativo no Laboratório</SimuslabBadge>
      </div>

      <!-- KPIs -->
      <div class="kpi-grid">
        <div class="kpi-card">
          <span class="kpi-val" :class="scoreColor(dados.score_geral)">{{ dados.score_geral }}%</span>
          <span class="kpi-label">Aproveitamento Geral</span>
        </div>
        <div class="kpi-card">
          <span class="kpi-val orbit">{{ dados.total_simulados }}</span>
          <span class="kpi-label">Avaliações Realizadas</span>
        </div>
        <div class="kpi-card">
          <span class="kpi-val pulsar">{{ dados.por_materia.length }}</span>
          <span class="kpi-label">Disciplinas Mapeadas</span>
        </div>
        <div class="kpi-card">
          <span class="kpi-val nova">{{ pontoFraco }}</span>
          <span class="kpi-label">Ponto de Atenção</span>
        </div>
      </div>

      <!-- Split: análise + histórico -->
      <div class="data-split">

        <!-- Disciplinas -->
        <section>
          <h3 class="section-title">Análise de Disciplinas</h3>

          <div v-if="dados.por_materia.length === 0" class="empty-list">
            Sem dados suficientes para gerar relatório tático.
          </div>

          <div v-for="mat in dados.por_materia" :key="mat.codigo" class="subject-card">
            <div class="subject-header" @click="toggleMateria(mat.codigo)">
              <div class="subj-left">
                <span class="subj-tag">{{ mat.codigo }}</span>
                <span class="subj-name">{{ mat.materia }}</span>
                <span class="subj-vol">{{ mat.acertos }}/{{ mat.total_questoes }} corretas</span>
              </div>
              <div class="subj-right">
                <div class="mini-bar">
                  <div class="mini-fill" :class="scoreBg(mat.percentual)" :style="{ width: mat.percentual + '%' }" />
                </div>
                <span class="subj-score" :class="scoreColor(mat.percentual)">{{ mat.percentual }}%</span>
                <span class="trend" :class="mat.diferenca_media >= 0 ? 'trend--up' : 'trend--down'">
                  {{ mat.diferenca_media >= 0 ? '▲ +' : '▼ ' }}{{ mat.diferenca_media }}%
                </span>
                <span class="toggle-icon">{{ materiasAbertas.includes(mat.codigo) ? '▲' : '▼' }}</span>
              </div>
            </div>

            <div v-if="materiasAbertas.includes(mat.codigo)" class="temas-breakdown">
              <div class="temas-legend">
                <span>Aluno</span><span>Média Base</span>
              </div>
              <div v-for="tema in mat.temas" :key="tema.tema" class="tema-row">
                <div class="tema-info">
                  <span class="tema-name">{{ tema.tema }}</span>
                  <span class="tema-vol">{{ tema.acertos }}/{{ tema.total }}</span>
                </div>
                <div class="tema-charts">
                  <div class="chart-line">
                    <span class="chart-label orbit">Aluno</span>
                    <div class="chart-bg"><div class="chart-fill" :class="scoreBg(tema.percentual)" :style="{ width: tema.percentual + '%' }" /></div>
                    <span class="chart-val" :class="scoreColor(tema.percentual)">{{ tema.percentual }}%</span>
                  </div>
                  <div class="chart-line">
                    <span class="chart-label dust">Média</span>
                    <div class="chart-bg"><div class="chart-fill bg-dust" :style="{ width: tema.media_plataforma + '%' }" /></div>
                    <span class="chart-val dust">{{ tema.media_plataforma }}%</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <!-- Histórico -->
        <section>
          <h3 class="section-title">Registro de Atividades</h3>
          <div v-if="dados.historico.length === 0" class="empty-list">Nenhum registro de avaliação.</div>
          <div v-else class="hist-card">
            <table class="hist-table">
              <thead>
                <tr class="thead-row">
                  <th class="th">Simulação</th>
                  <th class="th text-center">Acertos</th>
                  <th class="th text-center">Score</th>
                  <th class="th text-right">Data</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in dados.historico" :key="item.simulado_id" class="tbody-row">
                  <td class="td td-title">{{ item.simulado }}</td>
                  <td class="td text-center">{{ item.acertos }}/{{ item.total }}</td>
                  <td class="td text-center"><span class="score-badge" :class="scoreBg(item.score)">{{ item.score }}%</span></td>
                  <td class="td text-right dust">{{ item.data }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../services/api.js'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import SimuslabButton from '../components/ui/SimuslabButton.vue'
import SimuslabBadge from '../components/ui/SimuslabBadge.vue'

const router = useRouter()
const route = useRoute()
const username = localStorage.getItem('username') || ''
const carregando = ref(true)
const erro = ref('')
const materiasAbertas = ref([])

const dados = ref({
  aluno: { username: '', email: '' },
  score_geral: 0, total_simulados: 0, por_materia: [], historico: [],
})

const pontoFraco = computed(() =>
  dados.value.por_materia.length === 0 ? 'N/A' : dados.value.por_materia[0].codigo
)

onMounted(async () => {
  try {
    const res = await api.get(`/api/resultados/admin/alunos/${route.params.id}/`)
    dados.value = res.data
    if (dados.value.por_materia.length > 0) materiasAbertas.value = [dados.value.por_materia[0].codigo]
  } catch {
    erro.value = 'Falha ao extrair dados do candidato.'
  } finally {
    carregando.value = false
  }
})

function toggleMateria(codigo) {
  const i = materiasAbertas.value.indexOf(codigo)
  if (i === -1) materiasAbertas.value.push(codigo)
  else materiasAbertas.value.splice(i, 1)
}

function scoreColor(v) { return v >= 70 ? 'stellar' : v >= 50 ? 'flare' : 'nova' }
function scoreBg(v)    { return v >= 70 ? 'bg-stellar' : v >= 50 ? 'bg-flare' : 'bg-nova' }
</script>

<style scoped>
/* Skeleton */
.skeleton-stack { display: flex; flex-direction: column; gap: var(--space-5); }
.sk-row { display: flex; }
.sk-box { background: var(--color-nebula); border-radius: var(--radius-md); position: relative; overflow: hidden; }
.sk-box::after { content: ''; position: absolute; inset: 0; background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent); animation: shimmer 1.5s infinite; }
.sk-profile { height: 100px; }
.sk-kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-4); }
.sk-kpi { height: 100px; }
@keyframes shimmer { 0% { transform: translateX(-100%); } 100% { transform: translateX(100%); } }

/* Empty */
.empty-state { display: flex; flex-direction: column; align-items: center; text-align: center; padding: var(--space-14) var(--space-8); background: var(--color-nebula); border: 1px dashed var(--color-border); border-radius: var(--radius-xl); }
.empty-icon { font-size: 2.5rem; color: var(--color-orbit); margin-bottom: var(--space-5); }
.empty-icon.nova { color: var(--color-nova); }
.empty-title { font-family: var(--font-display); font-size: var(--text-lg); font-weight: var(--weight-bold); color: var(--color-star); margin-bottom: var(--space-2); }
.empty-sub { font-size: var(--text-sm); color: var(--color-comet); }
.mt-5 { margin-top: var(--space-5); }

/* Layout */
.page-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: var(--space-6); }
.section-title { font-family: var(--font-display); font-size: var(--text-base); font-weight: var(--weight-bold); color: var(--color-star); margin-bottom: var(--space-4); }

/* Profile */
.profile-card {
  background: var(--color-nebula);
  border: 1px solid var(--color-border);
  border-left: 3px solid var(--color-orbit);
  border-radius: var(--radius-xl);
  padding: var(--space-6) var(--space-7);
  display: flex;
  align-items: center;
  gap: var(--space-5);
  margin-bottom: var(--space-6);
  flex-wrap: wrap;
}
.profile-avatar { width: 60px; height: 60px; border-radius: 50%; background: rgba(0,229,255,0.1); border: 2px solid rgba(0,229,255,0.2); display: flex; align-items: center; justify-content: center; font-size: var(--text-2xl); font-weight: var(--weight-extrabold); color: var(--color-orbit); flex-shrink: 0; }
.profile-info { flex: 1; }
.profile-name { font-family: var(--font-display); font-size: var(--text-xl); font-weight: var(--weight-bold); color: var(--color-star); }
.profile-email { font-size: var(--text-sm); color: var(--color-comet); margin-top: 3px; }

/* KPIs */
.kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-4); margin-bottom: var(--space-7); }
.kpi-card { background: var(--color-nebula); border: 1px solid var(--color-border); border-radius: var(--radius-xl); padding: var(--space-6) var(--space-4); display: flex; flex-direction: column; align-items: center; text-align: center; }
.kpi-val { font-size: var(--text-3xl); font-weight: var(--weight-extrabold); line-height: 1.1; margin-bottom: var(--space-2); }
.kpi-label { font-size: var(--text-2xs); font-family: var(--font-mono); color: var(--color-dust); text-transform: uppercase; letter-spacing: 0.08em; }
.stellar { color: var(--color-stellar); }
.nova    { color: var(--color-nova); }
.orbit   { color: var(--color-orbit); }
.pulsar  { color: var(--color-pulsar); }
.flare   { color: var(--color-flare); }
.dust    { color: var(--color-dust); }
.bg-stellar { background: var(--color-stellar); }
.bg-flare   { background: var(--color-flare); }
.bg-nova    { background: var(--color-nova); }
.bg-dust    { background: var(--color-dust); opacity: 0.4; }

/* Split */
.data-split { display: grid; grid-template-columns: 1.4fr 1fr; gap: var(--space-7); }
.empty-list { background: var(--color-nebula); border: 1px solid var(--color-border); border-radius: var(--radius-md); padding: var(--space-6); text-align: center; color: var(--color-dust); font-size: var(--text-sm); font-style: italic; }

/* Subject cards */
.subject-card { background: var(--color-nebula); border: 1px solid var(--color-border); border-radius: var(--radius-md); margin-bottom: var(--space-3); overflow: hidden; }
.subject-header { display: flex; justify-content: space-between; align-items: center; padding: var(--space-4) var(--space-5); cursor: pointer; transition: background var(--transition-fast); gap: var(--space-3); }
.subject-header:hover { background: rgba(255,255,255,0.02); }
.subj-left { display: flex; align-items: center; gap: var(--space-3); }
.subj-tag { background: var(--color-orbit); color: var(--color-cosmos); padding: 2px var(--space-2); border-radius: var(--radius-sm); font-size: var(--text-2xs); font-family: var(--font-mono); font-weight: var(--weight-bold); }
.subj-name { font-weight: var(--weight-bold); color: var(--color-star); font-size: var(--text-sm); }
.subj-vol { font-size: var(--text-xs); color: var(--color-dust); }
.subj-right { display: flex; align-items: center; gap: var(--space-3); }
.mini-bar { width: 70px; height: 5px; background: rgba(255,255,255,0.08); border-radius: var(--radius-full); overflow: hidden; }
.mini-fill { height: 100%; border-radius: var(--radius-full); }
.subj-score { font-weight: var(--weight-extrabold); font-size: var(--text-sm); }
.trend { font-size: var(--text-2xs); font-weight: var(--weight-bold); padding: 2px var(--space-2); border-radius: 3px; }
.trend--up   { background: rgba(0,214,143,0.1); color: var(--color-stellar); }
.trend--down { background: var(--color-nova-dim); color: var(--color-nova); }
.toggle-icon { color: var(--color-dust); font-size: var(--text-xs); }

/* Temas breakdown */
.temas-breakdown { border-top: 1px solid var(--color-border); background: rgba(255,255,255,0.02); padding: var(--space-4) var(--space-5) var(--space-5); }
.temas-legend { display: flex; justify-content: flex-end; gap: var(--space-7); font-size: var(--text-2xs); font-family: var(--font-mono); color: var(--color-dust); text-transform: uppercase; margin-bottom: var(--space-4); padding-bottom: var(--space-3); border-bottom: 1px solid var(--color-border); }
.tema-row { display: flex; justify-content: space-between; align-items: center; padding: var(--space-3) 0; border-bottom: 1px dashed var(--color-border); }
.tema-row:last-child { border-bottom: none; }
.tema-info { display: flex; flex-direction: column; gap: 2px; }
.tema-name { font-size: var(--text-sm); font-weight: var(--weight-medium); color: var(--color-comet); }
.tema-vol { font-size: var(--text-xs); color: var(--color-dust); }
.tema-charts { display: flex; flex-direction: column; gap: var(--space-2); width: 200px; }
.chart-line { display: flex; align-items: center; gap: var(--space-2); }
.chart-label { font-size: var(--text-2xs); font-family: var(--font-mono); font-weight: var(--weight-bold); text-transform: uppercase; width: 36px; }
.chart-bg { flex: 1; height: 5px; background: rgba(255,255,255,0.08); border-radius: var(--radius-full); overflow: hidden; }
.chart-fill { height: 100%; border-radius: var(--radius-full); }
.chart-val { font-size: var(--text-xs); font-weight: var(--weight-bold); width: 34px; text-align: right; }

/* Histórico */
.hist-card { background: var(--color-nebula); border: 1px solid var(--color-border); border-radius: var(--radius-xl); overflow: hidden; }
.hist-table { width: 100%; border-collapse: collapse; }
.thead-row { border-bottom: 1px solid var(--color-border); }
.th { padding: var(--space-3) var(--space-4); text-align: left; font-size: var(--text-2xs); font-family: var(--font-mono); font-weight: var(--weight-bold); color: var(--color-dust); text-transform: uppercase; letter-spacing: 0.08em; }
.text-center { text-align: center; }
.text-right { text-align: right; }
.td { padding: var(--space-4); border-bottom: 1px solid rgba(255,255,255,0.03); vertical-align: middle; font-size: var(--text-sm); color: var(--color-comet); }
.tbody-row { transition: background var(--transition-fast); }
.tbody-row:hover { background: rgba(255,255,255,0.02); }
.td-title { font-weight: var(--weight-semibold); color: var(--color-star); }
.score-badge { display: inline-block; padding: 2px var(--space-2); border-radius: var(--radius-full); font-size: var(--text-xs); font-family: var(--font-mono); font-weight: var(--weight-bold); color: white; }

/* Responsive */
@media (max-width: 1100px) {
  .data-split { grid-template-columns: 1fr; }
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 768px) {
  .kpi-grid { grid-template-columns: repeat(2, 1fr); }
  .profile-card { flex-wrap: wrap; }
  .tema-charts { width: 100%; }
  .subj-right { flex-direction: column; align-items: flex-end; gap: var(--space-2); }
  .mini-bar { display: none; }
}
</style>

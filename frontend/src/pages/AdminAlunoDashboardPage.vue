<template>
  <div class="dashboard">
    <nav class="navbar">
      <h1>Portal de Simulados</h1>
      <div class="nav-links">
        <router-link to="/admin/alunos">← Voltar para alunos</router-link>
        <button @click="logout" class="btn-logout">Sair</button>
      </div>
    </nav>

    <div v-if="carregando" class="loading">Carregando...</div>
    <div v-else-if="erro" class="erro">{{ erro }}</div>

    <div v-else class="container">

      <!-- Cabeçalho com dados do aluno -->
      <div class="aluno-header">
        <div class="aluno-avatar">{{ dados.aluno.username[0].toUpperCase() }}</div>
        <div>
          <h2>{{ dados.aluno.username }}</h2>
          <p>{{ dados.aluno.email }}</p>
        </div>
      </div>

      <!-- Cards de resumo -->
      <div class="resumo">
        <div class="card-resumo">
          <span class="resumo-valor" :class="corScore(dados.score_geral)">
            {{ dados.score_geral }}%
          </span>
          <span class="resumo-label">Score geral</span>
        </div>
        <div class="card-resumo">
          <span class="resumo-valor azul">{{ dados.total_simulados }}</span>
          <span class="resumo-label">Simulados feitos</span>
        </div>
        <div class="card-resumo">
          <span class="resumo-valor roxo">{{ dados.por_materia.length }}</span>
          <span class="resumo-label">Matérias avaliadas</span>
        </div>
        <div class="card-resumo">
          <span class="resumo-valor" :class="pontoFracoColor">
            {{ pontoFraco }}
          </span>
          <span class="resumo-label">Ponto mais fraco</span>
        </div>
      </div>

      <!-- Desempenho por matéria -->
      <section class="secao">
        <h3>Desempenho por matéria</h3>
        <div v-if="dados.por_materia.length === 0" class="vazio">
          Este aluno ainda não respondeu questões com tema vinculado.
        </div>

        <div
          v-for="materia in dados.por_materia"
          :key="materia.codigo"
          class="card-materia"
        >
          <div class="materia-header" @click="toggleMateria(materia.codigo)">
            <div class="materia-info">
              <span class="materia-badge">{{ materia.codigo }}</span>
              <span class="materia-nome">{{ materia.materia }}</span>
              <span class="materia-detalhe">
                {{ materia.acertos }}/{{ materia.total_questoes }} questões
              </span>
            </div>
            <div class="materia-direita">
              <div class="barra-mini">
                <div
                  class="barra-fill"
                  :class="corScore(materia.percentual)"
                  :style="{ width: materia.percentual + '%' }"
                ></div>
              </div>
              <span class="materia-percentual" :class="corScore(materia.percentual)">
                {{ materia.percentual }}%
              </span>
              <span class="diferenca" :class="materia.diferenca_media >= 0 ? 'positivo' : 'negativo'">
                {{ materia.diferenca_media >= 0 ? '+' : '' }}{{ materia.diferenca_media }}% vs média
              </span>
              <span class="toggle-icon">
                {{ materiasAbertas.includes(materia.codigo) ? '▲' : '▼' }}
              </span>
            </div>
          </div>

          <div v-if="materiasAbertas.includes(materia.codigo)" class="temas-lista">
            <div class="temas-legenda">
              <span>Desempenho do aluno</span>
              <span>Média da plataforma</span>
            </div>
            <div
              v-for="tema in materia.temas"
              :key="tema.tema"
              class="tema-item"
            >
              <div class="tema-info">
                <span class="tema-nome">{{ tema.tema }}</span>
                <span class="tema-detalhe">{{ tema.acertos }}/{{ tema.total }} questões</span>
              </div>
              <div class="tema-direita">
                <div class="barra-dupla">
                  <div class="barra-label">Aluno</div>
                  <div class="barra-mini pequena">
                    <div
                      class="barra-fill"
                      :class="corScore(tema.percentual)"
                      :style="{ width: tema.percentual + '%' }"
                    ></div>
                  </div>
                  <span class="tema-percentual" :class="corScore(tema.percentual)">
                    {{ tema.percentual }}%
                  </span>
                </div>
                <div class="barra-dupla">
                  <div class="barra-label cinza">Média</div>
                  <div class="barra-mini pequena">
                    <div
                      class="barra-fill cinza-fill"
                      :style="{ width: tema.media_plataforma + '%' }"
                    ></div>
                  </div>
                  <span class="tema-percentual cinza">{{ tema.media_plataforma }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Histórico -->
      <section class="secao">
        <h3>Histórico de simulados</h3>
        <div v-if="dados.historico.length === 0" class="vazio">
          Este aluno ainda não realizou nenhum simulado.
        </div>
        <div class="tabela-container" v-else>
          <table class="tabela">
            <thead>
              <tr>
                <th>Simulado</th>
                <th>Acertos</th>
                <th>Score</th>
                <th>Data</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="item in dados.historico" :key="item.simulado_id">
                <td>{{ item.simulado }}</td>
                <td>{{ item.acertos }}/{{ item.total }}</td>
                <td :class="corScore(item.score)">{{ item.score }}%</td>
                <td class="data">{{ item.data }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import api from '../services/api.js'

const router = useRouter()
const route = useRoute()
const carregando = ref(true)
const erro = ref('')
const materiasAbertas = ref([])

const dados = ref({
  aluno: { username: '', email: '' },
  score_geral: 0,
  total_simulados: 0,
  por_materia: [],
  historico: [],
})

// Ponto mais fraco — primeira matéria da lista (já ordenada do pior para melhor)
const pontoFraco = computed(() => {
  if (dados.value.por_materia.length === 0) return '—'
  return dados.value.por_materia[0].codigo
})

const pontoFracoColor = computed(() => {
  if (dados.value.por_materia.length === 0) return ''
  return corScore(dados.value.por_materia[0].percentual)
})

onMounted(async () => {
  try {
    const response = await api.get(`/resultados/admin/alunos/${route.params.id}/`)
    dados.value = response.data

    if (dados.value.por_materia.length > 0) {
      materiasAbertas.value = [dados.value.por_materia[0].codigo]
    }
  } catch (error) {
    erro.value = 'Erro ao carregar o dashboard do aluno.'
  } finally {
    carregando.value = false
  }
})

function toggleMateria(codigo) {
  const index = materiasAbertas.value.indexOf(codigo)
  if (index === -1) {
    materiasAbertas.value.push(codigo)
  } else {
    materiasAbertas.value.splice(index, 1)
  }
}

function corScore(valor) {
  if (valor >= 70) return 'verde'
  if (valor >= 50) return 'amarelo'
  return 'vermelho'
}

function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_role')
  router.push({ name: 'login' })
}
</script>

<style scoped>
.dashboard { min-height: 100vh; background: #f5f5f5; }
.navbar {
  background: #667eea; color: white; padding: 16px 32px;
  display: flex; justify-content: space-between; align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.navbar h1 { font-size: 20px; font-weight: 600; }
.nav-links { display: flex; align-items: center; gap: 24px; }
.nav-links a { color: white; text-decoration: none; font-size: 14px; opacity: 0.9; }
.btn-logout {
  background: rgba(255,255,255,0.2); color: white;
  border: 1px solid rgba(255,255,255,0.4);
  padding: 6px 16px; border-radius: 6px; cursor: pointer; font-size: 14px;
}
.loading, .vazio { color: #999; padding: 40px; text-align: center; }
.erro { color: #c00; text-align: center; padding: 40px; }
.container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }

.aluno-header {
  display: flex; align-items: center; gap: 20px; margin-bottom: 32px;
}
.aluno-avatar {
  width: 56px; height: 56px; background: #667eea; color: white;
  border-radius: 50%; display: flex; align-items: center;
  justify-content: center; font-size: 24px; font-weight: 700;
}
.aluno-header h2 { font-size: 22px; color: #333; margin-bottom: 4px; }
.aluno-header p { color: #666; font-size: 14px; }

.resumo {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 16px; margin-bottom: 40px;
}
.card-resumo {
  background: white; border-radius: 12px; padding: 24px;
  text-align: center; box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  display: flex; flex-direction: column; gap: 8px;
}
.resumo-valor { font-size: 28px; font-weight: 700; }
.resumo-label { font-size: 13px; color: #999; }

.secao { margin-bottom: 40px; }
.secao h3 { font-size: 18px; color: #333; margin-bottom: 16px; }

.card-materia {
  background: white; border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07);
  margin-bottom: 12px; overflow: hidden;
}
.materia-header {
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px 20px; cursor: pointer; transition: background 0.15s;
}
.materia-header:hover { background: #f8f9ff; }
.materia-info { display: flex; align-items: center; gap: 12px; }
.materia-badge {
  background: #667eea; color: white;
  padding: 3px 10px; border-radius: 99px; font-size: 12px; font-weight: 600;
}
.materia-nome { font-weight: 600; color: #333; }
.materia-detalhe { font-size: 13px; color: #999; }
.materia-direita { display: flex; align-items: center; gap: 12px; }
.materia-percentual { font-weight: 700; font-size: 16px; min-width: 48px; text-align: right; }
.diferenca { font-size: 11px; font-weight: 600; }
.diferenca.positivo { color: #22c55e; }
.diferenca.negativo { color: #ef4444; }
.toggle-icon { color: #999; font-size: 12px; }

.barra-mini { width: 120px; height: 8px; background: #eee; border-radius: 99px; overflow: hidden; }
.barra-mini.pequena { width: 80px; height: 6px; }
.barra-fill { height: 100%; border-radius: 99px; transition: width 0.4s ease; }
.barra-fill.verde { background: #22c55e; }
.barra-fill.amarelo { background: #f59e0b; }
.barra-fill.vermelho { background: #ef4444; }
.barra-fill.cinza-fill { background: #cbd5e1; }

.temas-lista { border-top: 1px solid #f0f0f0; }
.temas-legenda {
  display: flex; justify-content: flex-end; gap: 40px;
  padding: 8px 20px; font-size: 11px; color: #bbb;
  border-bottom: 1px solid #f5f5f5;
}
.tema-item {
  display: flex; justify-content: space-between; align-items: center;
  padding: 12px 20px 12px 44px; border-bottom: 1px solid #f8f8f8;
}
.tema-item:last-child { border-bottom: none; }
.tema-info { display: flex; flex-direction: column; gap: 2px; }
.tema-nome { font-size: 14px; color: #444; }
.tema-detalhe { font-size: 12px; color: #bbb; }
.tema-direita { display: flex; flex-direction: column; gap: 6px; align-items: flex-end; }
.barra-dupla { display: flex; align-items: center; gap: 8px; }
.barra-label { font-size: 11px; color: #667eea; min-width: 32px; }
.barra-label.cinza { color: #bbb; }
.tema-percentual { font-size: 13px; font-weight: 600; min-width: 36px; text-align: right; }
.tema-percentual.cinza { color: #bbb; font-weight: 400; }

.tabela-container {
  background: white; border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07); overflow: hidden;
}
.tabela { width: 100%; border-collapse: collapse; }
.tabela thead { background: #667eea; color: white; }
.tabela th { padding: 12px 16px; text-align: left; font-size: 13px; font-weight: 500; }
.tabela tbody tr { border-bottom: 1px solid #f0f0f0; }
.tabela tbody tr:hover { background: #f8f9ff; }
.tabela td { padding: 12px 16px; font-size: 14px; color: #333; }
.data { color: #999; font-size: 13px; }

.verde { color: #22c55e; }
.amarelo { color: #f59e0b; }
.vermelho { color: #ef4444; }
.azul { color: #667eea; }
.roxo { color: #a855f7; }

@media (max-width: 700px) {
  .resumo { grid-template-columns: repeat(2, 1fr); }
  .barra-mini { width: 60px; }
}
</style>
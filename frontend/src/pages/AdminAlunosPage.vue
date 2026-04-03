<template>
  <div class="admin-alunos">
    <nav class="navbar">
      <h1>Portal de Simulados</h1>
      <div class="nav-links">
        <router-link to="/admin/alunos">Alunos</router-link>
        <router-link to="/admin/importar">Importar Questões</router-link>
        <button @click="logout" class="btn-logout">Sair</button>
      </div>
  </nav>

    <div class="container">
      <div class="header">
        <h2>👥 Alunos</h2>
        <p>Acompanhe o desempenho de cada aluno</p>
      </div>

      <div v-if="carregando" class="loading">Carregando alunos...</div>
      <div v-else-if="erro" class="erro">{{ erro }}</div>

      <div v-else>
        <div v-if="alunos.length === 0" class="vazio">
          Nenhum aluno cadastrado ainda.
        </div>

        <div class="tabela-container" v-else>
          <table class="tabela">
            <thead>
              <tr>
                <th>Aluno</th>
                <th>Email</th>
                <th>Simulados</th>
                <th>Score médio</th>
                <th>Ação</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="aluno in alunos" :key="aluno.id">
                <td class="aluno-nome">{{ aluno.username }}</td>
                <td class="email">{{ aluno.email }}</td>
                <td>{{ aluno.total_simulados }}</td>
                <td :class="corScore(aluno.score_medio)">
                  {{ aluno.total_simulados > 0 ? aluno.score_medio + '%' : '—' }}
                </td>
                <td>
                  <button
                    @click="verDashboard(aluno.id)"
                    class="btn-ver"
                    :disabled="aluno.total_simulados === 0"
                  >
                    Ver desempenho
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'

const router = useRouter()
const alunos = ref([])
const carregando = ref(true)
const erro = ref('')

onMounted(async () => {
  try {
    const response = await api.get('/resultados/admin/alunos/')
    alunos.value = response.data
  } catch (error) {
    erro.value = 'Erro ao carregar lista de alunos.'
  } finally {
    carregando.value = false
  }
})

function verDashboard(id) {
  router.push({ name: 'admin-aluno-dashboard', params: { id } })
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
.admin-alunos { min-height: 100vh; background: #f5f5f5; }
.navbar {
  background: #667eea; color: white;
  padding: 16px 32px; display: flex;
  justify-content: space-between; align-items: center;
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
.container { max-width: 900px; margin: 0 auto; padding: 40px 20px; }
.header { margin-bottom: 32px; }
.header h2 { font-size: 24px; color: #333; margin-bottom: 4px; }
.header p { color: #666; }
.loading, .vazio { color: #999; padding: 40px; text-align: center; }
.erro { color: #c00; text-align: center; padding: 40px; }
.tabela-container {
  background: white; border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.07); overflow: hidden;
}
.tabela { width: 100%; border-collapse: collapse; }
.tabela thead { background: #667eea; color: white; }
.tabela th { padding: 12px 16px; text-align: left; font-size: 13px; font-weight: 500; }
.tabela tbody tr { border-bottom: 1px solid #f0f0f0; transition: background 0.15s; }
.tabela tbody tr:hover { background: #f8f9ff; }
.tabela td { padding: 12px 16px; font-size: 14px; color: #333; }
.aluno-nome { font-weight: 500; }
.email { color: #666; font-size: 13px; }
.btn-ver {
  background: #667eea; color: white; border: none;
  padding: 6px 14px; border-radius: 6px;
  cursor: pointer; font-size: 13px; transition: background 0.2s;
}
.btn-ver:hover:not(:disabled) { background: #5a6fd6; }
.btn-ver:disabled { opacity: 0.4; cursor: not-allowed; }
.verde { color: #22c55e; font-weight: 600; }
.amarelo { color: #f59e0b; font-weight: 600; }
.vermelho { color: #ef4444; font-weight: 600; }
</style>
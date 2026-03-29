<template>
  <!-- Container principal da página de ranking -->
  <div class="ranking">

    <!-- Navbar superior -->
    <nav class="navbar">
      <h1>Portal de Simulados</h1>
      <div class="nav-links">
        <router-link to="/dashboard">Dashboard</router-link>
        <router-link to="/simulados">Simulados</router-link>
        <button @click="logout" class="btn-logout">Sair</button>
      </div>
    </nav>

    <!-- Conteúdo principal -->
    <div class="container">
      <h2>🏆 Ranking Geral</h2>
      <p class="subtitulo">Os melhores alunos do portal</p>

      <!-- Estado de carregamento -->
      <div v-if="carregando" class="loading">
        Carregando ranking...
      </div>

      <!-- Mensagem de erro -->
      <div v-else-if="erro" class="erro">{{ erro }}</div>

      <!-- Tabela de ranking -->
      <div v-else class="tabela-container">

        <!-- Mensagem quando não há resultados -->
        <div v-if="ranking.length === 0" class="vazio">
          Nenhum resultado encontrado ainda.
        </div>

        <!-- Tabela com os resultados -->
        <table v-else class="tabela">
          <thead>
            <tr>
              <!-- Cabeçalhos da tabela -->
              <th>#</th>
              <th>Aluno</th>
              <th>Simulado</th>
              <th>Acertos</th>
              <th>Score</th>
              <th>Data</th>
            </tr>
          </thead>
          <tbody>
            <!-- v-for percorre cada resultado do ranking -->
            <tr
              v-for="(item, index) in ranking"
              :key="index"
              :class="{ destaque: index < 3 }"
            >
              <!-- Posição no ranking com medalha para top 3 -->
              <td class="posicao">
                <span v-if="index === 0">🥇</span>
                <span v-else-if="index === 1">🥈</span>
                <span v-else-if="index === 2">🥉</span>
                <span v-else>{{ index + 1 }}</span>
              </td>

              <!-- Nome do aluno -->
              <td class="aluno">{{ item.aluno_username }}</td>

              <!-- Título do simulado -->
              <td class="simulado">{{ item.simulado_titulo }}</td>

              <!-- Acertos no formato "3 / 3" -->
              <td class="acertos">{{ item.acertos }} / {{ item.total_questoes }}</td>

              <!-- Score em percentual com cor baseada no valor -->
              <td class="score" :class="corScore(item.score)">
                {{ item.score }}%
              </td>

              <!-- Data formatada -->
              <td class="data">{{ formatarData(item.realizado_em) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
// Importa as funções reativas do Vue
import { ref, onMounted } from 'vue'

// Importa o router para navegação e logout
import { useRouter } from 'vue-router'

// Importa o serviço de API
import api from '../services/api.js'

const router = useRouter()

// Lista do ranking retornada pela API
const ranking = ref([])
const carregando = ref(true)
const erro = ref('')

// Busca o ranking ao carregar a página
onMounted(async () => {
  try {
    // Busca o ranking ordenado por score decrescente
    const response = await api.get('/resultados/ranking/')
    ranking.value = response.data
  } catch (error) {
    erro.value = 'Erro ao carregar o ranking.'
  } finally {
    carregando.value = false
  }
})

// Retorna a classe de cor baseada no score
// Verde para >= 70%, amarelo para >= 50%, vermelho para abaixo de 50%
function corScore(score) {
  const valor = parseFloat(score)
  if (valor >= 70) return 'verde'
  if (valor >= 50) return 'amarelo'
  return 'vermelho'
}

// Formata a data para o formato brasileiro
// ex: "2026-03-19T00:00:00" → "19/03/2026"
function formatarData(data) {
  return new Date(data).toLocaleDateString('pt-BR')
}

// Logout — remove tokens e redireciona para o login
function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  localStorage.removeItem('user_role')  
  router.push({ name: 'login' })
}
</script>

<style scoped>
.ranking {
  min-height: 100vh;
  background: #f5f5f5;
}

.navbar {
  background: #667eea;
  color: white;
  padding: 16px 32px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.navbar h1 { font-size: 20px; font-weight: 600; }

.nav-links {
  display: flex;
  align-items: center;
  gap: 24px;
}

.nav-links a {
  color: white;
  text-decoration: none;
  font-size: 14px;
  opacity: 0.9;
}

.btn-logout {
  background: rgba(255,255,255,0.2);
  color: white;
  border: 1px solid rgba(255,255,255,0.4);
  padding: 6px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 20px;
}

h2 { font-size: 24px; color: #333; margin-bottom: 8px; }

.subtitulo { color: #666; margin-bottom: 32px; }

.loading {
  text-align: center;
  color: #666;
  padding: 40px;
}

.erro {
  background: #fee;
  color: #c00;
  padding: 12px;
  border-radius: 6px;
}

.tabela-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  overflow: hidden;
}

.tabela {
  width: 100%;
  border-collapse: collapse;
}

.tabela thead {
  background: #667eea;
  color: white;
}

.tabela th {
  padding: 14px 16px;
  text-align: left;
  font-size: 13px;
  font-weight: 500;
}

.tabela tbody tr {
  border-bottom: 1px solid #f0f0f0;
  transition: background 0.15s;
}

.tabela tbody tr:hover {
  background: #f8f9ff;
}

/* Destaque para o top 3 */
.tabela tbody tr.destaque {
  background: #fefdf0;
}

.tabela td {
  padding: 14px 16px;
  font-size: 14px;
  color: #333;
}

.posicao { font-size: 18px; text-align: center; }

.aluno { font-weight: 500; }

.simulado { color: #666; }

.acertos { color: #666; }

/* Classes de cor para o score */
.verde { color: #22c55e; font-weight: 600; }
.amarelo { color: #f59e0b; font-weight: 600; }
.vermelho { color: #ef4444; font-weight: 600; }

.data { color: #999; font-size: 13px; }

.vazio {
  text-align: center;
  color: #999;
  padding: 40px;
}
</style>
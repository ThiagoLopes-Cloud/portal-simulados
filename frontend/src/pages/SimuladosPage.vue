<template>
  <div class="simulados">

    <!-- Navbar -->
    <nav class="navbar">
      <h1>Portal de Simulados</h1>
      <div class="nav-links">
        <router-link to="/dashboard">Dashboard</router-link>
        <router-link to="/ranking">Ranking</router-link>
        <button @click="logout" class="btn-logout">Sair</button>
      </div>
    </nav>

    <!-- Conteúdo -->
    <div class="container">
      <h2>Simulados disponíveis</h2>
      <p class="subtitle">Escolha um simulado para começar</p>

      <!-- Estado de carregamento -->
      <div v-if="carregando" class="loading">
        Carregando simulados...
      </div>

      <!-- Mensagem de erro -->
      <div v-else-if="erro" class="erro">{{ erro }}</div>

      <!-- Lista de simulados -->
      <div v-else class="lista">
        <div
          v-for="simulado in simulados"
          :key="simulado.id"
          class="card"
        >
          <div class="card-header">
            <h3>{{ simulado.titulo }}</h3>
            <span class="badge">{{ simulado.total_questoes }} questões</span>
          </div>
          <p>{{ simulado.descricao || 'Sem descrição' }}</p>
          <button @click="iniciar(simulado.id)">Iniciar simulado →</button>
        </div>

        <!-- Mensagem quando não há simulados -->
        <div v-if="simulados.length === 0" class="vazio">
          Nenhum simulado disponível no momento.
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

// Lista de simulados retornados pela API
const simulados = ref([])
const carregando = ref(true)
const erro = ref('')

// Busca os simulados ao carregar a página
onMounted(async () => {
  try {
    const response = await api.get('/simulados/')
    simulados.value = response.data
  } catch (error) {
    erro.value = 'Erro ao carregar simulados.'
  } finally {
    carregando.value = false
  }
})

// Navega para a tela de prova com o ID do simulado
function iniciar(id) {
  router.push({ name: 'prova', params: { id } })
}

// Logout
function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  router.push({ name: 'login' })
}
</script>

<style scoped>
.simulados {
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

h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 8px;
}

.subtitle {
  color: #666;
  margin-bottom: 32px;
}

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

.lista {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.card {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.card-header h3 {
  font-size: 18px;
  color: #333;
}

.badge {
  background: #e8f0fe;
  color: #667eea;
  padding: 4px 12px;
  border-radius: 99px;
  font-size: 13px;
  font-weight: 500;
}

.card p {
  color: #666;
  font-size: 14px;
  margin-bottom: 16px;
}

.card button {
  background: #667eea;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.card button:hover {
  background: #5a6fd6;
}

.vazio {
  text-align: center;
  color: #999;
  padding: 40px;
}
</style>
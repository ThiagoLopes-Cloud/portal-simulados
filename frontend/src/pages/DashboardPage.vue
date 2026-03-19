<template>
  <div class="dashboard">

    <!-- Navbar -->
    <nav class="navbar">
      <h1>Portal de Simulados</h1>
      <div class="nav-links">
        <router-link to="/simulados">Simulados</router-link>
        <router-link to="/ranking">Ranking</router-link>
        <button @click="logout" class="btn-logout">Sair</button>
      </div>
    </nav>

    <!-- Conteúdo principal -->
    <div class="container">

      <!-- Boas vindas -->
      <div class="welcome">
        <h2>Bem-vindo, {{ username }}! 👋</h2>
        <p>O que você quer fazer hoje?</p>
      </div>

      <!-- Cards de ação -->
      <div class="cards">

        <!-- Card de simulados -->
        <div class="card" @click="$router.push('/simulados')">
          <div class="card-icon">📝</div>
          <h3>Simulados</h3>
          <p>Acesse os simulados disponíveis e teste seus conhecimentos</p>
          <button>Ver simulados</button>
        </div>

        <!-- Card de ranking -->
        <div class="card" @click="$router.push('/ranking')">
          <div class="card-icon">🏆</div>
          <h3>Ranking</h3>
          <p>Veja sua posição no ranking geral dos alunos</p>
          <button>Ver ranking</button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
// Importa as funções reativas do Vue
import { ref, onMounted } from 'vue'

// Importa o router para redirecionar após o logout
import { useRouter } from 'vue-router'

// Importa o serviço de API
import api from '../services/api.js'

const router = useRouter()

// Variável reativa para o nome do usuário
const username = ref('')

// onMounted — executado quando o componente é montado na tela
// Busca os dados do usuário logado
onMounted(async () => {
  try {
    // Busca o perfil do usuário autenticado
    const response = await api.get('/profile/')
    username.value = response.data.username
  } catch (error) {
    console.error('Erro ao buscar perfil:', error)
  }
})

// Função de logout — remove os tokens e redireciona para o login
function logout() {
  // Remove os tokens do localStorage
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')

  // Redireciona para o login
  router.push({ name: 'login' })
}
</script>

<style scoped>
.dashboard {
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

.navbar h1 {
  font-size: 20px;
  font-weight: 600;
}

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

.nav-links a:hover {
  opacity: 1;
}

.btn-logout {
  background: rgba(255,255,255,0.2);
  color: white;
  border: 1px solid rgba(255,255,255,0.4);
  padding: 6px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.btn-logout:hover {
  background: rgba(255,255,255,0.3);
}

.container {
  max-width: 900px;
  margin: 0 auto;
  padding: 40px 20px;
}

.welcome {
  margin-bottom: 32px;
}

.welcome h2 {
  font-size: 28px;
  color: #333;
  margin-bottom: 8px;
}

.welcome p {
  color: #666;
  font-size: 16px;
}

.cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 24px;
}

.card {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.08);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  text-align: center;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.card-icon {
  font-size: 48px;
  margin-bottom: 16px;
}

.card h3 {
  font-size: 20px;
  color: #333;
  margin-bottom: 8px;
}

.card p {
  color: #666;
  font-size: 14px;
  margin-bottom: 20px;
  line-height: 1.5;
}

.card button {
  background: #667eea;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background 0.2s;
}

.card button:hover {
  background: #5a6fd6;
}
</style>
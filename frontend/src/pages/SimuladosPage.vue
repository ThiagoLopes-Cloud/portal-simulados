<template>
  <div class="simulados-page">
    <nav class="navbar">
      <h1>Portal de Simulados</h1>
      <div class="nav-links">
        <router-link to="/dashboard">Dashboard</router-link>
        <router-link to="/turmas">Minhas Turmas</router-link>
        <button @click="logout" class="btn-logout">Sair</button>
      </div>
    </nav>

    <div class="container">
      <div class="header">
        <h2>📚 Simulados Disponíveis</h2>
        <p>Escolha uma prova para testar seus conhecimentos</p>
      </div>

      <div class="tabs-container">
        <button 
          class="tab-btn" 
          :class="{ active: activeTab === 'globais' }" 
          @click="activeTab = 'globais'"
        >
          🌍 Simulados Globais
        </button>
        <button 
          class="tab-btn tab-exclusiva" 
          :class="{ active: activeTab === 'exclusivos' }" 
          @click="activeTab = 'exclusivos'"
        >
          🔒 Minhas Turmas
          <span v-if="simuladosExclusivos.length" class="badge-count">{{ simuladosExclusivos.length }}</span>
        </button>
      </div>

      <div v-if="carregando" class="loading-spinner"></div>
      
      <div v-else class="tab-content">
        
        <div v-if="activeTab === 'globais'" class="grid-simulados">
          <div v-if="simuladosGlobais.length === 0" class="vazio">
            <p>Nenhum simulado global disponível no momento.</p>
          </div>
          <div v-for="simulado in simuladosGlobais" :key="simulado.id" class="card">
            <h3>{{ simulado.titulo }}</h3>
            <p class="descricao">{{ simulado.descricao || 'Teste seus conhecimentos gerais.' }}</p>
            <div class="card-footer">
              <button @click="$router.push(`/simulado/${simulado.id}`)" class="btn-iniciar">
                Iniciar Prova
              </button>
            </div>
          </div>
        </div>

        <div v-if="activeTab === 'exclusivos'" class="grid-simulados">
          <div v-if="simuladosExclusivos.length === 0" class="vazio">
            <p>Você não tem simulados fechados para fazer. Entre em uma turma usando um código de convite!</p>
            <button @click="$router.push('/turmas')" class="btn-secundario">Ir para Minhas Turmas</button>
          </div>
          
          <div v-for="simulado in simuladosExclusivos" :key="simulado.id" class="card card-premium">
            <div class="tag-premium">⭐ Exclusivo Metamorfose</div>
            <h3>{{ simulado.titulo }}</h3>
            <p class="descricao">{{ simulado.descricao || 'Simulado direcionado para a sua turma.' }}</p>
            <div class="card-footer">
              <button @click="$router.push(`/simulado/${simulado.id}`)" class="btn-iniciar-premium">
                Acessar Prova Fechada
              </button>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const carregando = ref(true)
const activeTab = ref('globais') // A aba padrão
const simuladosGlobais = ref([])
const simuladosExclusivos = ref([])

onMounted(async () => {
  try {
    const res = await api.get('/simulados/')
    // Recebe o novo formato do Backend (separado por chave)
    simuladosGlobais.value = res.data.globais || []
    simuladosExclusivos.value = res.data.exclusivos || []
  } catch (error) {
    console.error("Erro ao carregar simulados:", error)
  } finally {
    carregando.value = false
  }
})

function logout() {
  localStorage.clear()
  router.push('/login')
}
</script>

<style scoped>
.simulados-page { min-height: 100vh; background: #f5f5f5; }
.navbar {
  background: #667eea; color: white; padding: 16px 32px;
  display: flex; justify-content: space-between; align-items: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}
.nav-links { display: flex; gap: 24px; align-items: center; }
.nav-links a { color: white; text-decoration: none; font-size: 14px; }
.btn-logout { background: rgba(255,255,255,0.2); border: 1px solid rgba(255,255,255,0.4); padding: 6px 16px; color: white; border-radius: 6px; cursor: pointer; }

.container { max-width: 900px; margin: 40px auto; padding: 0 20px; }
.header { margin-bottom: 24px; text-align: center; }
.header h2 { font-size: 28px; color: #1f2937; margin-bottom: 8px; }
.header p { color: #6b7280; font-size: 15px; }

/* Tabs */
.tabs-container {
  display: flex; justify-content: center; gap: 12px; margin-bottom: 32px;
  border-bottom: 2px solid #e5e7eb; padding-bottom: 12px;
}
.tab-btn {
  background: none; border: none; font-size: 16px; font-weight: 600; color: #6b7280;
  padding: 10px 20px; cursor: pointer; position: relative; transition: color 0.2s;
}
.tab-btn:hover { color: #374151; }
.tab-btn.active { color: #667eea; }
.tab-btn.active::after {
  content: ''; position: absolute; bottom: -14px; left: 0; width: 100%;
  height: 3px; background: #667eea; border-radius: 3px 3px 0 0;
}
.tab-exclusiva.active { color: #8b5cf6; }
.tab-exclusiva.active::after { background: #8b5cf6; }

.badge-count {
  background: #8b5cf6; color: white; font-size: 11px; padding: 2px 8px;
  border-radius: 99px; margin-left: 6px; vertical-align: middle;
}

/* Grids e Cards */
.grid-simulados { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 20px; }
.card { background: white; border-radius: 12px; padding: 24px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); display: flex; flex-direction: column; }
.card h3 { font-size: 18px; color: #1f2937; margin-bottom: 8px; }
.descricao { color: #6b7280; font-size: 14px; margin-bottom: 24px; line-height: 1.5; flex-grow: 1; }

.card-premium { border: 2px solid #e0e7ff; background: #fafaff; position: relative; }
.tag-premium {
  position: absolute; top: -12px; right: 20px; background: #8b5cf6; color: white;
  font-size: 11px; font-weight: 700; padding: 4px 10px; border-radius: 99px; box-shadow: 0 2px 4px rgba(139,92,246,0.3);
}

.btn-iniciar, .btn-iniciar-premium, .btn-secundario {
  width: 100%; padding: 12px; border-radius: 8px; border: none; font-weight: 600;
  cursor: pointer; transition: transform 0.1s, opacity 0.2s; font-size: 14px;
}
.btn-iniciar { background: #667eea; color: white; }
.btn-iniciar:hover { opacity: 0.9; transform: translateY(-2px); }

.btn-iniciar-premium { background: #8b5cf6; color: white; }
.btn-iniciar-premium:hover { opacity: 0.9; transform: translateY(-2px); }

.btn-secundario { background: #e5e7eb; color: #374151; margin-top: 16px; width: auto; padding: 10px 24px; }
.vazio { grid-column: 1 / -1; text-align: center; padding: 60px 20px; color: #6b7280; background: white; border-radius: 12px; border: 1px dashed #d1d5db; }
.loading-spinner { border: 4px solid #f3f3f3; border-top: 4px solid #667eea; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 40px auto; }
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
</style>
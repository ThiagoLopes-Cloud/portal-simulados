<template>
  <div class="login-wrapper">
    <div class="login-container">
      <div class="clean-card login-box">
        
        <div class="logo-area">
          <h1 class="logo-text">
            <span class="color-primary">SIMUS</span><span class="color-dark">LAB</span>
          </h1>
          <p class="tagline text-dim">by Metamorfose</p>
        </div>
        
        <div class="welcome-text">
          <h2>Bem-vindo de volta</h2>
          <p>Acesse seu painel de performance e continue sua evolução.</p>
        </div>
        
        <div v-if="loginError" class="erro-alerta">
          Credenciais inválidas. Verifique seus dados e tente novamente.
        </div>
        
        <form @submit.prevent="handleLogin" class="login-form">
          <div class="input-group">
            <label for="username">Usuário ou E-mail</label>
            <input 
              type="text" 
              id="username" 
              v-model="username" 
              @input="loginError = false"
              placeholder="Digite seu usuário" 
              required
            >
          </div>
          
          <div class="input-group">
            <label for="password">Senha</label>
            <input 
              type="password" 
              id="password" 
              v-model="password" 
              @input="loginError = false"
              placeholder="••••••••" 
              required
            >
          </div>
          
          <button 
            type="submit" 
            class="btn-primary btn-login"
            :disabled="isLoading"
            :class="{ 'is-loading': isLoading }"
          >
            {{ isLoading ? 'Autenticando...' : 'Acessar Plataforma' }}
          </button>
        </form>
        
        <div class="register-link">
          <p class="text-dim">Ainda não tem conta? <router-link to="/register" class="link-destaque">Cadastre-se</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'

// A LÓGICA CONTINUA EXATAMENTE A MESMA (NADA QUEBRADO)
const router = useRouter()
const username = ref('')
const password = ref('')
const loginError = ref(false)
const isLoading = ref(false)

async function handleLogin() {
  loginError.value = false 
  isLoading.value = true 
  
  try {
    const response = await api.post('/api/login/', { 
      username: username.value, 
      password: password.value 
    })
    
    localStorage.setItem('access_token', response.data.access)
    if (response.data.refresh) {
      localStorage.setItem('refresh_token', response.data.refresh)
    }
    localStorage.setItem('user_role', response.data.role || 'student')
    
    router.push({ name: 'dashboard' })
  } catch (error) {
    console.error("Erro na autenticação:", error)
    loginError.value = true 
  } finally {
    isLoading.value = false 
  }
}
</script>

<style scoped>
/* Importando uma fonte limpa e moderna do Google (Inter) */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* --- NOVA PALETA CLEAN TECH --- */
.login-wrapper { 
  min-height: 100vh; 
  display: flex; 
  align-items: center; 
  justify-content: center; 
  /* Fundo degradê cinza super claro e elegante */
  background: linear-gradient(135deg, #F4F7F9 0%, #E8EEF2 100%); 
  font-family: 'Inter', sans-serif; 
}

.login-container { 
  width: 100%; 
  max-width: 420px; 
  padding: 20px; 
}

/* Card Branco Sofisticado (Substituindo o vidro escuro) */
.clean-card { 
  background: #FFFFFF; 
  padding: 40px 35px; 
  border-radius: 16px; 
  box-shadow: 0 12px 32px rgba(0, 0, 0, 0.08); /* Sombra difusa e chique */
  border: 1px solid rgba(0, 0, 0, 0.03);
}

/* Tipografia e Cores */
.logo-area { text-align: center; margin-bottom: 30px; }
.logo-text { font-size: 2rem; font-weight: 700; letter-spacing: -0.5px; margin: 0; }

/* Azul Institucional de Alta Confiança (ex: usado por bancos digitais/techs) */
.color-primary { color: #0052FF; } 
.color-dark { color: #0A2540; }
.text-dim { color: #6B7280; font-size: 0.85rem; }

.welcome-text { margin-bottom: 25px; text-align: center; }
.welcome-text h2 { color: #0A2540; font-size: 1.5rem; font-weight: 600; margin-bottom: 5px; }
.welcome-text p { color: #6B7280; font-size: 0.9rem; line-height: 1.5; margin: 0; }

/* Alerta de erro mais discreto e profissional */
.erro-alerta { 
  background: #FEF2F2; 
  border-left: 4px solid #EF4444; 
  color: #B91C1C; 
  padding: 12px 15px; 
  margin-bottom: 20px; 
  font-size: 0.85rem; 
  border-radius: 4px;
}

/* Formulário Moderno */
.login-form { display: flex; flex-direction: column; gap: 20px; }
.input-group { display: flex; flex-direction: column; gap: 6px; }

.input-group label { 
  font-size: 0.85rem; 
  font-weight: 500; 
  color: #374151; 
}

.input-group input { 
  background: #F9FAFB; 
  border: 1px solid #E5E7EB; 
  border-radius: 8px; 
  padding: 14px 16px; 
  color: #111827; 
  font-size: 1rem;
  transition: all 0.2s ease; 
  outline: none;
}

.input-group input:focus { 
  background: #FFFFFF;
  border-color: #0052FF; 
  box-shadow: 0 0 0 3px rgba(0, 82, 255, 0.1); /* Anel de foco moderno */
}

/* Botão de Ação Primária */
.btn-login { 
  background: #0052FF; 
  color: white;
  border: none;
  padding: 14px; 
  font-size: 1rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer; 
  transition: all 0.2s ease; 
  margin-top: 10px;
}

.btn-login:hover:not(:disabled) { 
  background: #0043D1; 
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(0, 82, 255, 0.2);
}

.btn-login:disabled { 
  opacity: 0.7; 
  cursor: not-allowed; 
}

/* Estado de Loading */
.btn-login.is-loading { 
  background-color: #6B7280; 
  animation: pulse 1.5s infinite; 
}

@keyframes pulse {
  0% { opacity: 0.8; }
  50% { opacity: 1; }
  100% { opacity: 0.8; }
}

/* Links */
.register-link { text-align: center; margin-top: 25px; }
.link-destaque { color: #0052FF; font-weight: 600; text-decoration: none; transition: color 0.2s; }
.link-destaque:hover { color: #0043D1; text-decoration: underline; }
</style>
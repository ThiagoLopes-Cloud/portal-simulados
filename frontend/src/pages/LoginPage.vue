<template>
  <div class="login-split-layout">
    
    <div class="form-side">
      <div class="login-container">
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

    <div class="brand-side">
      <div class="brand-content">
        <div class="badge-tech">Plataforma de Alta Performance</div>
        <h2 class="brand-title">O futuro da sua aprovação começa aqui.</h2>
        <p class="brand-subtitle">
          Utilize dados precisos e simulações realistas para mapear seus pontos cegos, otimizar seu tempo e garantir sua vaga.
        </p>
        
        <div class="abstract-graphic">
          <div class="bar bar-1"></div>
          <div class="bar bar-2"></div>
          <div class="bar bar-3"></div>
          <div class="bar bar-4"></div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'

// A lógica de conexão intocável!
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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

/* O Segredo: Ocupar a tela inteira e matar as listras escuras */
.login-split-layout { 
  display: flex;
  min-height: 100vh;
  /* Estas 3 linhas forçam o componente a ignorar os limites do Vue e esticar 100% */
  width: 100vw;
  position: absolute;
  top: 0;
  left: 0;
  font-family: 'Inter', sans-serif; 
  background-color: #FFFFFF;
}

/* LADO ESQUERDO - FORMULÁRIO */
.form-side {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #FFFFFF;
  padding: 20px;
}

.login-container { 
  width: 100%; 
  max-width: 400px; 
}

/* LADO DIREITO - BRANDING */
.brand-side {
  flex: 1.2; /* Ocupa um pouco mais de espaço que o formulário */
  background: linear-gradient(135deg, #0052FF 0%, #0A2540 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px;
  position: relative;
  overflow: hidden;
}

.brand-content {
  max-width: 500px;
  color: #FFFFFF;
  position: relative;
  z-index: 2;
}

.badge-tech {
  display: inline-block;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  padding: 6px 14px;
  border-radius: 99px;
  font-size: 0.75rem;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 24px;
}

.brand-title {
  font-size: 3rem;
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 20px;
  letter-spacing: -1px;
}

.brand-subtitle {
  font-size: 1.1rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 40px;
}

/* Gráfico abstrato de crescimento feito só com CSS */
.abstract-graphic {
  display: flex;
  align-items: flex-end;
  gap: 15px;
  height: 100px;
  opacity: 0.8;
}

.bar {
  width: 40px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 6px 6px 0 0;
  transition: all 0.5s ease;
}

.bar-1 { height: 30%; }
.bar-2 { height: 50%; }
.bar-3 { height: 75%; }
.bar-4 { height: 100%; background: #00D09C; /* Verde de sucesso/crescimento */ box-shadow: 0 0 20px rgba(0, 208, 156, 0.4); }

/* Partículas/Fundo abstrato da lateral azul */
.brand-side::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-image: radial-gradient(circle at 80% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 30%);
  z-index: 1;
}

/* RESPONSIVIDADE: Esconde o lado direito em celulares e tablets */
@media (max-width: 900px) {
  .brand-side { display: none; }
  .login-split-layout { position: relative; width: 100%; }
}

/* Tipografia e Estilos do Form */
.logo-area { margin-bottom: 40px; }
.logo-text { font-size: 2rem; font-weight: 700; letter-spacing: -0.5px; margin: 0; }
.color-primary { color: #0052FF; } 
.color-dark { color: #0A2540; }
.text-dim { color: #6B7280; font-size: 0.85rem; }

.welcome-text { margin-bottom: 30px; }
.welcome-text h2 { color: #0A2540; font-size: 1.6rem; font-weight: 700; margin-bottom: 8px; }
.welcome-text p { color: #6B7280; font-size: 0.95rem; line-height: 1.5; margin: 0; }

.erro-alerta { 
  background: #FEF2F2; 
  border-left: 4px solid #EF4444; 
  color: #B91C1C; 
  padding: 12px 15px; 
  margin-bottom: 20px; 
  font-size: 0.85rem; 
  border-radius: 4px;
}

.login-form { display: flex; flex-direction: column; gap: 20px; }
.input-group { display: flex; flex-direction: column; gap: 6px; }
.input-group label { font-size: 0.85rem; font-weight: 600; color: #374151; }

.input-group input { 
  background: #FFFFFF; 
  border: 1px solid #D1D5DB; 
  border-radius: 8px; 
  padding: 14px 16px; 
  color: #111827; 
  font-size: 1rem;
  transition: all 0.2s ease; 
  outline: none;
}

.input-group input:focus { 
  border-color: #0052FF; 
  box-shadow: 0 0 0 3px rgba(0, 82, 255, 0.1); 
}

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

.btn-login:hover:not(:disabled) { background: #0043D1; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0, 82, 255, 0.2); }
.btn-login:disabled { opacity: 0.7; cursor: not-allowed; }
.btn-login.is-loading { background-color: #6B7280; animation: pulse 1.5s infinite; }
@keyframes pulse { 0% { opacity: 0.8; } 50% { opacity: 1; } 100% { opacity: 0.8; } }
.register-link { margin-top: 25px; }
.link-destaque { color: #0052FF; font-weight: 600; text-decoration: none; transition: color 0.2s; }
.link-destaque:hover { color: #0043D1; text-decoration: underline; }
</style>
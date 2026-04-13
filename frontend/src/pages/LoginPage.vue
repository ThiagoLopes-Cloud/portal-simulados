<template>
  <div class="login-wrapper">
    <div class="tech-background"></div>

    <div class="login-container">
      <div class="glass-card login-box">
        
        <div class="logo-area">
          <h1 class="ui-display logo-text"><span class="color-primary">SIMUS</span><span class="color-secondary">LAB</span></h1>
          <p class="tagline text-dim">by Metamorfose</p>
        </div>

        <div class="welcome-text">
          <h2 class="ui-display">Pronto para a Batalha?</h2>
          <p>Acesse seu cockpit tático e continue sua evolução.</p>
        </div>

        <div v-if="loginError" class="erro-alerta ui-display">
          ⚠️ Credenciais inválidas. Tente novamente.
        </div>

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="input-group">
            <label for="username" class="ui-display">Usuário ou E-mail</label>
            <input 
              type="text" 
              id="username" 
              v-model="username" 
              placeholder="Digite seu usuário" 
              required
            >
          </div>

          <div class="input-group">
            <label for="password" class="ui-display">Senha Tática</label>
            <input 
              type="password" 
              id="password" 
              v-model="password" 
              placeholder="••••••••" 
              required
            >
          </div>

          <div class="form-actions">
            <a href="#" class="forgot-password text-dim">Esqueceu a senha?</a>
          </div>

          <button type="submit" class="btn-primary ui-display btn-login">
            Entrar na Arena
          </button>
        </form>

        <div class="register-link">
          <p class="text-dim">Novo no esquadrão? <router-link to="/register" class="color-secondary font-bold">Aliste-se aqui</router-link></p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'

const router = useRouter()
const username = ref('')
const password = ref('')
const loginError = ref(false)

async function handleLogin() {
  loginError.value = false 
  try {
    // AJUSTE FINAL: Rota '/api/login/' conforme definido no seu users/urls.py
    const response = await api.post('/api/login/', { 
      username: username.value, 
      password: password.value 
    })
    
    // Armazenamento dos tokens para o Vue Router
    localStorage.setItem('access_token', response.data.access)
    
    if (response.data.refresh) {
      localStorage.setItem('refresh_token', response.data.refresh)
    }
    
    // Armazenamento do cargo do usuário
    if (response.data.role) {
      localStorage.setItem('user_role', response.data.role)
    } else {
      localStorage.setItem('user_role', 'student')
    }
    
    console.log("Acesso concedido. Navegando para o Dashboard...")
    
    // Redirecionamento usando o nome da rota definido no router/index.js
    router.push({ name: 'dashboard' })
    
  } catch (error) {
    console.error("Erro na autenticação:", error)
    loginError.value = true 
  }
}
</script>

<style scoped>
.login-wrapper {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-dark);
  overflow: hidden;
}

.tech-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url('../assets/login-bg-neon.png'); 
  background-size: cover;
  background-position: center;
  z-index: 1;
}

.tech-background::after {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: radial-gradient(circle at center, rgba(11, 15, 25, 0.4) 0%, rgba(11, 15, 25, 0.9) 100%);
}

.login-container {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 420px;
  padding: 20px;
}

.login-box {
  padding: 40px 30px;
  background: rgba(11, 15, 25, 0.6);
  border: 1px solid rgba(0, 229, 255, 0.2);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), inset 0 0 20px rgba(0, 229, 255, 0.05);
}

.logo-area {
  text-align: center;
  margin-bottom: 30px;
}

.logo-text {
  font-size: 2rem;
  letter-spacing: 2px;
  margin-bottom: -5px;
}

.tagline {
  font-size: 0.8rem;
  letter-spacing: 3px;
  text-transform: uppercase;
}

.welcome-text {
  text-align: center;
  margin-bottom: 25px;
}

.welcome-text h2 {
  font-size: 1.4rem;
  color: var(--text-main);
  margin-bottom: 5px;
}

.welcome-text p {
  font-size: 0.9rem;
  color: var(--text-dim);
}

.erro-alerta {
  background: rgba(255, 42, 85, 0.1);
  border: 1px solid var(--color-error);
  color: var(--color-error);
  padding: 10px;
  border-radius: 8px;
  text-align: center;
  font-size: 0.85rem;
  margin-bottom: 20px;
  box-shadow: 0 0 10px rgba(255, 42, 85, 0.2);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.input-group label {
  font-size: 0.75rem;
  color: var(--color-primary);
  letter-spacing: 1px;
}

.input-group input {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 8px;
  padding: 14px 16px;
  color: var(--text-main);
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 1rem;
  transition: all 0.3s ease;
  outline: none;
}

.input-group input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.2);
  background: rgba(0, 229, 255, 0.02);
}

.input-group input::placeholder {
  color: rgba(156, 163, 175, 0.3);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
}

.forgot-password {
  font-size: 0.8rem;
  text-decoration: none;
  transition: color 0.2s;
}

.forgot-password:hover {
  color: var(--color-primary);
}

.btn-login {
  padding: 16px;
  font-size: 1rem;
  letter-spacing: 1px;
  border-radius: 8px;
  cursor: pointer;
  margin-top: 10px;
}

.register-link {
  text-align: center;
  margin-top: 25px;
  font-size: 0.9rem;
}

.register-link a {
  text-decoration: none;
  transition: text-shadow 0.3s;
}

.register-link a:hover {
  text-shadow: var(--glow-secondary);
}

.color-primary { color: var(--color-primary); }
.color-secondary { color: var(--color-secondary); }
.text-dim { color: var(--text-dim); }
.font-bold { font-weight: 700; }
</style>
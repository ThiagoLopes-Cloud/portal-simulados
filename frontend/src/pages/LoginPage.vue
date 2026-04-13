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
            <input type="text" id="username" v-model="username" placeholder="Digite seu usuário" required>
          </div>
          <div class="input-group">
            <label for="password" class="ui-display">Senha Tática</label>
            <input type="password" id="password" v-model="password" placeholder="••••••••" required>
          </div>
          <button type="submit" class="btn-primary ui-display btn-login">Entrar na Arena</button>
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
    // ESTA É A ROTA QUE O SEU DJANGO EXIGE: /api/login/
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
  }
}
</script>

<style scoped>
.login-wrapper { position: relative; min-height: 100vh; display: flex; align-items: center; justify-content: center; background-color: var(--bg-dark); overflow: hidden; }
.tech-background { position: absolute; top: 0; left: 0; width: 100%; height: 100%; background-image: url('../assets/login-bg-neon.png'); background-size: cover; background-position: center; z-index: 1; }
.tech-background::after { content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: radial-gradient(circle at center, rgba(11, 15, 25, 0.4) 0%, rgba(11, 15, 25, 0.9) 100%); }
.login-container { position: relative; z-index: 2; width: 100%; max-width: 420px; padding: 20px; }
.login-box { padding: 40px 30px; background: rgba(11, 15, 25, 0.6); border: 1px solid rgba(0, 229, 255, 0.2); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5); }
.logo-text { font-size: 2rem; letter-spacing: 2px; }
.color-primary { color: var(--color-primary); }
.color-secondary { color: var(--color-secondary); }
.text-dim { color: var(--text-dim); }
.erro-alerta { background: rgba(255, 42, 85, 0.1); border: 1px solid var(--color-error); color: var(--color-error); padding: 10px; margin-bottom: 20px; text-align: center; }
.login-form { display: flex; flex-direction: column; gap: 20px; }
.input-group { display: flex; flex-direction: column; gap: 8px; }
.input-group input { background: rgba(255, 255, 255, 0.03); border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 8px; padding: 14px; color: white; outline: none; }
.btn-login { padding: 16px; cursor: pointer; }
</style>
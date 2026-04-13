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

        <form @submit.prevent="handleLogin" class="login-form">
          <div class="input-group">
            <label for="email" class="ui-display">E-mail de Acesso</label>
            <input 
              type="email" 
              id="email" 
              v-model="email" 
              placeholder="recruta@metamorfose.com.br" 
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
import api from '../services/api.js' // 1. Descomentamos a importação da API!

const router = useRouter()
// Note que seu backend original provavelmente usava username em vez de email,
// então vamos manter a variável 'username' aqui para garantir a conexão com o Django.
const username = ref('') 
const password = ref('')

async function handleLogin() {
  try {
    // 2. Religa a chamada oficial para o seu backend Django!
    // Se o seu endpoint for diferente de '/token/' (ex: '/login/'), é só ajustar.
    const response = await api.post('/token/', { 
      username: username.value, 
      password: password.value 
    })
    
    // 3. Salva os crachás de acesso no navegador
    localStorage.setItem('access_token', response.data.access)
    if (response.data.refresh) {
      localStorage.setItem('refresh_token', response.data.refresh)
    }
    
    // Se o seu backend manda a role do usuário no login, salvamos também
    if (response.data.role) {
      localStorage.setItem('user_role', response.data.role)
    } else {
      // Valor padrão caso não venha na API
      localStorage.setItem('user_role', 'student') 
    }
    
    console.log("Acesso concedido à Arena!")
    router.push('/dashboard')
    
  } catch (error) {
    console.error("Falha na autenticação:", error)
    alert('Credenciais inválidas! Tente novamente, recruta.')
  }
}
</script>

<style scoped>
/* A estrutura base herda do nosso Design System global, mas estilizamos os escopos locais aqui */

.login-wrapper {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--bg-dark);
  overflow: hidden;
}

/* Background Imersivo com overlay escuro para não ofuscar o formulário */
.tech-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  /* 👇 CORREÇÃO AQUI: Dois pontinhos antes da barra */
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
  background: rgba(11, 15, 25, 0.6); /* Mais escuro que o padrão para contraste extra */
  border: 1px solid rgba(0, 229, 255, 0.2); /* Borda sutil cyan */
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
  margin-bottom: 30px;
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

/* Utilitários Locais */
.color-primary { color: var(--color-primary); }
.color-secondary { color: var(--color-secondary); }
.text-dim { color: var(--text-dim); }
.font-bold { font-weight: 700; }

/* Estilo específico para o "LAB" com brilho Neon Magenta */
.color-secondary {
  color: var(--color-secondary); /* Aplica a cor Magenta */
  text-shadow: var(--glow-secondary); /* Adiciona o brilho Neon Magenta */
}
</style>
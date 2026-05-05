<template>
  <div class="register-split-layout">
    
    <div class="form-side">
      <div class="register-container">
        
        <div class="logo-area">
          <h1 class="logo-text">
            <span class="color-primary">SIMUS</span><span class="color-dark">LAB</span>
          </h1>
          <p class="tagline text-dim">by Metamorfose</p>
        </div>
        
        <div class="welcome-text">
          <h2>Crie sua conta</h2>
          <p>Junte-se ao laboratório e inicie sua jornada de alta performance.</p>
        </div>
        
        <div v-if="erro" class="erro-alerta">
          {{ erro }}
        </div>

        <div v-if="sucesso" class="sucesso-alerta">
          Conta criada com sucesso! Preparando seu painel...
        </div>
        
        <form @submit.prevent="register" class="register-form">
          <div class="input-group">
            <label for="username">Usuário</label>
            <input 
              type="text" 
              id="username" 
              v-model="username" 
              placeholder="Ex: joao.silva" 
              required
              :disabled="carregando || sucesso"
            />
          </div>
          
          <div class="input-group">
            <label for="email">E-mail</label>
            <input 
              type="email" 
              id="email" 
              v-model="email" 
              placeholder="seu@email.com" 
              required
              :disabled="carregando || sucesso"
            />
          </div>
          
          <div class="password-grid">
            <div class="input-group">
              <label for="password">Senha</label>
              <input 
                type="password" 
                id="password" 
                v-model="password" 
                placeholder="••••••••" 
                required
                :disabled="carregando || sucesso"
              />
            </div>
            
            <div class="input-group">
              <label for="password2">Confirmar Senha</label>
              <input 
                type="password" 
                id="password2" 
                v-model="password2" 
                placeholder="••••••••" 
                required
                :disabled="carregando || sucesso"
              />
            </div>
          </div>
          
          <button 
            type="submit" 
            class="btn-primary btn-register"
            :disabled="carregando || sucesso"
            :class="{ 'is-loading': carregando }"
          >
            {{ carregando ? 'Processando dados...' : 'Criar Conta' }}
          </button>
        </form>
        
        <div class="login-link">
          <p class="text-dim">Já faz parte do laboratório? <router-link to="/login" class="link-destaque">Faça login</router-link></p>
        </div>
      </div>
    </div>

    <div class="brand-side">
      <div class="brand-content">
        <div class="badge-tech">Acesso Restrito</div>
        <h2 class="brand-title">Transforme esforço em estratégia.</h2>
        <p class="brand-subtitle">
          Crie seu perfil para acessar simulações realistas, mapear seus pontos fracos e receber recomendações focadas na sua aprovação.
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

const router = useRouter()

const username = ref('')   
const email = ref('')      
const password = ref('')   
const password2 = ref('') 
const erro = ref('')       
const sucesso = ref(false) 
const carregando = ref(false) 

async function register() {
  erro.value = ''
  sucesso.value = false

  if (!username.value || !email.value || !password.value || !password2.value) {
    erro.value = 'Preencha todos os campos.'
    return
  }

  if (password.value !== password2.value) {
    erro.value = 'As senhas não conferem.'
    return
  }

  carregando.value = true

  try {
    await api.post('/api/register/', {
      username: username.value,
      email: email.value,
      password: password.value,
      password2: password2.value,
      role: 'student', 
    })

    sucesso.value = true

    setTimeout(() => {
      router.push({ name: 'login' })
    }, 2000)

  } catch (error) {
    if (error.response?.data) {
      const erros = error.response.data
      const primeiroErro = Object.values(erros)[0]
      erro.value = Array.isArray(primeiroErro) ? primeiroErro[0] : primeiroErro
    } else {
      erro.value = 'Erro ao criar conta. Tente novamente.'
    }
  } finally {
    carregando.value = false
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.register-split-layout { 
  display: flex;
  min-height: 100vh;
  width: 100vw;
  position: absolute;
  top: 0;
  left: 0;
  font-family: 'Inter', sans-serif; 
  background-color: #FFFFFF;
}

.form-side {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #FFFFFF;
  padding: 20px;
}

.register-container { 
  width: 100%; 
  max-width: 420px; 
}

.brand-side {
  flex: 1.2; 
  background: linear-gradient(135deg, #0A2540 0%, #0052FF 100%);
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
  font-size: 2.8rem;
  font-weight: 700;
  line-height: 1.1;
  margin-bottom: 20px;
  letter-spacing: -1px;
}

.brand-subtitle {
  font-size: 1.05rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.8);
  margin-bottom: 40px;
}

.abstract-graphic {
  display: flex; align-items: flex-end; gap: 15px; height: 100px; opacity: 0.8;
}
.bar { width: 40px; background: rgba(255, 255, 255, 0.2); border-radius: 6px 6px 0 0; transition: all 0.5s ease; }
.bar-1 { height: 40%; } .bar-2 { height: 60%; } .bar-3 { height: 80%; }
.bar-4 { height: 100%; background: #00D09C; box-shadow: 0 0 20px rgba(0, 208, 156, 0.4); }

.brand-side::after {
  content: ''; position: absolute; top: 0; left: 0; right: 0; bottom: 0;
  background-image: radial-gradient(circle at 20% 80%, rgba(255, 255, 255, 0.05) 0%, transparent 30%);
  z-index: 1;
}

@media (max-width: 900px) {
  .brand-side { display: none; }
  .register-split-layout { position: relative; width: 100%; }
  .password-grid { grid-template-columns: 1fr !important; gap: 15px !important; }
}

@media (max-width: 480px) {
  .form-side { padding: 16px; align-items: flex-start; padding-top: 40px; }
  .logo-area { margin-bottom: 22px; }
  .welcome-text { margin-bottom: 18px; }
  .welcome-text h2 { font-size: 1.35rem; }
  .register-form { gap: 14px; }
  .input-group input { padding: 12px 14px; }
  .btn-register { padding: 13px; font-size: 0.95rem; }
}

.logo-area { margin-bottom: 30px; }
.logo-text { font-size: 2rem; font-weight: 700; letter-spacing: -0.5px; margin: 0; }
.color-primary { color: #0052FF; } 
.color-dark { color: #0A2540; }
.text-dim { color: #6B7280; font-size: 0.85rem; }

.welcome-text { margin-bottom: 25px; }
.welcome-text h2 { color: #0A2540; font-size: 1.6rem; font-weight: 700; margin-bottom: 5px; }
.welcome-text p { color: #6B7280; font-size: 0.95rem; line-height: 1.5; margin: 0; }

.erro-alerta { 
  background: #FEF2F2; border-left: 4px solid #EF4444; color: #B91C1C; 
  padding: 12px 15px; margin-bottom: 20px; font-size: 0.85rem; border-radius: 4px;
}

.sucesso-alerta { 
  background: #ECFDF5; border-left: 4px solid #10B981; color: #047857; 
  padding: 12px 15px; margin-bottom: 20px; font-size: 0.85rem; border-radius: 4px; font-weight: 500;
}

.register-form { display: flex; flex-direction: column; gap: 16px; }
.input-group { display: flex; flex-direction: column; gap: 6px; }
.password-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; }

.input-group label { font-size: 0.85rem; font-weight: 600; color: #374151; }

.input-group input { 
  background: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 8px; 
  padding: 12px 14px; color: #111827; font-size: 0.95rem;
  transition: all 0.2s ease; outline: none;
}

.input-group input:focus { 
  border-color: #0052FF; box-shadow: 0 0 0 3px rgba(0, 82, 255, 0.1); 
}

.input-group input:disabled { background: #F3F4F6; cursor: not-allowed; opacity: 0.7; }

.btn-register { 
  background: #0052FF; color: white; border: none; padding: 14px; 
  font-size: 1rem; font-weight: 600; border-radius: 8px; cursor: pointer; 
  transition: all 0.2s ease; margin-top: 10px;
}

.btn-register:hover:not(:disabled) { background: #0043D1; transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0, 82, 255, 0.2); }
.btn-register:disabled { opacity: 0.7; cursor: not-allowed; }
.btn-register.is-loading { background-color: #6B7280; animation: pulse 1.5s infinite; }

@keyframes pulse { 0% { opacity: 0.8; } 50% { opacity: 1; } 100% { opacity: 0.8; } }

.login-link { margin-top: 25px; text-align: center; }
.link-destaque { color: #0052FF; font-weight: 600; text-decoration: none; transition: color 0.2s; }
.link-destaque:hover { color: #0043D1; text-decoration: underline; }
</style>
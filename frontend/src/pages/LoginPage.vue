<template>
  <!-- Container principal centralizado na tela -->
  <div class="login-container">
    <div class="login-card">

      <!-- Cabeçalho da página -->
      <h1>Portal de Simulados</h1>
      <p class="subtitle">Faça login para continuar</p>

      <!-- Mensagem de erro — aparece apenas se houver erro -->
      <div v-if="erro" class="erro">{{ erro }}</div>

      <!-- Formulário de login -->
      <div class="form">

        <!-- Campo de usuário -->
        <div class="field">
          <label>Usuário</label>
          <input
            v-model="username"
            type="text"
            placeholder="Digite seu usuário"
          />
        </div>

        <!-- Campo de senha -->
        <div class="field">
          <label>Senha</label>
          <input
            v-model="password"
            type="password"
            placeholder="Digite sua senha"
          />
        </div>

        <!-- Botão de login — desabilitado durante o carregamento -->
        <button @click="login" :disabled="carregando">
          {{ carregando ? 'Entrando...' : 'Entrar' }}
        </button>

        <!-- Link para a página de registro -->
        <p class="link">
          Não tem conta?
          <router-link to="/register">Cadastre-se</router-link>
        </p>

      </div>
    </div>
  </div>
</template>

<script setup>
// Importa as funções reativas do Vue
import { ref } from 'vue'

// Importa o router para redirecionar após o login
import { useRouter } from 'vue-router'

// Importa o serviço de API que configuramos
import api from '../services/api.js'

// useRouter — permite navegar entre páginas programaticamente
const router = useRouter()

// ref() — cria variáveis reativas
// Quando o valor muda, o Vue atualiza a tela automaticamente
const username = ref('')      // Valor do campo usuário
const password = ref('')      // Valor do campo senha
const erro = ref('')          // Mensagem de erro
const carregando = ref(false) // Controla o estado do botão

// Função de login — chamada ao clicar no botão
async function login() {
  // Limpa o erro anterior
  erro.value = ''

  // Ativa o estado de carregamento
  carregando.value = true

  try {
    // Faz a requisição POST para a API de login
    // Envia username e password para o Django
    const response = await api.post('/login/', {
      username: username.value,
      password: password.value,
    })

    // Salva os tokens no localStorage do browser
    // O interceptor do axios vai usar esses tokens automaticamente
    localStorage.setItem('access_token', response.data.access)
    localStorage.setItem('refresh_token', response.data.refresh)

    // Após salvar access_token e refresh_token, busca o perfil para obter o role
    const perfil = await api.get('/profile/')
    localStorage.setItem('user_role', perfil.data.role)

    // Redireciona para o dashboard após o login
    router.push({ name: 'dashboard' })

  } catch (error) {
    // Se o login falhar, exibe a mensagem de erro
    erro.value = 'Usuário ou senha incorretos.'

  } finally {
    // Desativa o estado de carregamento independente do resultado
    carregando.value = false
  }
}
</script>

<style scoped>
/* scoped — os estilos só se aplicam a esse componente */

.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  background: white;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.2);
  width: 100%;
  max-width: 400px;
}

h1 {
  font-size: 24px;
  color: #333;
  margin-bottom: 8px;
  text-align: center;
}

.subtitle {
  color: #666;
  text-align: center;
  margin-bottom: 24px;
}

.erro {
  background: #fee;
  color: #c00;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 16px;
  font-size: 14px;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

label {
  font-size: 14px;
  font-weight: 500;
  color: #444;
}

input {
  padding: 10px 14px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

input:focus {
  border-color: #667eea;
}

button {
  padding: 12px;
  background: #667eea;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 16px;
  cursor: pointer;
  transition: background 0.2s;
}

button:hover:not(:disabled) {
  background: #5a6fd6;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.link {
  text-align: center;
  font-size: 14px;
  color: #666;
}

.link a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}
</style>
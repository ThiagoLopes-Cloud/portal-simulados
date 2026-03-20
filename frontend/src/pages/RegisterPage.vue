<template>
  <!-- Container principal centralizado na tela -->
  <div class="register-container">
    <div class="register-card">

      <!-- Cabeçalho da página -->
      <h1>Portal de Simulados</h1>
      <p class="subtitle">Crie sua conta para começar</p>

      <!-- Mensagem de erro — aparece apenas se houver erro -->
      <div v-if="erro" class="erro">{{ erro }}</div>

      <!-- Mensagem de sucesso — aparece após o cadastro -->
      <div v-if="sucesso" class="sucesso">
        Conta criada com sucesso! Redirecionando...
      </div>

      <!-- Formulário de registro -->
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

        <!-- Campo de email -->
        <div class="field">
          <label>Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="Digite seu email"
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

        <!-- Campo de confirmação de senha -->
        <div class="field">
          <label>Confirmar senha</label>
          <input
            v-model="password2"
            type="password"
            placeholder="Confirme sua senha"
          />
        </div>

        <!-- Botão de registro -->
        <button @click="register" :disabled="carregando">
          {{ carregando ? 'Criando conta...' : 'Criar conta' }}
        </button>

        <!-- Link para a página de login -->
        <p class="link">
          Já tem conta?
          <router-link to="/login">Faça login</router-link>
        </p>

      </div>
    </div>
  </div>
</template>

<script setup>
// Importa as funções reativas do Vue
import { ref } from 'vue'

// Importa o router para redirecionar após o registro
import { useRouter } from 'vue-router'

// Importa o serviço de API
import api from '../services/api.js'

const router = useRouter()

// Variáveis reativas do formulário
const username = ref('')   // Campo usuário
const email = ref('')      // Campo email
const password = ref('')   // Campo senha
const password2 = ref('') // Campo confirmar senha
const erro = ref('')       // Mensagem de erro
const sucesso = ref(false) // Controla mensagem de sucesso
const carregando = ref(false) // Controla o estado do botão

// Função de registro — chamada ao clicar no botão
async function register() {
  // Limpa mensagens anteriores
  erro.value = ''
  sucesso.value = false

  // Validação básica no frontend
  if (!username.value || !email.value || !password.value || !password2.value) {
    erro.value = 'Preencha todos os campos.'
    return
  }

  // Verifica se as senhas conferem
  if (password.value !== password2.value) {
    erro.value = 'As senhas não conferem.'
    return
  }

  // Ativa o estado de carregamento
  carregando.value = true

  try {
    // Faz a requisição POST para a API de registro
    await api.post('/register/', {
      username: username.value,
      email: email.value,
      password: password.value,
      password2: password2.value,
      role: 'student', // Todo novo usuário é criado como estudante
    })

    // Exibe mensagem de sucesso
    sucesso.value = true

    // Aguarda 2 segundos e redireciona para o login
    setTimeout(() => {
      router.push({ name: 'login' })
    }, 2000)

  } catch (error) {
    // Trata os erros retornados pela API
    if (error.response?.data) {
      // Pega o primeiro erro retornado pelo Django
      const erros = error.response.data
      const primeiroErro = Object.values(erros)[0]
      erro.value = Array.isArray(primeiroErro) ? primeiroErro[0] : primeiroErro
    } else {
      erro.value = 'Erro ao criar conta. Tente novamente.'
    }

  } finally {
    // Desativa o estado de carregamento
    carregando.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.register-card {
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

.sucesso {
  background: #f0fdf4;
  color: #16a34a;
  padding: 10px;
  border-radius: 6px;
  margin-bottom: 16px;
  font-size: 14px;
  text-align: center;
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
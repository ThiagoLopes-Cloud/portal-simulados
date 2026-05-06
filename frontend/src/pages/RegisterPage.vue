<template>
  <AuthLayout>
    <div class="mb-8">
      <SimuslabLogo size="md" class="mb-6" />
      <h2 class="register-title">Crie sua conta</h2>
      <p class="register-sub">Junte-se ao laboratório e inicie sua jornada de alta performance.</p>
    </div>

    <div v-if="erro" class="alert alert--error">{{ erro }}</div>
    <div v-if="sucesso" class="alert alert--success">Conta criada! Redirecionando...</div>

    <form @submit.prevent="register" class="form-stack">
      <SimuslabInput
        v-model="username"
        label="Usuário"
        placeholder="ex: joao.silva"
        :disabled="carregando || sucesso"
        required
      />
      <SimuslabInput
        v-model="email"
        label="E-mail"
        type="email"
        placeholder="seu@email.com"
        :disabled="carregando || sucesso"
        required
      />
      <div class="grid-2">
        <SimuslabInput
          v-model="password"
          label="Senha"
          type="password"
          placeholder="••••••••"
          :disabled="carregando || sucesso"
          required
        />
        <SimuslabInput
          v-model="password2"
          label="Confirmar"
          type="password"
          placeholder="••••••••"
          :disabled="carregando || sucesso"
          required
        />
      </div>

      <SimuslabButton
        type="submit"
        variant="primary"
        size="lg"
        block
        :loading="carregando"
        :disabled="sucesso"
      >
        Criar Conta
      </SimuslabButton>
    </form>

    <p class="register-footer">
      Já faz parte do laboratório?
      <router-link to="/login" class="link-orbit">Faça login</router-link>
    </p>
  </AuthLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'
import AuthLayout from '../layouts/AuthLayout.vue'
import SimuslabLogo from '../components/ui/SimuslabLogo.vue'
import SimuslabInput from '../components/ui/SimuslabInput.vue'
import SimuslabButton from '../components/ui/SimuslabButton.vue'

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
    })
    sucesso.value = true
    setTimeout(() => router.push({ name: 'login' }), 2000)
  } catch (error) {
    if (error.response?.data) {
      const erros = error.response.data
      const primeiro = Object.values(erros)[0]
      erro.value = Array.isArray(primeiro) ? primeiro[0] : primeiro
    } else {
      erro.value = 'Erro ao criar conta. Tente novamente.'
    }
  } finally {
    carregando.value = false
  }
}
</script>

<style scoped>
.register-title {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  margin-bottom: var(--space-2);
}
.register-sub {
  font-size: var(--text-sm);
  color: var(--color-comet);
  line-height: var(--leading-relaxed);
}
.form-stack { display: flex; flex-direction: column; gap: var(--space-4); }
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-3); }
.alert {
  padding: var(--space-3) var(--space-4);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  margin-bottom: var(--space-5);
}
.alert--error  { background: var(--color-nova-dim); border: 1px solid var(--color-nova-border); color: var(--color-nova); }
.alert--success { background: var(--color-stellar-dim); border: 1px solid var(--color-stellar-border); color: var(--color-stellar); }
.register-footer { margin-top: var(--space-7); text-align: center; font-size: var(--text-sm); color: var(--color-dust); }
.link-orbit { color: var(--color-orbit); font-weight: var(--weight-semibold); text-decoration: none; margin-left: var(--space-1); }
.link-orbit:hover { text-decoration: underline; }
</style>

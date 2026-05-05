<template>
  <AuthLayout>
    <!-- Logo mobile (só aparece sem o painel esquerdo) -->
    <div class="login-logo-mobile">
      <OrbynLogo size="md" />
    </div>

    <div class="login-header">
      <h2 class="login-title">Bem-vindo de volta</h2>
      <p class="login-subtitle">Acesse seu painel de performance e continue sua evolução.</p>
    </div>

    <!-- Erro -->
    <div v-if="loginError" class="login-error" role="alert">
      <span class="error-icon">✕</span>
      <span>Credenciais inválidas. Verifique seus dados e tente novamente.</span>
    </div>

    <!-- Formulário -->
    <form @submit.prevent="handleLogin" class="login-form">
      <OrbynInput
        v-model="username"
        label="Usuário ou E-mail"
        placeholder="Digite seu usuário"
        required
        autocomplete="username"
        @input="loginError = false"
      />

      <OrbynInput
        v-model="password"
        label="Senha"
        type="password"
        placeholder="••••••••"
        required
        autocomplete="current-password"
        @input="loginError = false"
      />

      <OrbynButton
        type="submit"
        variant="primary"
        size="lg"
        block
        :loading="isLoading"
      >
        Acessar Plataforma
        <template #loading>Autenticando...</template>
      </OrbynButton>
    </form>

    <p class="login-register">
      Ainda não tem conta?
      <router-link to="/register" class="register-link">Cadastre-se</router-link>
    </p>
  </AuthLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'
import AuthLayout  from '../layouts/AuthLayout.vue'
import OrbynLogo   from '../components/ui/OrbynLogo.vue'
import OrbynButton from '../components/ui/OrbynButton.vue'
import OrbynInput  from '../components/ui/OrbynInput.vue'

const router    = useRouter()
const username  = ref('')
const password  = ref('')
const loginError = ref(false)
const isLoading  = ref(false)

async function handleLogin() {
  loginError.value = false
  isLoading.value  = true

  try {
    const response = await api.post('/api/login/', {
      username: username.value,
      password: password.value,
    })

    localStorage.setItem('access_token', response.data.access)
    if (response.data.refresh) localStorage.setItem('refresh_token', response.data.refresh)
    localStorage.setItem('user_role', response.data.role || 'student')
    if (response.data.username) localStorage.setItem('username', response.data.username)

    router.push({ name: 'dashboard' }).then(() => window.location.reload())
  } catch {
    loginError.value = true
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
/* Mobile logo (hidden on desktop when brand panel shows) */
.login-logo-mobile { display: none; margin-bottom: var(--space-8); }
@media (max-width: 768px) { .login-logo-mobile { display: flex; } }

/* Header */
.login-header { margin-bottom: var(--space-7); }

.login-title {
  font-family: var(--font-display);
  font-size: var(--text-2xl);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  margin-bottom: var(--space-2);
}

.login-subtitle {
  font-size: var(--text-base);
  color: var(--color-comet);
  line-height: var(--leading-relaxed);
}

/* Error banner */
.login-error {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  background: var(--color-nova-dim);
  border: 1px solid var(--color-nova-border);
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-4);
  color: var(--color-nova);
  font-size: var(--text-base);
  margin-bottom: var(--space-5);
}

.error-icon {
  font-weight: var(--weight-bold);
  flex-shrink: 0;
}

/* Form */
.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
  margin-bottom: var(--space-7);
}

/* Register link */
.login-register {
  text-align: center;
  font-size: var(--text-base);
  color: var(--color-comet);
}

.register-link {
  color: var(--color-orbit);
  font-weight: var(--weight-semibold);
  margin-left: var(--space-1);
  transition: color var(--transition-fast);
}
.register-link:hover { color: var(--color-orbit-bright); }
</style>

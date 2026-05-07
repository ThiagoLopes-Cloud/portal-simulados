<template>
  <AuthLayout>
    <div class="login-form-wrapper">

      <!-- Cabeçalho do formulário -->
      <div class="login-header">
        <span class="login-label">Plataforma de Simulados</span>
        <h2 class="login-title">Bem-vindo de volta</h2>
        <p class="login-subtitle">Acesse seu painel e continue evoluindo.</p>
      </div>

      <!-- Banner de erro -->
      <Transition name="slide-down">
        <div v-if="loginError" class="login-error" role="alert">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
            <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.5"/>
            <path d="M8 5v3.5M8 10.5v.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <span>Usuário ou senha incorretos. Verifique e tente novamente.</span>
        </div>
      </Transition>

      <!-- Formulário -->
      <form @submit.prevent="handleLogin" class="login-fields" novalidate>

        <div class="field-group">
          <label for="login-user" class="field-lbl">Usuário ou e-mail</label>
          <div class="field-wrap" :class="{ 'field-wrap--error': loginError }">
            <input
              id="login-user"
              v-model="username"
              type="text"
              class="field-inp"
              placeholder="seu.usuario"
              required
              autocomplete="username"
              @input="loginError = false"
            />
          </div>
        </div>

        <div class="field-group">
          <div class="field-row">
            <label for="login-pass" class="field-lbl">Senha</label>
            <a href="#" class="field-forgot" tabindex="-1">Esqueceu a senha?</a>
          </div>
          <div class="field-wrap" :class="{ 'field-wrap--error': loginError }">
            <input
              id="login-pass"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              class="field-inp"
              placeholder="••••••••"
              required
              autocomplete="current-password"
              @input="loginError = false"
            />
            <button
              type="button"
              class="field-eye"
              :aria-label="showPassword ? 'Ocultar senha' : 'Mostrar senha'"
              @click="showPassword = !showPassword"
            >
              <svg v-if="!showPassword" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                <path d="M1 8s2.5-5 7-5 7 5 7 5-2.5 5-7 5-7-5-7-5z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
                <circle cx="8" cy="8" r="2" stroke="currentColor" stroke-width="1.4"/>
              </svg>
              <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
                <path d="M2 2l12 12M6.5 6.6A2 2 0 0 0 9.4 9.5M4.2 4.3C2.8 5.3 2 7 2 7s2.5 4 6 4.5M10.5 11A7 7 0 0 0 14 8s-2.5-5-6-5c-.9 0-1.8.2-2.6.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
        </div>

        <button type="submit" class="login-btn" :disabled="isLoading || !username || !password">
          <span v-if="!isLoading" class="login-btn-content">
            Acessar Plataforma
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          <span v-else class="login-btn-content">
            <span class="login-spinner" aria-hidden="true" />
            Autenticando...
          </span>
        </button>
      </form>

      <!-- Rodapé do form -->
      <p class="login-footer">
        Ainda não tem acesso?
        <router-link to="/register" class="login-footer-link">Criar conta gratuita</router-link>
      </p>

    </div>
  </AuthLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'
import AuthLayout from '../layouts/AuthLayout.vue'

const router       = useRouter()
const username     = ref('')
const password     = ref('')
const loginError   = ref(false)
const isLoading    = ref(false)
const showPassword = ref(false)

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
.login-form-wrapper {
  width: 100%;
  max-width: 400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-6);
}

/* ── Header ── */
.login-header {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.login-label {
  display: inline-flex;
  align-items: center;
  padding: 3px var(--space-3);
  border-radius: var(--radius-full);
  background: var(--color-orbit-dim);
  border: 1px solid var(--color-orbit-border);
  color: var(--color-orbit);
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  letter-spacing: var(--tracking-wider);
  text-transform: uppercase;
  width: fit-content;
}

.login-title {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  letter-spacing: var(--tracking-tight);
  line-height: var(--leading-tight);
  margin: 0;
}

.login-subtitle {
  font-size: var(--text-sm);
  color: var(--color-comet);
  margin: 0;
}

/* ── Error banner ── */
.login-error {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2);
  background: var(--color-nova-dim);
  border: 1px solid var(--color-nova-border);
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-4);
  color: var(--color-nova);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
}

/* ── Fields ── */
.login-fields {
  display: flex;
  flex-direction: column;
  gap: var(--space-5);
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-1-5);
}

.field-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.field-lbl {
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  color: var(--color-comet);
}

.field-forgot {
  font-size: var(--text-sm);
  color: var(--color-orbit);
  text-decoration: none;
  font-weight: var(--weight-medium);
  transition: color var(--duration-fast) var(--ease-out);
}
.field-forgot:hover { color: var(--color-orbit-bright); }

.field-wrap {
  display: flex;
  align-items: center;
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--input-radius);
  transition:
    border-color var(--duration-fast) var(--ease-out),
    box-shadow var(--duration-normal) var(--ease-out);
}
.field-wrap:focus-within {
  border-color: var(--color-orbit);
  box-shadow: var(--shadow-focus);
}
.field-wrap--error {
  border-color: var(--color-nova);
}

.field-inp {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  padding: var(--space-2-5) var(--space-3);
  color: var(--color-star);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  min-width: 0;
}
.field-inp::placeholder { color: var(--color-dust); }

.field-eye {
  padding: var(--space-2);
  color: var(--color-dust);
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  border-radius: var(--radius-sm);
  transition: color var(--duration-fast) var(--ease-out);
  flex-shrink: 0;
  margin-right: var(--space-1);
}
.field-eye:hover { color: var(--color-comet); }

/* ── Submit button ── */
.login-btn {
  width: 100%;
  min-height: 48px;
  background: var(--color-orbit);
  color: var(--color-cosmos);
  border: none;
  border-radius: var(--radius-md);
  font-family: var(--font-display);
  font-weight: var(--weight-bold);
  font-size: var(--text-sm);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  cursor: pointer;
  box-shadow: var(--shadow-orbit);
  transition:
    transform var(--duration-fast) var(--ease-spring),
    box-shadow var(--duration-normal) var(--ease-out),
    opacity var(--duration-fast) var(--ease-out);
}
.login-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-orbit), 0 8px 24px rgba(0, 229, 255, 0.2);
}
.login-btn:active:not(:disabled) {
  transform: scale(0.98);
  box-shadow: none;
}
.login-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}
.login-btn:focus-visible {
  outline: none;
  box-shadow: var(--shadow-focus);
}

.login-btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
}

.login-spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(8, 9, 26, 0.3);
  border-top-color: var(--color-cosmos);
  border-radius: 50%;
  animation: spinnerRing 0.6s linear infinite;
}

/* ── Footer ── */
.login-footer {
  text-align: center;
  font-size: var(--text-sm);
  color: var(--color-comet);
}

.login-footer-link {
  color: var(--color-orbit);
  font-weight: var(--weight-semibold);
  margin-left: var(--space-1);
  text-decoration: none;
  transition: color var(--duration-fast) var(--ease-out);
}
.login-footer-link:hover { color: var(--color-orbit-bright); text-decoration: underline; }

/* ── Transition ── */
.slide-down-enter-active { transition: all var(--duration-normal) var(--ease-in-out); }
.slide-down-leave-active { transition: all var(--duration-fast) var(--ease-in-out); }
.slide-down-enter-from   { opacity: 0; transform: translateY(-10px); }
.slide-down-leave-to     { opacity: 0; transform: translateY(-5px); }
</style>

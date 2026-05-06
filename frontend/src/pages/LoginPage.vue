<template>
  <AuthLayout>
    <div class="login-box">

      <!-- Cabeçalho do formulário -->
      <div class="form-header">
        <div class="form-badge">Plataforma de Simulados</div>
        <h2 class="form-title">Bem-vindo de volta</h2>
        <p class="form-sub">Acesse seu painel e continue evoluindo.</p>
      </div>

      <!-- Banner de erro -->
      <Transition name="slide-down">
        <div v-if="loginError" class="error-banner" role="alert">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" class="error-icon">
            <circle cx="8" cy="8" r="7" stroke="#b91c1c" stroke-width="1.5"/>
            <path d="M8 5v3.5M8 10.5v.5" stroke="#b91c1c" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <span>Usuário ou senha incorretos. Verifique e tente novamente.</span>
        </div>
      </Transition>

      <!-- Formulário -->
      <form @submit.prevent="handleLogin" class="form-fields" novalidate>
        <div class="field-group">
          <label for="login-user" class="field-label">Usuário ou e-mail</label>
          <input
            id="login-user"
            v-model="username"
            type="text"
            class="field-input"
            :class="{ 'field-input--error': loginError }"
            placeholder="seu.usuario"
            required
            autocomplete="username"
            @input="loginError = false"
          />
        </div>

        <div class="field-group">
          <div class="field-label-row">
            <label for="login-pass" class="field-label">Senha</label>
            <a href="#" class="forgot-link" tabindex="-1">Esqueceu a senha?</a>
          </div>
          <div class="password-wrap">
            <input
              id="login-pass"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              class="field-input"
              :class="{ 'field-input--error': loginError }"
              placeholder="••••••••"
              required
              autocomplete="current-password"
              @input="loginError = false"
            />
            <button type="button" class="eye-btn" @click="showPassword = !showPassword" tabindex="-1" :aria-label="showPassword ? 'Ocultar senha' : 'Mostrar senha'">
              <svg v-if="!showPassword" width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M1 8s2.5-5 7-5 7 5 7 5-2.5 5-7 5-7-5-7-5z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
                <circle cx="8" cy="8" r="2" stroke="currentColor" stroke-width="1.4"/>
              </svg>
              <svg v-else width="16" height="16" viewBox="0 0 16 16" fill="none">
                <path d="M2 2l12 12M6.5 6.6A2 2 0 0 0 9.4 9.5M4.2 4.3C2.8 5.3 2 7 2 7s2.5 4 6 4.5M10.5 11A7 7 0 0 0 14 8s-2.5-5-6-5c-.9 0-1.8.2-2.6.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
              </svg>
            </button>
          </div>
        </div>

        <button
          type="submit"
          class="submit-btn"
          :class="{ 'submit-btn--loading': isLoading }"
          :disabled="isLoading || !username || !password"
        >
          <span v-if="!isLoading" class="submit-label">
            Acessar Plataforma
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          <span v-else class="submit-loading">
            <span class="spinner" />
            Autenticando...
          </span>
        </button>
      </form>

      <!-- Rodapé do form -->
      <p class="form-switch">
        Ainda não tem acesso?
        <router-link to="/register" class="switch-link">Criar conta gratuita</router-link>
      </p>

    </div>
  </AuthLayout>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'
import AuthLayout from '../layouts/AuthLayout.vue'

const router     = useRouter()
const username   = ref('')
const password   = ref('')
const loginError = ref(false)
const isLoading  = ref(false)
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
.login-box {
  width: 100%;
  max-width: 400px;
}

/* ── Cabeçalho ── */
.form-header {
  margin-bottom: 32px;
}

.form-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 999px;
  background: #eff6ff;
  color: #1d4ed8;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 14px;
}

.form-title {
  font-family: var(--font-display);
  font-size: 1.75rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.025em;
  line-height: 1.2;
  margin-bottom: 6px;
}

.form-sub {
  font-size: 0.9375rem;
  color: #64748b;
  line-height: 1.5;
}

/* ── Error banner ── */
.error-banner {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  background: #fef2f2;
  border: 1px solid #fecaca;
  border-radius: 10px;
  padding: 12px 14px;
  color: #b91c1c;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 20px;
}
.error-icon { flex-shrink: 0; margin-top: 1px; }

/* slide-down transition */
.slide-down-enter-active { transition: all 0.2s ease; }
.slide-down-leave-active { transition: all 0.15s ease; }
.slide-down-enter-from   { opacity: 0; transform: translateY(-8px); }
.slide-down-leave-to     { opacity: 0; transform: translateY(-4px); }

/* ── Formulário ── */
.form-fields {
  display: flex;
  flex-direction: column;
  gap: 18px;
  margin-bottom: 24px;
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.field-label {
  font-size: 0.8125rem;
  font-weight: 500;
  color: #374151;
}

.field-label-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.forgot-link {
  font-size: 0.8125rem;
  color: #2563eb;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.12s ease;
}
.forgot-link:hover { color: #1d4ed8; text-decoration: underline; }

/* Input nativo — visual Stripe/Clerk */
.field-input {
  width: 100%;
  padding: 10px 14px;
  background: #ffffff;
  border: 1.5px solid #e2e8f0;
  border-radius: 10px;
  font-family: var(--font-body);
  font-size: 0.9375rem;
  color: #0f172a;
  outline: none;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
  -webkit-appearance: none;
}
.field-input::placeholder { color: #94a3b8; }
.field-input:hover:not(:focus) { border-color: #cbd5e1; }
.field-input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.14);
}
.field-input--error {
  border-color: #fca5a5;
  background: #fffafa;
}
.field-input--error:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.12);
}

/* Password wrapper */
.password-wrap {
  position: relative;
}
.password-wrap .field-input {
  padding-right: 44px;
}
.eye-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: #94a3b8;
  display: flex;
  align-items: center;
  padding: 4px;
  border-radius: 4px;
  transition: color 0.12s ease;
}
.eye-btn:hover { color: #475569; }

/* ── Botão primário ── */
.submit-btn {
  width: 100%;
  padding: 11px 20px;
  background: #2563eb;
  color: #ffffff;
  font-family: var(--font-body);
  font-weight: 600;
  font-size: 0.9375rem;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.15s ease, box-shadow 0.15s ease, transform 0.12s ease;
  box-shadow: 0 1px 3px rgba(37, 99, 235, 0.4), 0 1px 2px rgba(0, 0, 0, 0.06);
  min-height: 44px;
}
.submit-btn:hover:not(:disabled) {
  background: #1d4ed8;
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
  transform: translateY(-1px);
}
.submit-btn:active:not(:disabled) {
  transform: translateY(0) scale(0.99);
}
.submit-btn:disabled {
  opacity: 0.55;
  cursor: not-allowed;
}

.submit-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.submit-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  font-size: 0.875rem;
  opacity: 0.9;
}

.spinner {
  width: 15px;
  height: 15px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-top-color: #ffffff;
  border-radius: 50%;
  animation: spin 0.65s linear infinite;
  flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Link de cadastro ── */
.form-switch {
  text-align: center;
  font-size: 0.875rem;
  color: #64748b;
}
.switch-link {
  color: #2563eb;
  font-weight: 600;
  text-decoration: none;
  margin-left: 4px;
  transition: color 0.12s ease;
}
.switch-link:hover { color: #1d4ed8; text-decoration: underline; }
</style>

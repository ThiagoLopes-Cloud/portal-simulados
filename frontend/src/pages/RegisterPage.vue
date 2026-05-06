<template>
  <AuthLayout>
    <div class="register-box">

      <!-- Cabeçalho -->
      <div class="form-header">
        <div class="form-badge">Acesso Gratuito</div>
        <h2 class="form-title">Crie sua conta</h2>
        <p class="form-sub">Junte-se a mais de 3.200 alunos em preparação para concursos.</p>
      </div>

      <!-- Banners de feedback -->
      <Transition name="slide-down">
        <div v-if="erro" class="alert alert--error" role="alert">
          <svg width="15" height="15" viewBox="0 0 16 16" fill="none" class="alert-icon">
            <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.5"/>
            <path d="M8 5v3.5M8 10.5v.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          {{ erro }}
        </div>
      </Transition>

      <Transition name="slide-down">
        <div v-if="sucesso" class="alert alert--success" role="status">
          <svg width="15" height="15" viewBox="0 0 16 16" fill="none" class="alert-icon">
            <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.5"/>
            <path d="M5 8.5l2 2 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Conta criada com sucesso! Redirecionando para o login...
        </div>
      </Transition>

      <!-- Formulário -->
      <form @submit.prevent="register" class="form-fields" novalidate>
        <div class="field-group">
          <label for="reg-username" class="field-label">Nome de usuário</label>
          <input
            id="reg-username"
            v-model="username"
            type="text"
            class="field-input"
            placeholder="ex: joao.silva"
            required
            autocomplete="username"
            :disabled="carregando || sucesso"
            @input="erro = ''"
          />
          <span class="field-hint">Letras minúsculas, números e pontos.</span>
        </div>

        <div class="field-group">
          <label for="reg-email" class="field-label">E-mail</label>
          <input
            id="reg-email"
            v-model="email"
            type="email"
            class="field-input"
            placeholder="seu@email.com"
            required
            autocomplete="email"
            :disabled="carregando || sucesso"
            @input="erro = ''"
          />
        </div>

        <div class="password-row">
          <div class="field-group">
            <label for="reg-pass" class="field-label">Senha</label>
            <div class="password-wrap">
              <input
                id="reg-pass"
                v-model="password"
                :type="showPass ? 'text' : 'password'"
                class="field-input"
                placeholder="Mínimo 8 caracteres"
                required
                autocomplete="new-password"
                :disabled="carregando || sucesso"
                @input="erro = ''"
              />
              <button type="button" class="eye-btn" @click="showPass = !showPass" tabindex="-1">
                <svg v-if="!showPass" width="15" height="15" viewBox="0 0 16 16" fill="none">
                  <path d="M1 8s2.5-5 7-5 7 5 7 5-2.5 5-7 5-7-5-7-5z" stroke="currentColor" stroke-width="1.4" stroke-linejoin="round"/>
                  <circle cx="8" cy="8" r="2" stroke="currentColor" stroke-width="1.4"/>
                </svg>
                <svg v-else width="15" height="15" viewBox="0 0 16 16" fill="none">
                  <path d="M2 2l12 12M6.5 6.6A2 2 0 0 0 9.4 9.5M4.2 4.3C2.8 5.3 2 7 2 7s2.5 4 6 4.5M10.5 11A7 7 0 0 0 14 8s-2.5-5-6-5c-.9 0-1.8.2-2.6.5" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>
                </svg>
              </button>
            </div>
          </div>

          <div class="field-group">
            <label for="reg-pass2" class="field-label">Confirmar</label>
            <input
              id="reg-pass2"
              v-model="password2"
              :type="showPass ? 'text' : 'password'"
              class="field-input"
              :class="{ 'field-input--mismatch': password2 && password !== password2 }"
              placeholder="Repita a senha"
              required
              autocomplete="new-password"
              :disabled="carregando || sucesso"
              @input="erro = ''"
            />
          </div>
        </div>

        <!-- Barra de força da senha -->
        <div v-if="password" class="strength-bar-wrap">
          <div class="strength-bar">
            <div class="strength-fill" :class="`strength--${passwordStrength.level}`" :style="{ width: passwordStrength.width }" />
          </div>
          <span class="strength-label" :class="`label--${passwordStrength.level}`">{{ passwordStrength.label }}</span>
        </div>

        <button
          type="submit"
          class="submit-btn"
          :class="{ 'submit-btn--loading': carregando }"
          :disabled="carregando || sucesso || !canSubmit"
        >
          <span v-if="!carregando" class="submit-label">
            Criar Conta
            <svg width="15" height="15" viewBox="0 0 16 16" fill="none">
              <path d="M8 2v12M2 8h12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </span>
          <span v-else class="submit-loading">
            <span class="spinner" />
            Criando sua conta...
          </span>
        </button>
      </form>

      <p class="form-switch">
        Já faz parte do laboratório?
        <router-link to="/login" class="switch-link">Fazer login</router-link>
      </p>

    </div>
  </AuthLayout>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api.js'
import AuthLayout from '../layouts/AuthLayout.vue'

const router    = useRouter()
const username  = ref('')
const email     = ref('')
const password  = ref('')
const password2 = ref('')
const erro      = ref('')
const sucesso   = ref(false)
const carregando = ref(false)
const showPass  = ref(false)

const canSubmit = computed(() =>
  username.value && email.value && password.value && password2.value
)

const passwordStrength = computed(() => {
  const p = password.value
  if (!p) return { level: 'none', width: '0%', label: '' }
  let score = 0
  if (p.length >= 8) score++
  if (p.length >= 12) score++
  if (/[A-Z]/.test(p)) score++
  if (/[0-9]/.test(p)) score++
  if (/[^A-Za-z0-9]/.test(p)) score++
  if (score <= 1) return { level: 'weak',   width: '25%',  label: 'Fraca' }
  if (score <= 2) return { level: 'fair',   width: '50%',  label: 'Razoável' }
  if (score <= 3) return { level: 'good',   width: '75%',  label: 'Boa' }
  return              { level: 'strong', width: '100%', label: 'Forte' }
})

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
.register-box {
  width: 100%;
  max-width: 420px;
}

/* ── Cabeçalho ── */
.form-header {
  margin-bottom: 28px;
}

.form-badge {
  display: inline-flex;
  align-items: center;
  padding: 4px 12px;
  border-radius: 999px;
  background: #f0fdf4;
  color: #166534;
  font-size: 0.7rem;
  font-weight: 700;
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 14px;
  border: 1px solid #bbf7d0;
}

.form-title {
  font-family: var(--font-display);
  font-size: 1.625rem;
  font-weight: 800;
  color: #0f172a;
  letter-spacing: -0.025em;
  line-height: 1.2;
  margin-bottom: 6px;
}

.form-sub {
  font-size: 0.9rem;
  color: #64748b;
  line-height: 1.5;
}

/* ── Alertas ── */
.alert {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 11px 14px;
  border-radius: 10px;
  font-size: 0.875rem;
  font-weight: 500;
  margin-bottom: 18px;
}
.alert-icon { flex-shrink: 0; margin-top: 1px; }
.alert--error   { background: #fef2f2; border: 1px solid #fecaca; color: #b91c1c; }
.alert--success { background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; }

.slide-down-enter-active { transition: all 0.2s ease; }
.slide-down-leave-active { transition: all 0.15s ease; }
.slide-down-enter-from   { opacity: 0; transform: translateY(-8px); }
.slide-down-leave-to     { opacity: 0; transform: translateY(-4px); }

/* ── Formulário ── */
.form-fields {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 22px;
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

.field-hint {
  font-size: 0.75rem;
  color: #94a3b8;
}

/* Linha de senhas lado a lado */
.password-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

/* Input */
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
.field-input:hover:not(:focus):not(:disabled) { border-color: #cbd5e1; }
.field-input:focus {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.14);
}
.field-input:disabled { opacity: 0.5; cursor: not-allowed; background: #f8fafc; }
.field-input--mismatch {
  border-color: #fca5a5;
}
.field-input--mismatch:focus {
  border-color: #ef4444;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.12);
}

/* Password wrapper */
.password-wrap { position: relative; }
.password-wrap .field-input { padding-right: 40px; }
.eye-btn {
  position: absolute;
  right: 10px;
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

/* ── Barra de força ── */
.strength-bar-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: -4px;
}
.strength-bar {
  flex: 1;
  height: 4px;
  background: #f1f5f9;
  border-radius: 999px;
  overflow: hidden;
}
.strength-fill {
  height: 100%;
  border-radius: 999px;
  transition: width 0.3s ease, background 0.3s ease;
}
.strength--weak   { background: #ef4444; }
.strength--fair   { background: #f59e0b; }
.strength--good   { background: #3b82f6; }
.strength--strong { background: #10b981; }

.strength-label {
  font-size: 0.7rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  flex-shrink: 0;
}
.label--weak   { color: #ef4444; }
.label--fair   { color: #f59e0b; }
.label--good   { color: #3b82f6; }
.label--strong { color: #10b981; }

/* ── Botão ── */
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

/* ── Link de login ── */
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

/* ── Mobile ── */
@media (max-width: 480px) {
  .password-row { grid-template-columns: 1fr; }
}
</style>

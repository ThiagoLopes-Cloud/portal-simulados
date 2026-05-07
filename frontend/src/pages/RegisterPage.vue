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
  margin-bottom: var(--space-7);
}

.form-badge {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  background: var(--color-stellar-dim);
  color: var(--color-stellar-bright);
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  letter-spacing: var(--tracking-wider);
  text-transform: uppercase;
  margin-bottom: var(--space-3-5);
  border: 1px solid var(--color-stellar-border);
}

.form-title {
  font-family: var(--font-display);
  font-size: var(--text-3xl);
  font-weight: var(--weight-extrabold);
  color: var(--color-star);
  letter-spacing: var(--tracking-tight);
  line-height: var(--leading-tight);
  margin-bottom: var(--space-1-5);
}

.form-sub {
  font-size: var(--text-sm);
  color: var(--color-comet);
  line-height: var(--leading-normal);
}

/* ── Alertas ── */
.alert {
  display: flex;
  align-items: flex-start;
  gap: var(--space-2-5);
  padding: var(--space-3) var(--space-3-5);
  border-radius: var(--radius-md);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  margin-bottom: var(--space-4-5, 18px);
}
.alert-icon { flex-shrink: 0; margin-top: 1px; }
.alert--error   { background: var(--color-nova-dim);    border: 1px solid var(--color-nova-border);    color: var(--color-nova); }
.alert--success { background: var(--color-stellar-dim); border: 1px solid var(--color-stellar-border); color: var(--color-stellar-bright); }

.slide-down-enter-active { transition: all var(--duration-normal) var(--ease-in-out); }
.slide-down-leave-active { transition: all var(--duration-fast) var(--ease-in-out); }
.slide-down-enter-from   { opacity: 0; transform: translateY(-8px); }
.slide-down-leave-to     { opacity: 0; transform: translateY(-4px); }

/* ── Formulário ── */
.form-fields {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.field-group {
  display: flex;
  flex-direction: column;
  gap: var(--space-1-5);
}

.field-label {
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  color: var(--color-comet);
}

.field-hint {
  font-size: var(--text-xs);
  color: var(--color-dust);
}

.password-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3);
}

/* Input */
.field-input {
  width: 100%;
  padding: var(--space-2-5) var(--space-3-5);
  background: var(--color-bg-surface);
  border: 1.5px solid var(--color-border);
  border-radius: var(--input-radius);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  color: var(--color-star);
  outline: none;
  transition:
    border-color var(--duration-fast) var(--ease-out),
    box-shadow var(--duration-fast) var(--ease-out);
  -webkit-appearance: none;
}
.field-input::placeholder { color: var(--color-dust); }
.field-input:hover:not(:focus):not(:disabled) { border-color: var(--color-comet); }
.field-input:focus {
  border-color: var(--color-orbit);
  box-shadow: var(--shadow-focus);
}
.field-input:disabled { opacity: 0.45; cursor: not-allowed; background: var(--color-bg-elevated); }
.field-input--mismatch { border-color: var(--color-nova); }
.field-input--mismatch:focus {
  border-color: var(--color-nova);
  box-shadow: 0 0 0 3px rgba(255, 69, 96, 0.2);
}

/* Password wrapper */
.password-wrap { position: relative; }
.password-wrap .field-input { padding-right: 40px; }
.eye-btn {
  position: absolute;
  right: var(--space-2-5);
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-dust);
  display: flex;
  align-items: center;
  padding: var(--space-1);
  border-radius: var(--radius-sm);
  transition: color var(--duration-fast) var(--ease-out);
}
.eye-btn:hover { color: var(--color-comet); }

/* ── Barra de força ── */
.strength-bar-wrap {
  display: flex;
  align-items: center;
  gap: var(--space-2-5);
  margin-top: -4px;
}
.strength-bar {
  flex: 1;
  height: 4px;
  background: var(--color-bg-elevated);
  border-radius: var(--radius-full);
  overflow: hidden;
}
.strength-fill {
  height: 100%;
  border-radius: var(--radius-full);
  transition: width var(--duration-normal) var(--ease-out), background var(--duration-normal) var(--ease-out);
}
.strength--weak   { background: var(--color-nova); }
.strength--fair   { background: var(--color-flare); }
.strength--good   { background: var(--color-orbit); }
.strength--strong { background: var(--color-stellar); }

.strength-label {
  font-size: var(--text-2xs);
  font-weight: var(--weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  flex-shrink: 0;
}
.label--weak   { color: var(--color-nova); }
.label--fair   { color: var(--color-flare); }
.label--good   { color: var(--color-orbit); }
.label--strong { color: var(--color-stellar); }

/* ── Botão ── */
.submit-btn {
  width: 100%;
  padding: var(--space-3) var(--space-5);
  background: var(--color-orbit);
  color: var(--color-cosmos);
  font-family: var(--font-display);
  font-weight: var(--weight-bold);
  font-size: var(--text-sm);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition:
    transform var(--duration-fast) var(--ease-spring),
    box-shadow var(--duration-normal) var(--ease-out),
    opacity var(--duration-fast) var(--ease-out);
  box-shadow: var(--shadow-orbit);
  min-height: var(--btn-height-md);
}
.submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: var(--shadow-orbit), 0 8px 24px rgba(0, 229, 255, 0.2);
}
.submit-btn:active:not(:disabled) {
  transform: scale(0.98);
  box-shadow: none;
}
.submit-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}
.submit-btn:focus-visible {
  outline: none;
  box-shadow: var(--shadow-focus);
}

.submit-label {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
}
.submit-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2-5);
  font-size: var(--text-sm);
  opacity: 0.9;
}

.spinner {
  width: 15px;
  height: 15px;
  border: 2px solid rgba(8, 9, 26, 0.3);
  border-top-color: var(--color-cosmos);
  border-radius: 50%;
  animation: spin 0.65s linear infinite;
  flex-shrink: 0;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* ── Link de login ── */
.form-switch {
  text-align: center;
  font-size: var(--text-sm);
  color: var(--color-comet);
}
.switch-link {
  color: var(--color-orbit);
  font-weight: var(--weight-semibold);
  text-decoration: none;
  margin-left: var(--space-1);
  transition: color var(--duration-fast) var(--ease-out);
}
.switch-link:hover { color: var(--color-orbit-bright); text-decoration: underline; }

/* ── Mobile ── */
@media (max-width: 480px) {
  .password-row { grid-template-columns: 1fr; }
}
</style>

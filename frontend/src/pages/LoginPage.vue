<template>
  <AuthLayout>
    <div class="w-full max-w-[400px] mx-auto">

      <!-- Cabeçalho do formulário -->
      <div class="mb-8">
        <div class="inline-flex items-center px-3 py-1 rounded-full bg-simus-cyan/10 text-simus-cyan text-xs font-bold tracking-widest uppercase mb-4">
          Plataforma de Simulados
        </div>
        <h2 class="font-display text-3xl font-bold text-white tracking-tight leading-tight mb-2">
          Bem-vindo de volta
        </h2>
        <p class="text-sm text-slate-400">
          Acesse seu painel e continue evoluindo.
        </p>
      </div>

      <!-- Banner de erro -->
      <Transition name="slide-down">
        <div v-if="loginError" class="flex items-start gap-3 bg-red-500/10 border border-red-500/20 rounded-lg p-3 text-red-400 text-sm font-medium mb-6" role="alert">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="none" class="flex-shrink-0 mt-[2px]">
            <circle cx="8" cy="8" r="7" stroke="currentColor" stroke-width="1.5"/>
            <path d="M8 5v3.5M8 10.5v.5" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
          </svg>
          <span>Usuário ou senha incorretos. Verifique e tente novamente.</span>
        </div>
      </Transition>

      <!-- Formulário -->
      <form @submit.prevent="handleLogin" class="flex flex-col gap-5 mb-6" novalidate>
        
        <div class="flex flex-col gap-1.5">
          <label for="login-user" class="text-sm font-medium text-slate-300">Usuário ou e-mail</label>
          <input
            id="login-user"
            v-model="username"
            type="text"
            class="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-lg font-body text-white placeholder:text-slate-500 focus:outline-none focus:border-simus-cyan focus:ring-1 focus:ring-simus-cyan focus:bg-white/10 transition-all"
            :class="{ 'border-red-500/50 focus:border-red-500 focus:ring-red-500': loginError }"
            placeholder="seu.usuario"
            required
            autocomplete="username"
            @input="loginError = false"
          />
        </div>

        <div class="flex flex-col gap-1.5">
          <div class="flex items-center justify-between">
            <label for="login-pass" class="text-sm font-medium text-slate-300">Senha</label>
            <a href="#" class="text-sm text-simus-cyan font-medium hover:text-cyan-300 hover:underline transition-colors" tabindex="-1">
              Esqueceu a senha?
            </a>
          </div>
          <div class="relative">
            <input
              id="login-pass"
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              class="w-full px-4 py-2.5 bg-white/5 border border-white/10 rounded-lg font-body text-white placeholder:text-slate-500 pr-11 focus:outline-none focus:border-simus-cyan focus:ring-1 focus:ring-simus-cyan focus:bg-white/10 transition-all"
              :class="{ 'border-red-500/50 focus:border-red-500 focus:ring-red-500': loginError }"
              placeholder="••••••••"
              required
              autocomplete="current-password"
              @input="loginError = false"
            />
            <button type="button" class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white transition-colors p-1" @click="showPassword = !showPassword" tabindex="-1" :aria-label="showPassword ? 'Ocultar senha' : 'Mostrar senha'">
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
          class="w-full mt-2 py-3 bg-simus-cyan text-simus-bg font-display font-bold text-sm uppercase tracking-wider rounded-lg shadow-[0_0_15px_rgba(0,229,255,0.3)] hover:scale-[1.02] transition-all disabled:opacity-50 disabled:hover:scale-100 disabled:cursor-not-allowed flex items-center justify-center min-h-[48px]"
          :disabled="isLoading || !username || !password"
        >
          <span v-if="!isLoading" class="flex items-center gap-2">
            Acessar Plataforma
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </span>
          <span v-else class="flex items-center gap-2 opacity-90">
            <span class="w-4 h-4 border-2 border-simus-bg/30 border-t-simus-bg rounded-full animate-spin flex-shrink-0" />
            Autenticando...
          </span>
        </button>
      </form>

      <!-- Rodapé do form -->
      <p class="text-center text-sm text-slate-400">
        Ainda não tem acesso?
        <router-link to="/register" class="text-simus-cyan font-semibold ml-1 hover:underline transition-colors">
          Criar conta gratuita
        </router-link>
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
/* Removemos quase todo o CSS pois agora o Tailwind gerencia tudo! */
/* Mantemos apenas a animação da notificação de erro, que o Vue Transition precisa */
.slide-down-enter-active { transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1); }
.slide-down-leave-active { transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1); }
.slide-down-enter-from   { opacity: 0; transform: translateY(-10px); }
.slide-down-leave-to     { opacity: 0; transform: translateY(-5px); }
</style>
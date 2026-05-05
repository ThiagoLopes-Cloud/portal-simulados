<template>
  <div class="min-h-screen w-full flex bg-simus-bg font-body">

    <!-- ── Lado do formulário ─────────────────────────────────── -->
    <div class="flex-1 flex items-center justify-center px-6 py-12">
      <div class="w-full max-w-sm">

        <!-- Logo -->
        <div class="mb-10">
          <h1 class="font-display text-3xl font-bold tracking-tight">
            <span class="text-simus-cyan">SIMUS</span><span class="text-slate-50">LAB</span>
          </h1>
          <p class="text-slate-500 text-sm mt-1">by Metamorfose</p>
        </div>

        <!-- Boas-vindas -->
        <div class="mb-8">
          <h2 class="font-display text-2xl font-semibold text-slate-50 mb-2">
            Bem-vindo de volta
          </h2>
          <p class="text-slate-400 text-sm leading-relaxed">
            Acesse seu painel de performance e continue sua evolução.
          </p>
        </div>

        <!-- Erro -->
        <div v-if="loginError"
             class="mb-6 flex items-center gap-3 bg-red-500/10 border border-red-500/30 rounded-xl px-4 py-3">
          <span class="text-red-400 text-sm">
            Credenciais inválidas. Verifique seus dados e tente novamente.
          </span>
        </div>

        <!-- Formulário -->
        <form @submit.prevent="handleLogin" class="space-y-5">

          <div class="space-y-1.5">
            <label for="username" class="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
              Usuário ou E-mail
            </label>
            <input
              type="text"
              id="username"
              v-model="username"
              @input="loginError = false"
              placeholder="Digite seu usuário"
              required
              class="simus-input"
            />
          </div>

          <div class="space-y-1.5">
            <label for="password" class="block text-xs font-semibold text-slate-400 uppercase tracking-wider">
              Senha
            </label>
            <input
              type="password"
              id="password"
              v-model="password"
              @input="loginError = false"
              placeholder="••••••••"
              required
              class="simus-input"
            />
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full mt-2 inline-flex items-center justify-center gap-2.5
                   px-6 py-3.5 rounded-xl
                   font-display font-semibold text-sm uppercase tracking-widest
                   bg-simus-cyan text-simus-bg
                   transition-all duration-200 ease-out
                   hover:scale-[1.02] hover:shadow-[0_0_22px_rgba(0,229,255,0.35)]
                   disabled:opacity-50 disabled:pointer-events-none"
          >
            <span v-if="isLoading"
                  class="w-4 h-4 border-2 border-simus-bg/30 border-t-simus-bg rounded-full animate-spin" />
            {{ isLoading ? 'Autenticando...' : 'Acessar Plataforma' }}
          </button>

        </form>

        <p class="mt-8 text-center text-sm text-slate-500">
          Ainda não tem conta?
          <router-link to="/register"
                       class="text-simus-cyan font-semibold hover:underline ml-1">
            Cadastre-se
          </router-link>
        </p>

      </div>
    </div>

    <!-- ── Lado da marca (oculto em mobile) ──────────────────── -->
    <div class="hidden lg:flex flex-[1.2] relative items-center justify-center px-16 overflow-hidden
                border-l border-white/5">

      <!-- Glows decorativos de fundo -->
      <div class="absolute top-1/4 right-1/3 w-96 h-96 bg-simus-cyan/[0.04] rounded-full blur-3xl pointer-events-none" />
      <div class="absolute bottom-1/3 left-1/4 w-72 h-72 bg-simus-purple/[0.06] rounded-full blur-3xl pointer-events-none" />

      <div class="relative z-10 max-w-lg">

        <!-- Badge -->
        <span class="inline-flex items-center gap-2 px-4 py-1.5 mb-8 rounded-full
                     bg-simus-cyan/10 border border-simus-cyan/20
                     text-simus-cyan text-xs font-display font-semibold uppercase tracking-widest">
          <span class="w-1.5 h-1.5 rounded-full bg-simus-cyan animate-pulse" />
          Plataforma de Alta Performance
        </span>

        <h2 class="font-display text-5xl font-bold leading-[1.1] text-slate-50 tracking-tight mb-6">
          O futuro da sua aprovação começa aqui.
        </h2>

        <p class="text-slate-400 text-lg leading-relaxed mb-12">
          Utilize dados precisos e simulações realistas para mapear seus pontos cegos,
          otimizar seu tempo e garantir sua vaga.
        </p>

        <!-- Gráfico abstrato de barras -->
        <div class="flex items-end gap-3 h-24">
          <div class="w-9 bg-white/[0.07] rounded-t-md" style="height:30%" />
          <div class="w-9 bg-white/[0.07] rounded-t-md" style="height:52%" />
          <div class="w-9 bg-white/[0.07] rounded-t-md" style="height:73%" />
          <div class="w-9 h-full rounded-t-md bg-simus-cyan shadow-[0_0_20px_rgba(0,229,255,0.4)]" />
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
const password = ref('')
const loginError = ref(false)
const isLoading = ref(false)

async function handleLogin() {
  loginError.value = false
  isLoading.value = true

  try {
    const response = await api.post('/api/login/', {
      username: username.value,
      password: password.value
    })

    localStorage.setItem('access_token', response.data.access)
    if (response.data.refresh) {
      localStorage.setItem('refresh_token', response.data.refresh)
    }

    const userRole = response.data.role || 'student'
    localStorage.setItem('user_role', userRole)

    router.push({ name: 'dashboard' }).then(() => {
      window.location.reload()
    })

  } catch (error) {
    console.error("Erro na autenticação:", error)
    loginError.value = true
  } finally {
    isLoading.value = false
  }
}
</script>

<style scoped>
@reference "../assets/main.css";

.simus-input {
  @apply w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3.5
         text-slate-50 placeholder:text-slate-600 text-sm
         transition-all duration-150 outline-none;
}

.simus-input:focus {
  @apply border-simus-cyan bg-simus-cyan/5;
  box-shadow: 0 0 0 3px rgba(0, 229, 255, 0.1);
}
</style>

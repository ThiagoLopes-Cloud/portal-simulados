<template>
  <div class="min-h-screen w-full flex bg-simus-bg font-body">

    <!-- ── Lado do formulário ─────────────────────────────────── -->
    <div class="flex-1 flex items-center justify-center px-6 py-12">
      <div class="w-full max-w-sm">

        <div class="mb-8">
          <h1 class="font-display text-3xl font-bold tracking-tight">
            <span class="text-simus-cyan">SIMUS</span><span class="text-slate-50">LAB</span>
          </h1>
          <p class="text-slate-500 text-sm mt-1">by Metamorfose</p>
        </div>

        <div class="mb-7">
          <h2 class="font-display text-2xl font-semibold text-slate-50 mb-2">Crie sua conta</h2>
          <p class="text-slate-400 text-sm leading-relaxed">Junte-se ao laboratório e inicie sua jornada de alta performance.</p>
        </div>

        <div v-if="erro" class="mb-5 flex items-center gap-3 bg-red-500/10 border border-red-500/30 rounded-xl px-4 py-3">
          <span class="text-red-400 text-sm">{{ erro }}</span>
        </div>

        <div v-if="sucesso" class="mb-5 flex items-center gap-3 bg-emerald-500/10 border border-emerald-500/30 rounded-xl px-4 py-3">
          <span class="text-emerald-400 text-sm font-medium">Conta criada com sucesso! Preparando seu painel...</span>
        </div>

        <form @submit.prevent="register" class="space-y-4">

          <div class="space-y-1.5">
            <label for="username" class="block text-xs font-semibold text-slate-400 uppercase tracking-wider">Usuário</label>
            <input type="text" id="username" v-model="username" placeholder="Ex: joao.silva"
                   required :disabled="carregando || sucesso" class="simus-input" />
          </div>

          <div class="space-y-1.5">
            <label for="email" class="block text-xs font-semibold text-slate-400 uppercase tracking-wider">E-mail</label>
            <input type="email" id="email" v-model="email" placeholder="seu@email.com"
                   required :disabled="carregando || sucesso" class="simus-input" />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div class="space-y-1.5">
              <label for="password" class="block text-xs font-semibold text-slate-400 uppercase tracking-wider">Senha</label>
              <input type="password" id="password" v-model="password" placeholder="••••••••"
                     required :disabled="carregando || sucesso" class="simus-input" />
            </div>
            <div class="space-y-1.5">
              <label for="password2" class="block text-xs font-semibold text-slate-400 uppercase tracking-wider">Confirmar</label>
              <input type="password" id="password2" v-model="password2" placeholder="••••••••"
                     required :disabled="carregando || sucesso" class="simus-input" />
            </div>
          </div>

          <button type="submit" :disabled="carregando || sucesso"
                  class="w-full mt-1 inline-flex items-center justify-center gap-2.5
                         px-6 py-3.5 rounded-xl
                         font-display font-semibold text-sm uppercase tracking-widest
                         bg-simus-cyan text-simus-bg
                         transition-all duration-200 ease-out
                         hover:scale-[1.02] hover:shadow-[0_0_22px_rgba(0,229,255,0.35)]
                         disabled:opacity-50 disabled:pointer-events-none">
            <span v-if="carregando" class="w-4 h-4 border-2 border-simus-bg/30 border-t-simus-bg rounded-full animate-spin" />
            {{ carregando ? 'Processando dados...' : 'Criar Conta' }}
          </button>

        </form>

        <p class="mt-7 text-center text-sm text-slate-500">
          Já faz parte do laboratório?
          <router-link to="/login" class="text-simus-cyan font-semibold hover:underline ml-1">Faça login</router-link>
        </p>

      </div>
    </div>

    <!-- ── Lado da marca (oculto em mobile) ──────────────────── -->
    <div class="hidden lg:flex flex-[1.2] relative items-center justify-center px-16 overflow-hidden border-l border-white/5">
      <div class="absolute top-1/3 left-1/4 w-80 h-80 bg-simus-purple/[0.05] rounded-full blur-3xl pointer-events-none" />
      <div class="absolute bottom-1/4 right-1/3 w-96 h-96 bg-simus-cyan/[0.04] rounded-full blur-3xl pointer-events-none" />

      <div class="relative z-10 max-w-lg">
        <span class="inline-flex items-center gap-2 px-4 py-1.5 mb-8 rounded-full
                     bg-simus-purple/10 border border-simus-purple/20
                     text-simus-purple text-xs font-display font-semibold uppercase tracking-widest">
          <span class="w-1.5 h-1.5 rounded-full bg-simus-purple animate-pulse" />
          Acesso Restrito
        </span>

        <h2 class="font-display text-5xl font-bold leading-[1.1] text-slate-50 tracking-tight mb-6">
          Transforme esforço em estratégia.
        </h2>

        <p class="text-slate-400 text-lg leading-relaxed mb-12">
          Crie seu perfil para acessar simulações realistas, mapear seus pontos fracos e receber recomendações focadas na sua aprovação.
        </p>

        <div class="flex items-end gap-3 h-24">
          <div class="w-9 bg-white/[0.07] rounded-t-md" style="height:40%" />
          <div class="w-9 bg-white/[0.07] rounded-t-md" style="height:60%" />
          <div class="w-9 bg-white/[0.07] rounded-t-md" style="height:80%" />
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
      role: 'student',
    })

    sucesso.value = true

    setTimeout(() => {
      router.push({ name: 'login' })
    }, 2000)

  } catch (error) {
    if (error.response?.data) {
      const erros = error.response.data
      const primeiroErro = Object.values(erros)[0]
      erro.value = Array.isArray(primeiroErro) ? primeiroErro[0] : primeiroErro
    } else {
      erro.value = 'Erro ao criar conta. Tente novamente.'
    }
  } finally {
    carregando.value = false
  }
}
</script>

<style scoped>
@reference "../assets/main.css";

.simus-input {
  @apply w-full bg-white/5 border border-white/10 rounded-xl px-4 py-3
         text-slate-50 placeholder:text-slate-600 text-sm
         transition-all duration-150 outline-none
         disabled:opacity-40 disabled:cursor-not-allowed;
}
.simus-input:focus {
  @apply border-simus-cyan bg-simus-cyan/5;
  box-shadow: 0 0 0 3px rgba(0, 229, 255, 0.1);
}
</style>

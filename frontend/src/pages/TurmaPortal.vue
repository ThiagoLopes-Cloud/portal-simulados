<template>
  <div class="turma-portal container">
    <h2>🏫 Minhas Turmas no Metamorfose</h2>
    
    <div class="card-convite">
      <h3>Tens um código de convite?</h3>
      <div class="input-group">
        <input 
          v-model="codigoInput" 
          placeholder="Ex: A1B2C3D4" 
          maxlength="12"
        />
        <button @click="entrarNaTurma" :disabled="!codigoInput">
          Matricular-me
        </button>
      </div>
      <p v-if="mensagem" class="feedback-ok">{{ mensagem }}</p>
      <p v-if="erro" class="feedback-erro">{{ erro }}</p>
    </div>

    <div class="lista-turmas">
      <div v-for="t in turmas" :key="t.id" class="turma-item">
        <div class="turma-info">
          <strong>{{ t.nome }}</strong>
          <span>Professor: {{ t.professor_nome }}</span>
        </div>
        <span class="badge">Ativa</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const codigoInput = ref('')
const mensagem = ref('')
const erro = ref('')
const turmas = ref([])

async function entrarNaTurma() {
  try {
    const res = await api.post('/escolas/entrar/', { codigo: codigoInput.value })
    mensagem.value = res.data.message
    erro.value = ''
    codigoInput.value = ''
    carregarTurmas()
  } catch (e) {
    erro.value = e.response?.data?.error || 'Erro ao entrar na turma.'
    mensagem.value = ''
  }
}

async function carregarTurmas() {
  // Chamada para buscar turmas onde o aluno está matriculado
  const res = await api.get('/escolas/minhas-turmas/')
  turmas.value = res.data
}

onMounted(carregarTurmas)
</script>
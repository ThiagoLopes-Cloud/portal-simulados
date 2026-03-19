<template>
  <!-- Container principal da página de resultado -->
  <div class="resultado">

    <!-- Navbar superior -->
    <nav class="navbar">
      <h1>Portal de Simulados</h1>
    </nav>

    <!-- Container centralizado -->
    <div class="container">

      <!-- Ícone dinâmico — 🎉 se aprovado, 📚 se reprovado -->
      <div class="icone">
        {{ parseFloat(score) >= 70 ? '🎉' : '📚' }}
      </div>

      <!-- Título dinâmico baseado no score -->
      <h2>{{ parseFloat(score) >= 70 ? 'Parabéns!' : 'Continue praticando!' }}</h2>

      <!-- Subtítulo fixo -->
      <p class="subtitulo">Você concluiu o simulado!</p>

      <!-- Card com os dados do resultado -->
      <div class="card">

        <!-- Score principal em percentual -->
        <div class="score">
          <span class="score-valor">{{ score }}</span>
          <span class="score-label">de aproveitamento</span>
        </div>

        <!-- Linha divisória -->
        <div class="divisor"></div>

        <!-- Detalhes: acertos, erros e total -->
        <div class="detalhes">

          <!-- Acertos em verde -->
          <div class="detalhe">
            <span class="detalhe-valor verde">{{ acertos }}</span>
            <span class="detalhe-label">Acertos</span>
          </div>

          <!-- Erros em vermelho -->
          <div class="detalhe">
            <span class="detalhe-valor vermelho">{{ total - acertos }}</span>
            <span class="detalhe-label">Erros</span>
          </div>

          <!-- Total em azul -->
          <div class="detalhe">
            <span class="detalhe-valor azul">{{ total }}</span>
            <span class="detalhe-label">Total</span>
          </div>

        </div>

      </div>

      <!-- Botões de ação -->
      <div class="acoes">
        <button @click="$router.push('/simulados')" class="btn-secundario">
          Ver outros simulados
        </button>
        <button @click="$router.push('/ranking')" class="btn-primario">
          Ver ranking 🏆
        </button>
      </div>

    </div>
  </div>
</template>

<script setup>
// Importa useRoute para acessar os query params da URL
import { useRoute } from 'vue-router'

// useRoute permite acessar os parâmetros da URL atual
const route = useRoute()

// Extrai os dados do resultado dos query params
// Foram enviados pela ProvaPage após o envio das respostas
const acertos = parseInt(route.query.acertos) || 0
const total = parseInt(route.query.total) || 0
const score = route.query.score || '0.00%'
</script>

<style scoped>
.resultado {
  min-height: 100vh;
  background: #f5f5f5;
}

.navbar {
  background: #667eea;
  color: white;
  padding: 16px 32px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.navbar h1 { font-size: 20px; font-weight: 600; }

.container {
  max-width: 500px;
  margin: 0 auto;
  padding: 60px 20px;
  text-align: center;
}

.icone { font-size: 72px; margin-bottom: 16px; }

h2 { font-size: 28px; color: #333; margin-bottom: 8px; }

.subtitulo { color: #666; margin-bottom: 32px; }

.card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0,0,0,0.1);
  margin-bottom: 32px;
}

.score {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  margin-bottom: 24px;
}

.score-valor { font-size: 56px; font-weight: 700; color: #667eea; }
.score-label { font-size: 14px; color: #999; }

.divisor { height: 1px; background: #eee; margin-bottom: 24px; }

.detalhes { display: flex; justify-content: space-around; }

.detalhe {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.detalhe-valor { font-size: 32px; font-weight: 700; }
.detalhe-label { font-size: 13px; color: #999; }

.verde { color: #22c55e; }
.vermelho { color: #ef4444; }
.azul { color: #667eea; }

.acoes { display: flex; gap: 12px; justify-content: center; }

.btn-primario, .btn-secundario {
  padding: 12px 24px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  font-size: 15px;
  transition: background 0.2s;
}

.btn-primario { background: #667eea; color: white; }
.btn-primario:hover { background: #5a6fd6; }

.btn-secundario { background: #eee; color: #555; }
.btn-secundario:hover { background: #ddd; }
</style>
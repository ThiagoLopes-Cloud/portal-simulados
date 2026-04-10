<template>
  <div class="evolucao-container" v-if="evolucao && evolucao.length > 0">
    <h3>Sua Evolução Neste Simulado</h3>
    
    <div class="chart-wrapper">
      <div 
        v-for="(item, index) in evolucao" 
        :key="item.resultado_id" 
        class="bar-column"
      >
        <div class="bar-value">{{ item.score }}%</div>
        
        <div 
          class="bar" 
          :style="{ height: `${item.score}%` }"
          :class="getBarClass(index)"
        ></div>
        
        <div class="bar-label">T{{ item.tentativa }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
// O defineProps é nativo do <script setup> no Vue 3, então não precisa (e nem deve) ser importado.
const props = defineProps({
  evolucao: {
    type: Array,
    required: true,
    default: () => []
  }
});

// Lógica de cálculo visual: verde se melhorou, vermelho se piorou, azul se manteve ou é o primeiro
const getBarClass = (index) => {
  if (index === 0) return 'bar-neutral'; // Primeira tentativa
  
  const atual = props.evolucao[index].score;
  const anterior = props.evolucao[index - 1].score;
  
  if (atual > anterior) return 'bar-positive';
  if (atual < anterior) return 'bar-negative';
  return 'bar-neutral';
};
</script>

<style scoped>
.evolucao-container {
  margin-top: 2rem;
  padding: 1.5rem;
  background: #f8fafc; /* Fundo leve cinza-azulado */
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

h3 { 
  margin-bottom: 1.5rem; 
  color: #334155; 
  font-size: 1.25rem;
  font-weight: 600;
}

.chart-wrapper {
  display: flex;
  align-items: flex-end; /* Alinha as barras pela base */
  gap: 1.5rem;
  height: 180px; /* Altura fixa do gráfico */
  padding-bottom: 10px;
  border-bottom: 2px solid #cbd5e1;
  overflow-x: auto; /* Permite scroll se o aluno tiver dezenas de tentativas */
}

.bar-column {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
  min-width: 50px;
  max-width: 80px;
}

.bar-value {
  font-size: 0.85rem;
  font-weight: bold;
  margin-bottom: 6px;
  color: #475569;
}

.bar {
  width: 100%;
  border-radius: 4px 4px 0 0;
  transition: height 0.5s ease-in-out;
  min-height: 4px; /* Garante que scores 0% tenham representação visual */
}

.bar-label {
  margin-top: 8px;
  font-size: 0.9rem;
  font-weight: 600;
  color: #64748b;
}

/* Cores de status */
.bar-neutral { background-color: #3b82f6; } /* Azul - Base/Primeira tentativa */
.bar-positive { background-color: #22c55e; } /* Verde - Melhorou */
.bar-negative { background-color: #ef4444; } /* Vermelho - Piorou */
</style>
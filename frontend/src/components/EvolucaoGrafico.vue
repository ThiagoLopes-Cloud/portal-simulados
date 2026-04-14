<template>
  <div class="evolucao-container clean-card" v-if="evolucao && evolucao.length > 0">
    <div class="chart-header">
      <h3 class="chart-title">Curva de Aprendizado</h3>
      <p class="chart-subtitle">Sua evolução histórica de precisão nesta avaliação.</p>
    </div>
    
    <div class="canvas-wrapper">
      <Line v-if="chartDataVisivel" :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script setup>
import { computed, ref, onMounted, watch } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

// Registrando os módulos necessários do Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const props = defineProps({
  evolucao: {
    type: Array,
    required: true,
    default: () => []
  }
})

const chartDataVisivel = ref(false)

// Prepara os dados lendo exatamente as propriedades que você já usava
const chartData = computed(() => {
  // Se tiver a data usa a data, senão usa o formato "T1", "T2" (Tentativa)
  const labels = props.evolucao.map((item, index) => item.data || `T${item.tentativa || index + 1}`)
  const dataPoints = props.evolucao.map(item => parseFloat(item.score))

  return {
    labels: labels,
    datasets: [
      {
        label: 'Aproveitamento',
        data: dataPoints,
        borderColor: '#0052FF', // Azul Clean Tech
        backgroundColor: 'rgba(0, 82, 255, 0.1)', // Fundo translúcido abaixo da linha
        borderWidth: 3,
        pointBackgroundColor: '#FFFFFF',
        pointBorderColor: '#0052FF',
        pointBorderWidth: 2,
        pointRadius: 5,
        pointHoverRadius: 7,
        pointHoverBackgroundColor: '#0052FF',
        pointHoverBorderColor: '#FFFFFF',
        fill: true, 
        tension: 0.4 // Deixa a linha suavemente curvada (Premium)
      }
    ]
  }
})

// Configurações de design do gráfico
const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false // Escondemos a legenda padrão
    },
    tooltip: {
      backgroundColor: '#0F172A',
      titleFont: { size: 13, family: "'Inter', sans-serif" },
      bodyFont: { size: 14, weight: 'bold', family: "'Inter', sans-serif" },
      padding: 12,
      displayColors: false,
      callbacks: {
        label: function(context) {
          return `Score: ${context.parsed.y}%`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      grid: {
        color: '#F1F5F9',
        drawBorder: false,
      },
      ticks: {
        color: '#64748B',
        font: { family: "'Inter', sans-serif", size: 11, weight: '500' },
        stepSize: 20,
        callback: function(value) {
          return value + '%'
        }
      }
    },
    x: {
      grid: {
        display: false,
        drawBorder: false,
      },
      ticks: {
        color: '#64748B',
        font: { family: "'Inter', sans-serif", size: 11, weight: '600' },
      }
    }
  }
}

// Garante que o canvas só renderize após a montagem do componente
onMounted(() => {
  if (props.evolucao.length > 0) {
    setTimeout(() => { chartDataVisivel.value = true }, 100)
  }
})

// Se os dados atualizarem depois que a página carregou, ele re-renderiza
watch(() => props.evolucao, (newVal) => {
  if (newVal.length > 0) {
    chartDataVisivel.value = true
  }
}, { deep: true })
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

.evolucao-container {
  margin-bottom: 24px;
  font-family: 'Inter', sans-serif;
}

.clean-card {
  background: white;
  border: 1px solid #E2E8F0;
  border-radius: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.03);
  padding: 30px;
}

.chart-header {
  margin-bottom: 20px;
}

.chart-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: #0F172A;
  margin: 0 0 4px 0;
}

.chart-subtitle {
  color: #64748B;
  font-size: 0.95rem;
  margin: 0;
}

.canvas-wrapper {
  position: relative;
  height: 280px; /* Altura perfeita para visualização sem ocupar a tela toda */
  width: 100%;
}
</style>
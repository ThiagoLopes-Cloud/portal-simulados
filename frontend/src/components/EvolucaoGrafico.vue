<template>
  <div class="evolucao-container" v-if="evolucao && evolucao.length > 0">
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

// DS hex values for Chart.js (CSS vars not supported in Chart.js)
const DS = {
  orbit:      '#00E5FF',
  orbitFill:  'rgba(0, 229, 255, 0.08)',
  cosmos:     '#08091A',
  gridLine:   'rgba(255, 255, 255, 0.06)',
  tick:       'rgba(255, 255, 255, 0.35)',
  tooltipBg:  '#1A1D3D',
  font:       'DM Sans',
}

const chartData = computed(() => {
  const labels = props.evolucao.map((item, index) => item.data || `T${item.tentativa || index + 1}`)
  const dataPoints = props.evolucao.map(item => parseFloat(item.score))

  return {
    labels,
    datasets: [{
      label: 'Aproveitamento',
      data: dataPoints,
      borderColor: DS.orbit,
      backgroundColor: DS.orbitFill,
      borderWidth: 2.5,
      pointBackgroundColor: DS.cosmos,
      pointBorderColor: DS.orbit,
      pointBorderWidth: 2,
      pointRadius: 5,
      pointHoverRadius: 7,
      pointHoverBackgroundColor: DS.orbit,
      pointHoverBorderColor: DS.cosmos,
      fill: true,
      tension: 0.4,
    }],
  }
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      backgroundColor: DS.tooltipBg,
      titleFont: { size: 13, family: DS.font },
      bodyFont: { size: 14, weight: 'bold', family: DS.font },
      padding: 12,
      displayColors: false,
      callbacks: {
        label: (context) => `Score: ${context.parsed.y}%`,
      },
    },
  },
  scales: {
    y: {
      beginAtZero: true,
      max: 100,
      grid: { color: DS.gridLine, drawBorder: false },
      ticks: {
        color: DS.tick,
        font: { family: DS.font, size: 11, weight: '500' },
        stepSize: 20,
        callback: (value) => value + '%',
      },
    },
    x: {
      grid: { display: false, drawBorder: false },
      ticks: { color: DS.tick, font: { family: DS.font, size: 11, weight: '600' } },
    },
  },
}

onMounted(() => {
  if (props.evolucao.length > 0) {
    setTimeout(() => { chartDataVisivel.value = true }, 100)
  }
})

watch(() => props.evolucao, (newVal) => {
  if (newVal.length > 0) chartDataVisivel.value = true
}, { deep: true })
</script>

<style scoped>
.evolucao-container {
  margin-bottom: var(--space-6);
  font-family: var(--font-body);
  background: var(--card-bg);
  border: 1px solid var(--card-border);
  border-radius: var(--card-radius);
  box-shadow: var(--card-shadow);
  padding: var(--space-7-5, 30px);
}

.chart-header { margin-bottom: var(--space-5); }

.chart-title {
  font-family: var(--font-display);
  font-size: var(--text-xl);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  margin: 0 0 var(--space-1) 0;
}

.chart-subtitle {
  color: var(--color-comet);
  font-size: var(--text-sm);
  margin: 0;
}

.canvas-wrapper {
  position: relative;
  height: 280px;
  width: 100%;
}
</style>

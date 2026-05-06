<template>
  <a
    :href="material.url || '#'"
    :target="material.url ? '_blank' : undefined"
    rel="noopener noreferrer"
    class="group flex items-center gap-3 p-3 rounded-xl border border-slate-100 bg-white shadow-simus-soft transition-all duration-200 hover:border-simus-primary/30 hover:shadow-md active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-simus-primary/50"
  >
    <!-- Ícone por tipo -->
    <div
      class="shrink-0 w-10 h-10 rounded-xl flex items-center justify-center text-lg"
      :class="iconBg"
    >
      {{ icon }}
    </div>

    <!-- Conteúdo -->
    <div class="flex-1 min-w-0">
      <p class="text-sm font-body font-semibold text-simus-text truncate">{{ material.titulo }}</p>
      <div class="flex items-center gap-2 mt-0.5">
        <span class="text-[11px] font-bold uppercase tracking-wide px-1.5 py-0.5 rounded" :class="badgeClass">
          {{ material.tipo }}
        </span>
        <span v-if="material.tamanho_kb" class="text-[11px] text-simus-muted">
          {{ formatSize(material.tamanho_kb) }}
        </span>
      </div>
    </div>

    <!-- Seta -->
    <svg
      class="shrink-0 w-4 h-4 text-slate-300 group-hover:text-simus-primary transition-colors"
      fill="none" viewBox="0 0 16 16"
    >
      <path d="M6 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </a>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  material: { type: Object, required: true },
})

const CONFIG = {
  PDF:       { icon: '📄', bg: 'bg-red-50 text-red-600',    badge: 'bg-red-100 text-red-700' },
  VIDEO:     { icon: '▶️', bg: 'bg-indigo-50 text-indigo-600', badge: 'bg-indigo-100 text-indigo-700' },
  LINK:      { icon: '🔗', bg: 'bg-sky-50 text-sky-600',    badge: 'bg-sky-100 text-sky-700' },
  EXERCICIO: { icon: '📝', bg: 'bg-amber-50 text-amber-600', badge: 'bg-amber-100 text-amber-700' },
}

const cfg = computed(() => CONFIG[props.material.tipo] || CONFIG.LINK)
const icon = computed(() => cfg.value.icon)
const iconBg = computed(() => cfg.value.bg)
const badgeClass = computed(() => cfg.value.badge)

function formatSize(kb) {
  if (kb >= 1024) return `${(kb / 1024).toFixed(1)} MB`
  return `${kb} KB`
}
</script>

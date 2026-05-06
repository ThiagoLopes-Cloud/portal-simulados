<template>
  <button
    type="button"
    class="group relative w-full text-left rounded-2xl overflow-hidden border border-slate-100 shadow-simus-soft bg-white transition-all duration-300 md:hover:shadow-xl md:hover:-translate-y-1 active:scale-[0.98] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-simus-primary/50"
    @click="$emit('click')"
  >
    <!-- Header com gradiente da cor da trilha -->
    <div
      class="relative h-28 flex items-end p-4"
      :style="{ background: `linear-gradient(135deg, ${trilha.cor}22 0%, ${trilha.cor}44 100%)` }"
    >
      <!-- Ícone grande no canto superior direito -->
      <span class="absolute top-4 right-4 text-4xl opacity-60 select-none">{{ trilha.icone }}</span>

      <!-- Badge de progresso -->
      <span
        v-if="trilha.percentual_progresso === 100"
        class="absolute top-3 left-3 bg-emerald-500 text-white text-[10px] font-display font-bold px-2 py-0.5 rounded-full"
      >COMPLETO ✓</span>
      <span
        v-else-if="trilha.aulas_concluidas > 0"
        class="absolute top-3 left-3 bg-simus-primary text-white text-[10px] font-display font-bold px-2 py-0.5 rounded-full"
      >EM PROGRESSO</span>

      <h3 class="font-display font-bold text-simus-text text-lg leading-tight pr-12">
        {{ trilha.nome }}
      </h3>
    </div>

    <!-- Body -->
    <div class="p-4 space-y-3">
      <!-- Meta: módulos e aulas -->
      <div class="flex items-center gap-3 text-xs text-simus-muted font-body">
        <span class="flex items-center gap-1">
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 16 16"><rect x="2" y="2" width="5" height="5" rx="1" fill="currentColor"/><rect x="9" y="2" width="5" height="5" rx="1" fill="currentColor"/><rect x="2" y="9" width="5" height="5" rx="1" fill="currentColor"/><rect x="9" y="9" width="5" height="5" rx="1" fill="currentColor" opacity=".4"/></svg>
          {{ trilha.total_modulos }} módulos
        </span>
        <span>·</span>
        <span class="flex items-center gap-1">
          <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 16 16"><circle cx="8" cy="8" r="6" stroke="currentColor" stroke-width="1.5"/><path d="M6 5.5l5 2.5-5 2.5V5.5z" fill="currentColor"/></svg>
          {{ trilha.total_aulas }} aulas
        </span>
        <span>·</span>
        <span class="text-simus-primary font-semibold">{{ trilha.aulas_concluidas }}/{{ trilha.total_aulas }}</span>
      </div>

      <!-- Barra de progresso -->
      <div class="space-y-1">
        <div class="h-2 w-full bg-slate-100 rounded-full overflow-hidden">
          <div
            class="h-full rounded-full transition-all duration-700 ease-out"
            :style="{
              width: `${trilha.percentual_progresso}%`,
              background: trilha.percentual_progresso === 100
                ? '#10b981'
                : `linear-gradient(90deg, ${trilha.cor}, ${trilha.cor}cc)`
            }"
          />
        </div>
        <div class="flex justify-between items-center">
          <span class="text-[11px] text-simus-muted">{{ trilha.percentual_progresso }}% concluído</span>
          <span v-if="trilha.percentual_progresso < 100" class="text-[11px] font-semibold text-simus-primary">
            +{{ trilha.total_aulas - trilha.aulas_concluidas }} restantes
          </span>
        </div>
      </div>
    </div>
  </button>
</template>

<script setup>
defineProps({
  trilha: { type: Object, required: true },
})
defineEmits(['click'])
</script>

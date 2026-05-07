<template>
  <div class="sl-filter" :class="{ 'sl-filter--inline': inline }">
    <!-- Trigger (inline=false) -->
    <template v-if="!inline">
      <button
        class="sl-filter-trigger"
        :class="{ 'sl-filter-trigger--active': activeCount > 0 }"
        type="button"
        :aria-expanded="isOpen"
        @click="isOpen = !isOpen"
      >
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3"/></svg>
        Filtros
        <span v-if="activeCount > 0" class="sl-filter-badge">{{ activeCount }}</span>
      </button>

      <Transition name="sl-filter-panel">
        <div v-if="isOpen" class="sl-filter-panel sl-filter-panel--popover" ref="panelRef">
          <div class="sl-filter-panel-header">
            <span class="sl-filter-panel-title">Filtros</span>
            <button v-if="activeCount > 0" class="sl-filter-clear-all" @click="clearAll">Limpar tudo</button>
          </div>
          <div class="sl-filter-panel-body">
            <slot :groups="groups" :toggle="toggleOption" :clearGroup="clearGroup" :activeValues="activeValues">
              <FilterGroups :groups="groups" :activeValues="activeValues" @toggle="toggleOption" @clearGroup="clearGroup" />
            </slot>
          </div>
          <div class="sl-filter-panel-footer">
            <button class="sl-filter-btn sl-filter-btn--ghost" @click="clearAll">Resetar</button>
            <button class="sl-filter-btn sl-filter-btn--primary" @click="apply">Aplicar</button>
          </div>
        </div>
      </Transition>
    </template>

    <!-- Inline mode -->
    <template v-else>
      <!-- Active chips bar -->
      <Transition name="sl-filter-chips">
        <div v-if="activeCount > 0" class="sl-filter-chips">
          <span class="sl-filter-chips-label">Filtros ativos:</span>
          <template v-for="(vals, gKey) in activeValues" :key="gKey">
            <span
              v-for="val in vals"
              :key="val"
              class="sl-filter-chip"
            >
              {{ getOptionLabel(gKey, val) }}
              <button
                class="sl-filter-chip-remove"
                :aria-label="`Remover filtro ${getOptionLabel(gKey, val)}`"
                @click="toggleOption(gKey, val)"
              >
                <svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
              </button>
            </span>
          </template>
          <button class="sl-filter-clear-chip" @click="clearAll">Limpar tudo</button>
        </div>
      </Transition>

      <!-- Filter groups -->
      <FilterGroups :groups="groups" :activeValues="activeValues" @toggle="toggleOption" @clearGroup="clearGroup" />
    </template>
  </div>
</template>

<!-- Sub-component: renders filter groups -->
<script>
const FilterGroups = {
  name: 'FilterGroups',
  props: {
    groups:       { type: Array,  default: () => [] },
    activeValues: { type: Object, default: () => ({}) },
  },
  emits: ['toggle', 'clearGroup'],
  data() { return { collapsed: {} } },
  methods: {
    isCollapsed(key) { return !!this.collapsed[key] },
    toggleCollapse(key) { this.collapsed[key] = !this.collapsed[key] },
    isActive(gKey, val) { return (this.activeValues[gKey] || []).includes(val) },
  },
  template: `
    <div class="sl-filter-groups">
      <div v-for="group in groups" :key="group.key" class="sl-filter-group">
        <button
          class="sl-filter-group-header"
          :aria-expanded="!isCollapsed(group.key)"
          @click="toggleCollapse(group.key)"
        >
          <span class="sl-filter-group-label">{{ group.label }}</span>
          <span v-if="(activeValues[group.key] || []).length" class="sl-filter-group-count">
            {{ (activeValues[group.key] || []).length }}
          </span>
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"
            :style="{ transform: isCollapsed(group.key) ? 'rotate(-90deg)' : 'rotate(0deg)', transition: 'transform 0.2s ease' }"
            aria-hidden="true"><polyline points="6 9 12 15 18 9"/></svg>
        </button>

        <div v-show="!isCollapsed(group.key)" class="sl-filter-group-body">
          <template v-if="group.type === 'checkbox' || !group.type">
            <label
              v-for="opt in group.options"
              :key="opt.value"
              class="sl-filter-option"
              :class="{ 'sl-filter-option--checked': isActive(group.key, opt.value), 'sl-filter-option--disabled': opt.disabled }"
            >
              <input
                type="checkbox"
                class="sl-filter-checkbox"
                :checked="isActive(group.key, opt.value)"
                :disabled="opt.disabled"
                @change="$emit('toggle', group.key, opt.value)"
              />
              <span class="sl-filter-checkmark" aria-hidden="true" />
              <span class="sl-filter-option-label">{{ opt.label }}</span>
              <span v-if="opt.count !== undefined" class="sl-filter-option-count">{{ opt.count }}</span>
            </label>
          </template>

          <template v-else-if="group.type === 'radio'">
            <label
              v-for="opt in group.options"
              :key="opt.value"
              class="sl-filter-option"
              :class="{ 'sl-filter-option--checked': isActive(group.key, opt.value) }"
            >
              <input
                type="radio"
                class="sl-filter-radio"
                :name="group.key"
                :value="opt.value"
                :checked="isActive(group.key, opt.value)"
                @change="$emit('toggle', group.key, opt.value)"
              />
              <span class="sl-filter-radiomark" aria-hidden="true" />
              <span class="sl-filter-option-label">{{ opt.label }}</span>
            </label>
          </template>
        </div>
      </div>
    </div>
  `,
}
</script>

<script setup>
import { ref, computed, reactive, onMounted, onUnmounted } from 'vue'

const props = defineProps({
  groups:  { type: Array,   default: () => [] },
  inline:  { type: Boolean, default: false },
  modelValue: { type: Object, default: () => ({}) },
})

const emit = defineEmits(['update:modelValue', 'apply', 'clear'])

const isOpen      = ref(false)
const panelRef    = ref(null)
const activeValues = reactive({ ...props.modelValue })

const activeCount = computed(() =>
  Object.values(activeValues).reduce((sum, arr) => sum + (arr?.length || 0), 0)
)

function toggleOption(groupKey, value) {
  if (!activeValues[groupKey]) activeValues[groupKey] = []
  const group = props.groups.find(g => g.key === groupKey)
  if (group?.type === 'radio') {
    activeValues[groupKey] = activeValues[groupKey][0] === value ? [] : [value]
  } else {
    const idx = activeValues[groupKey].indexOf(value)
    if (idx === -1) activeValues[groupKey].push(value)
    else            activeValues[groupKey].splice(idx, 1)
  }
  emit('update:modelValue', { ...activeValues })
  if (props.inline) emit('apply', { ...activeValues })
}

function clearGroup(groupKey) {
  activeValues[groupKey] = []
  emit('update:modelValue', { ...activeValues })
}

function clearAll() {
  props.groups.forEach(g => { activeValues[g.key] = [] })
  emit('update:modelValue', { ...activeValues })
  emit('clear')
  if (!props.inline) isOpen.value = false
}

function apply() {
  emit('apply', { ...activeValues })
  isOpen.value = false
}

function getOptionLabel(gKey, val) {
  const group = props.groups.find(g => g.key === gKey)
  const opt   = group?.options?.find(o => o.value === val)
  return opt?.label ?? val
}

function handleOutsideClick(e) {
  if (panelRef.value && !panelRef.value.closest('.sl-filter')?.contains(e.target)) {
    isOpen.value = false
  }
}

onMounted(() => document.addEventListener('mousedown', handleOutsideClick))
onUnmounted(() => document.removeEventListener('mousedown', handleOutsideClick))
</script>

<style scoped>
/* ── Trigger ── */
.sl-filter-trigger {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  height: var(--btn-height-md);
  padding: 0 var(--space-4);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-comet);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--btn-radius);
  cursor: pointer;
  transition:
    color var(--duration-fast) var(--ease-out),
    border-color var(--duration-fast) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out);
}
.sl-filter-trigger:hover {
  color: var(--color-star);
  border-color: var(--color-border-hover);
}
.sl-filter-trigger--active {
  color: var(--color-orbit);
  border-color: var(--color-orbit-border);
  background: var(--color-orbit-dim);
}
.sl-filter-trigger:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

.sl-filter-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 18px;
  height: 18px;
  padding: 0 var(--space-1);
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  color: var(--color-cosmos);
  background: var(--color-orbit);
  border-radius: var(--radius-full);
}

/* ── Panel (popover) ── */
.sl-filter-panel--popover {
  position: absolute;
  top: calc(100% + var(--space-2));
  left: 0;
  z-index: var(--z-dropdown);
  min-width: 260px;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-hover);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
}

.sl-filter-panel-enter-active { transition: opacity var(--duration-fast) var(--ease-out), transform var(--duration-fast) var(--ease-out); }
.sl-filter-panel-leave-active { transition: opacity var(--duration-fast) var(--ease-in); }
.sl-filter-panel-enter-from   { opacity: 0; transform: translateY(-6px) scale(0.97); }
.sl-filter-panel-leave-to     { opacity: 0; }

.sl-filter-panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-4);
  border-bottom: 1px solid var(--color-border);
}
.sl-filter-panel-title {
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-star);
}
.sl-filter-panel-body { padding: var(--space-2) 0; max-height: 360px; overflow-y: auto; }
.sl-filter-panel-footer {
  display: flex;
  justify-content: flex-end;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  border-top: 1px solid var(--color-border);
}

/* ── Buttons ── */
.sl-filter-btn {
  height: var(--btn-height-sm);
  padding: 0 var(--space-4);
  border-radius: var(--btn-radius);
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  cursor: pointer;
  transition: background-color var(--duration-fast) var(--ease-out), color var(--duration-fast) var(--ease-out);
}
.sl-filter-btn--ghost {
  background: none;
  border: 1px solid var(--color-border);
  color: var(--color-comet);
}
.sl-filter-btn--ghost:hover { border-color: var(--color-border-hover); color: var(--color-star); }
.sl-filter-btn--primary {
  background: var(--color-orbit);
  border: 1px solid transparent;
  color: var(--color-cosmos);
}
.sl-filter-btn--primary:hover { background: var(--color-orbit-bright); }

/* ── Clear all ── */
.sl-filter-clear-all {
  font-size: var(--text-xs);
  color: var(--color-dust);
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
  transition: color var(--duration-fast) var(--ease-out);
}
.sl-filter-clear-all:hover { color: var(--color-nova); }

/* ── Groups ── */
:deep(.sl-filter-groups) { display: flex; flex-direction: column; }
:deep(.sl-filter-group)  { border-bottom: 1px solid var(--color-border); }
:deep(.sl-filter-group):last-child { border-bottom: none; }

:deep(.sl-filter-group-header) {
  width: 100%;
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-3) var(--space-4);
  background: none;
  border: none;
  cursor: pointer;
  font-family: var(--font-body);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-comet);
  transition: color var(--duration-fast) var(--ease-out);
}
:deep(.sl-filter-group-header):hover { color: var(--color-star); }

:deep(.sl-filter-group-label) { flex: 1; text-align: left; }

:deep(.sl-filter-group-count) {
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  color: var(--color-orbit);
  background: var(--color-orbit-dim);
  border-radius: var(--radius-full);
  padding: 1px var(--space-1-5);
}

:deep(.sl-filter-group-body) { padding: 0 var(--space-4) var(--space-3); display: flex; flex-direction: column; gap: var(--space-1); }

/* ── Options ── */
:deep(.sl-filter-option) {
  display: flex;
  align-items: center;
  gap: var(--space-2-5);
  padding: var(--space-1-5) var(--space-2);
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-size: var(--text-sm);
  color: var(--color-comet);
  transition: background-color var(--duration-fast) var(--ease-out), color var(--duration-fast) var(--ease-out);
  user-select: none;
}
:deep(.sl-filter-option):hover { background: var(--color-surface-hover); color: var(--color-star); }
:deep(.sl-filter-option--checked) { color: var(--color-star); }
:deep(.sl-filter-option--disabled) { opacity: 0.4; cursor: not-allowed; }

:deep(.sl-filter-checkbox),
:deep(.sl-filter-radio) { display: none; }

:deep(.sl-filter-checkmark) {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  border-radius: var(--radius-xs);
  border: 1.5px solid var(--color-border-hover);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color var(--duration-fast) var(--ease-out), border-color var(--duration-fast) var(--ease-out);
}
:deep(.sl-filter-option--checked) :deep(.sl-filter-checkmark) {
  background: var(--color-orbit);
  border-color: var(--color-orbit);
}
:deep(.sl-filter-option--checked) :deep(.sl-filter-checkmark)::after {
  content: '';
  width: 9px;
  height: 5px;
  border-left: 2px solid var(--color-cosmos);
  border-bottom: 2px solid var(--color-cosmos);
  transform: rotate(-45deg) translate(1px, -1px);
}

:deep(.sl-filter-radiomark) {
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  border-radius: var(--radius-full);
  border: 1.5px solid var(--color-border-hover);
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-color var(--duration-fast) var(--ease-out);
}
:deep(.sl-filter-option--checked) :deep(.sl-filter-radiomark) {
  border-color: var(--color-orbit);
}
:deep(.sl-filter-option--checked) :deep(.sl-filter-radiomark)::after {
  content: '';
  width: 8px;
  height: 8px;
  border-radius: var(--radius-full);
  background: var(--color-orbit);
}

:deep(.sl-filter-option-label) { flex: 1; }
:deep(.sl-filter-option-count) {
  font-size: var(--text-xs);
  color: var(--color-dust);
}

/* ── Active chips ── */
.sl-filter-chips {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-2) 0;
}
.sl-filter-chips-enter-active,
.sl-filter-chips-leave-active { transition: opacity var(--duration-fast) var(--ease-out), transform var(--duration-fast) var(--ease-out); }
.sl-filter-chips-enter-from,
.sl-filter-chips-leave-to { opacity: 0; transform: translateY(-4px); }

.sl-filter-chips-label {
  font-size: var(--text-xs);
  color: var(--color-dust);
  white-space: nowrap;
}

.sl-filter-chip {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1-5);
  height: 24px;
  padding: 0 var(--space-2-5);
  background: var(--color-orbit-dim);
  border: 1px solid var(--color-orbit-border);
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  color: var(--color-orbit);
}

.sl-filter-chip-remove {
  display: flex;
  align-items: center;
  justify-content: center;
  background: none;
  border: none;
  cursor: pointer;
  color: var(--color-orbit);
  opacity: 0.7;
  padding: 0;
  transition: opacity var(--duration-fast) var(--ease-out);
}
.sl-filter-chip-remove:hover { opacity: 1; }

.sl-filter-clear-chip {
  font-size: var(--text-xs);
  color: var(--color-dust);
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
  transition: color var(--duration-fast) var(--ease-out);
}
.sl-filter-clear-chip:hover { color: var(--color-nova); }

/* ── Inline mode layout ── */
.sl-filter--inline :deep(.sl-filter-groups) {
  flex-direction: row;
  flex-wrap: wrap;
  gap: var(--space-2);
}
.sl-filter--inline :deep(.sl-filter-group) {
  border-bottom: none;
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  overflow: hidden;
}
</style>

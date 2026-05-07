<template>
  <div class="sl-search" :class="[`sl-search--${size}`, { 'sl-search--open': isOpen, 'sl-search--focused': focused }]" ref="rootRef">
    <!-- Input wrapper -->
    <div class="sl-search-input-wrap" @click="openPanel">
      <span class="sl-search-icon" aria-hidden="true">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
      </span>

      <input
        ref="inputRef"
        class="sl-search-input"
        type="search"
        :value="query"
        :placeholder="placeholder"
        :aria-label="placeholder"
        aria-autocomplete="list"
        :aria-expanded="isOpen"
        aria-haspopup="listbox"
        role="combobox"
        autocomplete="off"
        @input="handleInput"
        @focus="handleFocus"
        @blur="handleBlur"
        @keydown="handleKeydown"
      />

      <Transition name="sl-search-clear">
        <button
          v-if="query"
          class="sl-search-clear"
          type="button"
          aria-label="Limpar busca"
          @click.stop="clear"
        >
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>
        </button>
      </Transition>

      <span v-if="shortcut && !query" class="sl-search-shortcut" aria-hidden="true">{{ shortcut }}</span>
    </div>

    <!-- Dropdown panel -->
    <Transition name="sl-search-panel">
      <div
        v-if="isOpen && (filteredSuggestions.length || recentSearches.length || query)"
        class="sl-search-panel"
        role="listbox"
        :aria-label="query ? 'Resultados da busca' : 'Buscas recentes'"
      >
        <!-- Recent searches (empty query) -->
        <template v-if="!query && recentSearches.length">
          <p class="sl-search-group-label">Recentes</p>
          <button
            v-for="(item, i) in recentSearches"
            :key="`recent-${i}`"
            class="sl-search-item"
            :class="{ 'sl-search-item--active': activeIndex === i }"
            role="option"
            :aria-selected="activeIndex === i"
            @click="selectItem(item)"
            @mouseenter="activeIndex = i"
          >
            <span class="sl-search-item-icon sl-search-item-icon--recent" aria-hidden="true">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-4"/></svg>
            </span>
            <span class="sl-search-item-label">{{ item.label }}</span>
          </button>
        </template>

        <!-- Suggestions -->
        <template v-if="query && filteredSuggestions.length">
          <p v-if="groupLabel" class="sl-search-group-label">{{ groupLabel }}</p>
          <button
            v-for="(item, i) in filteredSuggestions"
            :key="`s-${i}`"
            class="sl-search-item"
            :class="{ 'sl-search-item--active': activeIndex === i }"
            role="option"
            :aria-selected="activeIndex === i"
            @click="selectItem(item)"
            @mouseenter="activeIndex = i"
          >
            <span v-if="item.icon" class="sl-search-item-icon" aria-hidden="true" v-html="item.icon" />
            <span v-else-if="item.type" class="sl-search-item-type-dot" :class="`sl-search-item-type-dot--${item.type}`" aria-hidden="true" />
            <span class="sl-search-item-label" v-html="highlight(item.label)" />
            <span v-if="item.meta" class="sl-search-item-meta">{{ item.meta }}</span>
          </button>
        </template>

        <!-- No results -->
        <div v-if="query && !filteredSuggestions.length && !loading" class="sl-search-empty">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
          <p>Nenhum resultado para <strong>"{{ query }}"</strong></p>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="sl-search-loading">
          <span class="sl-search-spinner" aria-hidden="true" />
          <span>Buscando…</span>
        </div>

        <!-- Search action footer -->
        <div v-if="query" class="sl-search-footer">
          <button class="sl-search-footer-btn" @click="submitSearch">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><polyline points="9 10 4 15 9 20"/><path d="M20 4v7a4 4 0 0 1-4 4H4"/></svg>
            Buscar "{{ query }}"
          </button>
          <span class="sl-search-footer-hint" aria-hidden="true">↑↓ navegar · ↵ selecionar · Esc fechar</span>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted, nextTick } from 'vue'

const props = defineProps({
  modelValue:    { type: String, default: '' },
  placeholder:   { type: String, default: 'Buscar…' },
  suggestions:   { type: Array, default: () => [] },
  recentSearches:{ type: Array, default: () => [] },
  loading:       { type: Boolean, default: false },
  size:          { type: String, default: 'md', validator: v => ['sm', 'md', 'lg'].includes(v) },
  shortcut:      { type: String, default: '' },
  groupLabel:    { type: String, default: '' },
  debounce:      { type: Number, default: 300 },
})

const emit = defineEmits(['update:modelValue', 'search', 'select', 'clear'])

const rootRef   = ref(null)
const inputRef  = ref(null)
const query     = ref(props.modelValue)
const isOpen    = ref(false)
const focused   = ref(false)
const activeIndex = ref(-1)
let debounceTimer = null

const filteredSuggestions = computed(() => {
  if (!query.value) return []
  const q = query.value.toLowerCase()
  return props.suggestions.filter(s => s.label.toLowerCase().includes(q))
})

const listLength = computed(() =>
  query.value ? filteredSuggestions.value.length : props.recentSearches.length
)

function handleInput(e) {
  query.value = e.target.value
  activeIndex.value = -1
  isOpen.value = true
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    emit('update:modelValue', query.value)
    emit('search', query.value)
  }, props.debounce)
}

function handleFocus() {
  focused.value = true
  isOpen.value = true
}

function handleBlur() {
  focused.value = false
}

function openPanel() {
  isOpen.value = true
  nextTick(() => inputRef.value?.focus())
}

function close() {
  isOpen.value = false
  activeIndex.value = -1
}

function clear() {
  query.value = ''
  activeIndex.value = -1
  emit('update:modelValue', '')
  emit('clear')
  nextTick(() => inputRef.value?.focus())
}

function selectItem(item) {
  query.value = item.label
  emit('update:modelValue', item.label)
  emit('select', item)
  close()
}

function submitSearch() {
  emit('search', query.value)
  close()
}

function handleKeydown(e) {
  if (!isOpen.value) return
  switch (e.key) {
    case 'ArrowDown':
      e.preventDefault()
      activeIndex.value = Math.min(activeIndex.value + 1, listLength.value - 1)
      break
    case 'ArrowUp':
      e.preventDefault()
      activeIndex.value = Math.max(activeIndex.value - 1, -1)
      break
    case 'Enter':
      e.preventDefault()
      if (activeIndex.value >= 0) {
        const list = query.value ? filteredSuggestions.value : props.recentSearches
        if (list[activeIndex.value]) selectItem(list[activeIndex.value])
      } else {
        submitSearch()
      }
      break
    case 'Escape':
      e.preventDefault()
      if (query.value) clear()
      else close()
      break
  }
}

function highlight(text) {
  if (!query.value) return text
  const escaped = query.value.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')
  return text.replace(new RegExp(`(${escaped})`, 'gi'), '<mark class="sl-search-highlight">$1</mark>')
}

function handleOutsideClick(e) {
  if (rootRef.value && !rootRef.value.contains(e.target)) close()
}

watch(() => props.modelValue, v => { if (v !== query.value) query.value = v })

onMounted(() => document.addEventListener('mousedown', handleOutsideClick))
onUnmounted(() => {
  document.removeEventListener('mousedown', handleOutsideClick)
  clearTimeout(debounceTimer)
})
</script>

<style scoped>
.sl-search {
  position: relative;
  width: 100%;
}

/* ── Input wrap ── */
.sl-search-input-wrap {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  background: var(--color-bg-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--input-radius);
  padding: 0 var(--space-3);
  cursor: text;
  transition:
    border-color var(--duration-fast) var(--ease-out),
    box-shadow var(--duration-normal) var(--ease-out),
    background-color var(--duration-fast) var(--ease-out);
}

.sl-search-input-wrap:hover {
  border-color: var(--color-border-hover);
  background: var(--color-bg-elevated);
}

.sl-search--focused .sl-search-input-wrap {
  border-color: var(--color-orbit);
  box-shadow: var(--shadow-focus);
  background: var(--color-bg-elevated);
}

/* ── Sizes ── */
.sl-search--sm .sl-search-input-wrap { height: var(--btn-height-sm); }
.sl-search--md .sl-search-input-wrap { height: var(--btn-height-md); }
.sl-search--lg .sl-search-input-wrap { height: var(--btn-height-lg); }

/* ── Icon ── */
.sl-search-icon {
  display: flex;
  align-items: center;
  flex-shrink: 0;
  color: var(--color-dust);
  transition: color var(--duration-fast) var(--ease-out);
}
.sl-search--focused .sl-search-icon { color: var(--color-orbit); }

/* ── Input ── */
.sl-search-input {
  flex: 1;
  background: transparent;
  border: none;
  outline: none;
  font-family: var(--font-body);
  font-size: var(--text-sm);
  color: var(--color-star);
  min-width: 0;
}
.sl-search--lg .sl-search-input { font-size: var(--text-base); }
.sl-search-input::placeholder { color: var(--color-dust); }
.sl-search-input::-webkit-search-cancel-button { display: none; }

/* ── Clear button ── */
.sl-search-clear {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  border-radius: var(--radius-full);
  border: none;
  background: var(--color-bg-elevated);
  color: var(--color-dust);
  cursor: pointer;
  transition: background-color var(--duration-fast) var(--ease-out), color var(--duration-fast) var(--ease-out);
}
.sl-search-clear:hover { background: var(--color-surface-hover); color: var(--color-star); }

.sl-search-clear-enter-active,
.sl-search-clear-leave-active { transition: opacity var(--duration-fast) var(--ease-out), transform var(--duration-fast) var(--ease-out); }
.sl-search-clear-enter-from,
.sl-search-clear-leave-to    { opacity: 0; transform: scale(0.7); }

/* ── Shortcut badge ── */
.sl-search-shortcut {
  flex-shrink: 0;
  font-size: var(--text-2xs);
  font-family: var(--font-mono);
  color: var(--color-dust);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-sm);
  padding: 1px var(--space-1-5);
  line-height: 1.4;
}

/* ── Panel ── */
.sl-search-panel {
  position: absolute;
  top: calc(100% + var(--space-1-5));
  left: 0;
  right: 0;
  z-index: var(--z-dropdown);
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-hover);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  padding: var(--space-1-5);
}

.sl-search-panel-enter-active { transition: opacity var(--duration-fast) var(--ease-out), transform var(--duration-fast) var(--ease-out); }
.sl-search-panel-leave-active { transition: opacity var(--duration-fast) var(--ease-in); }
.sl-search-panel-enter-from   { opacity: 0; transform: translateY(-6px) scale(0.98); }
.sl-search-panel-leave-to     { opacity: 0; }

/* ── Group label ── */
.sl-search-group-label {
  font-size: var(--text-2xs);
  font-weight: var(--weight-semibold);
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--color-dust);
  padding: var(--space-1-5) var(--space-3);
  margin: 0;
}

/* ── Item ── */
.sl-search-item {
  width: 100%;
  display: flex;
  align-items: center;
  gap: var(--space-2-5);
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  background: none;
  border: none;
  font-family: var(--font-body);
  font-size: var(--text-sm);
  color: var(--color-comet);
  cursor: pointer;
  text-align: left;
  transition: background-color var(--duration-fast) var(--ease-out), color var(--duration-fast) var(--ease-out);
}
.sl-search-item:hover,
.sl-search-item--active {
  background: var(--color-surface-hover);
  color: var(--color-star);
}
.sl-search-item--active { background: var(--color-orbit-dim); }

.sl-search-item-icon {
  display: flex;
  align-items: center;
  flex-shrink: 0;
  color: var(--color-dust);
}
.sl-search-item-icon--recent { color: var(--color-dust); }

.sl-search-item-type-dot {
  width: 8px;
  height: 8px;
  border-radius: var(--radius-full);
  flex-shrink: 0;
}
.sl-search-item-type-dot--simulado  { background: var(--color-orbit); }
.sl-search-item-type-dot--trilha    { background: var(--color-pulsar); }
.sl-search-item-type-dot--aluno     { background: var(--color-stellar); }
.sl-search-item-type-dot--turma     { background: var(--color-flare); }

.sl-search-item-label { flex: 1; min-width: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.sl-search-item-meta {
  font-size: var(--text-xs);
  color: var(--color-dust);
  white-space: nowrap;
  flex-shrink: 0;
}

/* ── Highlight ── */
:deep(.sl-search-highlight) {
  background: transparent;
  color: var(--color-orbit);
  font-weight: var(--weight-semibold);
}

/* ── Empty ── */
.sl-search-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-6) var(--space-4);
  color: var(--color-dust);
  text-align: center;
}
.sl-search-empty p { font-size: var(--text-sm); margin: 0; }
.sl-search-empty strong { color: var(--color-comet); }

/* ── Loading ── */
.sl-search-loading {
  display: flex;
  align-items: center;
  gap: var(--space-2-5);
  padding: var(--space-3) var(--space-4);
  font-size: var(--text-sm);
  color: var(--color-dust);
}
.sl-search-spinner {
  width: 14px;
  height: 14px;
  border: 2px solid var(--color-border-hover);
  border-top-color: var(--color-orbit);
  border-radius: var(--radius-full);
  animation: spinnerRing 0.7s linear infinite;
  flex-shrink: 0;
}

/* ── Footer ── */
.sl-search-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-2) var(--space-3) var(--space-1);
  border-top: 1px solid var(--color-border);
  margin-top: var(--space-1);
}
.sl-search-footer-btn {
  display: flex;
  align-items: center;
  gap: var(--space-1-5);
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  color: var(--color-orbit);
  background: none;
  border: none;
  cursor: pointer;
  padding: var(--space-1) var(--space-2);
  border-radius: var(--radius-sm);
  transition: background-color var(--duration-fast) var(--ease-out);
  max-width: 60%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.sl-search-footer-btn:hover { background: var(--color-orbit-dim); }
.sl-search-footer-hint {
  font-size: var(--text-2xs);
  color: var(--color-dust);
  font-family: var(--font-mono);
  white-space: nowrap;
}
</style>

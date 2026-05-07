<template>
  <div class="sl-table-wrap">
    <div v-if="loading" class="sl-table-skeleton">
      <div v-for="i in skeletonRows" :key="i" class="sl-table-skeleton-row">
        <div v-for="j in columns.length" :key="j" class="sl-table-skeleton-cell" />
      </div>
    </div>

    <table v-else class="sl-table" :class="{ 'sl-table--hoverable': hoverable }" role="table">
      <caption v-if="caption" class="sr-only">{{ caption }}</caption>
      <thead>
        <tr class="sl-table-head-row">
          <th
            v-for="col in columns"
            :key="col.key"
            class="sl-th"
            :class="[col.align ? `sl-th--${col.align}` : '', col.class]"
            scope="col"
          >
            {{ col.label }}
          </th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(row, rowIndex) in rows"
          :key="rowIndex"
          class="sl-table-row"
          :class="rowClass ? rowClass(row, rowIndex) : ''"
          @click="hoverable && $emit('row-click', row)"
        >
          <td
            v-for="col in columns"
            :key="col.key"
            class="sl-td"
            :class="[col.align ? `sl-td--${col.align}` : '', col.class]"
          >
            <slot :name="`cell-${col.key}`" :row="row" :value="row[col.key]" :index="rowIndex">
              {{ row[col.key] }}
            </slot>
          </td>
        </tr>
        <tr v-if="rows.length === 0">
          <td :colspan="columns.length" class="sl-td sl-td--empty">
            <slot name="empty">
              <span class="sl-table-empty-text">Nenhum resultado encontrado.</span>
            </slot>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
defineProps({
  columns:      { type: Array,    required: true },
  rows:         { type: Array,    default: () => [] },
  loading:      { type: Boolean,  default: false },
  hoverable:    { type: Boolean,  default: true },
  caption:      { type: String,   default: '' },
  rowClass:     { type: Function, default: null },
  skeletonRows: { type: Number,   default: 5 },
})

defineEmits(['row-click'])
</script>

<style scoped>
.sl-table-wrap {
  width: 100%;
  overflow-x: auto;
  border-radius: var(--card-radius);
  border: 1px solid var(--card-border);
  background: var(--card-bg);
}

/* ── Table ── */
.sl-table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-sm);
}

/* ── Head ── */
.sl-table-head-row {
  border-bottom: 1px solid var(--color-border);
}

.sl-th {
  padding: var(--space-3) var(--space-4);
  text-align: left;
  font-family: var(--font-body);
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  color: var(--color-dust);
  white-space: nowrap;
}

.sl-th--center { text-align: center; }
.sl-th--right  { text-align: right; }

/* ── Body rows ── */
.sl-table-row {
  border-bottom: 1px solid var(--color-border);
  transition: background-color var(--duration-fast) var(--ease-out);
}
.sl-table-row:last-child { border-bottom: none; }

.sl-table--hoverable .sl-table-row {
  cursor: pointer;
}
.sl-table--hoverable .sl-table-row:hover {
  background: var(--color-surface-hover);
}

.sl-td {
  padding: var(--space-3) var(--space-4);
  color: var(--color-comet);
  font-family: var(--font-body);
  vertical-align: middle;
}

.sl-td--center { text-align: center; }
.sl-td--right  { text-align: right; }
.sl-td--empty  { text-align: center; padding: var(--space-10); }

.sl-table-empty-text {
  color: var(--color-dust);
  font-size: var(--text-sm);
}

/* ── Skeleton ── */
.sl-table-skeleton {
  padding: var(--space-3);
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.sl-table-skeleton-row {
  display: flex;
  gap: var(--space-3);
}

.sl-table-skeleton-cell {
  flex: 1;
  height: 36px;
  background: var(--color-bg-elevated);
  border-radius: var(--radius-xs);
  position: relative;
  overflow: hidden;
}

.sl-table-skeleton-cell::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.04), transparent);
  animation: shimmer 1.6s infinite;
}
</style>

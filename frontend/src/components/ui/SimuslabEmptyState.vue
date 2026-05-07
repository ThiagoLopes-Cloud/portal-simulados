<template>
  <div class="sl-empty" :class="{ 'sl-empty--card': card }">
    <div v-if="icon || $slots.icon" class="sl-empty-icon" :class="`sl-empty-icon--${color}`">
      <slot name="icon">
        <svg v-if="icon === 'document'" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
        <svg v-else-if="icon === 'trophy'" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="7"/><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"/></svg>
        <svg v-else-if="icon === 'search'" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
        <svg v-else-if="icon === 'book'" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg>
        <svg v-else-if="icon === 'users'" width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
        <svg v-else width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.25" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
      </slot>
    </div>

    <div class="sl-empty-text">
      <h3 v-if="title" class="sl-empty-title">{{ title }}</h3>
      <p v-if="description" class="sl-empty-desc">{{ description }}</p>
      <slot name="description" />
    </div>

    <div v-if="actionLabel || $slots.action" class="sl-empty-actions">
      <slot name="action">
        <SimuslabButton :variant="actionVariant" :size="actionSize" @click="$emit('action')">
          {{ actionLabel }}
        </SimuslabButton>
      </slot>
    </div>
  </div>
</template>

<script setup>
import SimuslabButton from './SimuslabButton.vue'

defineProps({
  icon:          { type: String, default: '' },
  title:         { type: String, default: '' },
  description:   { type: String, default: '' },
  actionLabel:   { type: String, default: '' },
  actionVariant: { type: String, default: 'primary' },
  actionSize:    { type: String, default: 'md' },
  color:         { type: String, default: 'orbit' },
  card:          { type: Boolean, default: false },
})

defineEmits(['action'])
</script>

<style scoped>
.sl-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: var(--space-12) var(--space-8);
  gap: var(--space-5);
}

.sl-empty--card {
  background: var(--card-bg);
  border: 1px dashed var(--color-border);
  border-radius: var(--card-radius);
}

/* ── Icon ── */
.sl-empty-icon {
  width: 72px;
  height: 72px;
  border-radius: var(--radius-xl);
  display: flex;
  align-items: center;
  justify-content: center;
}

.sl-empty-icon--orbit   { background: var(--color-orbit-dim);   color: var(--color-orbit);   border: 1px solid var(--color-orbit-border); }
.sl-empty-icon--pulsar  { background: var(--color-pulsar-dim);  color: var(--color-pulsar);  border: 1px solid var(--color-pulsar-border); }
.sl-empty-icon--stellar { background: var(--color-stellar-dim); color: var(--color-stellar); border: 1px solid var(--color-stellar-border); }
.sl-empty-icon--nova    { background: var(--color-nova-dim);    color: var(--color-nova);    border: 1px solid var(--color-nova-border); }
.sl-empty-icon--flare   { background: var(--color-flare-dim);   color: var(--color-flare);   border: 1px solid var(--color-flare-border); }

/* ── Text ── */
.sl-empty-text {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.sl-empty-title {
  font-family: var(--font-display);
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  color: var(--color-star);
  letter-spacing: var(--tracking-tight);
}

.sl-empty-desc {
  font-size: var(--text-sm);
  color: var(--color-comet);
  line-height: var(--leading-relaxed);
  max-width: 380px;
}

/* ── Actions ── */
.sl-empty-actions { display: flex; gap: var(--space-2); flex-wrap: wrap; justify-content: center; }
</style>

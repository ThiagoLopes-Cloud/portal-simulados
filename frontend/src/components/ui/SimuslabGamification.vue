<template>
  <!-- XP Bar widget -->
  <div v-if="type === 'xpbar'" class="sl-xpbar">
    <div class="sl-xpbar-info">
      <span class="sl-xpbar-level">Nível {{ level }}</span>
      <span class="sl-xpbar-xp">{{ currentXP }}<span class="sl-xpbar-max">/{{ nextLevelXP }} XP</span></span>
    </div>
    <div class="sl-xpbar-track">
      <div class="sl-xpbar-fill" :style="{ width: `${progress}%` }" />
    </div>
  </div>

  <!-- Level badge -->
  <div v-else-if="type === 'level'" class="sl-level-badge" :class="`sl-level--${tier}`">
    <span class="sl-level-num">{{ level }}</span>
    <span class="sl-level-label">NVL</span>
  </div>

  <!-- Streak counter -->
  <div v-else-if="type === 'streak'" class="sl-streak" :class="{ 'sl-streak--active': streak > 0 }">
    <svg class="sl-streak-flame" width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      <path d="M12 2C9.5 7 7 8.5 7 12a5 5 0 0 0 10 0c0-5-3-7-5-10zM9 16.5A2.5 2.5 0 0 0 11.5 19c1.38 0 2.5-1.12 2.5-2.5 0-2-2-3-2-3s-3 1-3 3z"/>
    </svg>
    <span class="sl-streak-count">{{ streak }}</span>
    <span class="sl-streak-label">dias</span>
  </div>

  <!-- Rank medal -->
  <div v-else-if="type === 'medal'" class="sl-medal" :class="`sl-medal--${position}`">
    <span v-if="position === 1" class="sl-medal-emoji">🥇</span>
    <span v-else-if="position === 2" class="sl-medal-emoji">🥈</span>
    <span v-else-if="position === 3" class="sl-medal-emoji">🥉</span>
    <span v-else class="sl-medal-pos">{{ position }}°</span>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  type:    { type: String, default: 'xpbar', validator: v => ['xpbar', 'level', 'streak', 'medal'].includes(v) },
  level:   { type: Number, default: 1 },
  xp:      { type: Number, default: 0 },
  xpPerLevel: { type: Number, default: 500 },
  streak:  { type: Number, default: 0 },
  position: { type: Number, default: 0 },
})

const currentXP    = computed(() => props.xp % props.xpPerLevel)
const nextLevelXP  = computed(() => props.xpPerLevel)
const progress     = computed(() => Math.min(100, (currentXP.value / nextLevelXP.value) * 100))

const tier = computed(() => {
  if (props.level >= 20) return 'diamond'
  if (props.level >= 10) return 'gold'
  if (props.level >= 5)  return 'silver'
  return 'bronze'
})
</script>

<style scoped>
/* ── XP Bar ── */
.sl-xpbar {
  display: flex;
  flex-direction: column;
  gap: var(--space-1);
  min-width: 120px;
}

.sl-xpbar-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.sl-xpbar-level {
  font-family: var(--font-body);
  font-size: var(--text-2xs);
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  color: var(--color-orbit);
}

.sl-xpbar-xp {
  font-family: var(--font-mono);
  font-size: var(--text-2xs);
  color: var(--color-comet);
}

.sl-xpbar-max {
  color: var(--color-dust);
}

.sl-xpbar-track {
  height: 4px;
  background: var(--color-bg-elevated);
  border-radius: var(--radius-full);
  overflow: hidden;
}

.sl-xpbar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-orbit), var(--color-orbit-bright));
  border-radius: var(--radius-full);
  transition: width var(--duration-slow) var(--ease-out);
  box-shadow: 0 0 8px rgba(0, 229, 255, 0.4);
}

/* ── Level Badge ── */
.sl-level-badge {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  border: 1px solid;
  line-height: 1;
  gap: 1px;
}

.sl-level--bronze  { background: rgba(205, 127, 50, 0.1); border-color: rgba(205, 127, 50, 0.3); color: #CD7F32; }
.sl-level--silver  { background: rgba(192, 200, 216, 0.1); border-color: rgba(192, 200, 216, 0.3); color: var(--color-silver); }
.sl-level--gold    { background: rgba(255, 215, 0, 0.1);   border-color: rgba(255, 215, 0, 0.3);   color: var(--color-gold); }
.sl-level--diamond { background: var(--color-orbit-dim);   border-color: var(--color-orbit-border); color: var(--color-orbit); }

.sl-level-num {
  font-family: var(--font-display);
  font-size: var(--text-base);
  font-weight: var(--weight-extrabold);
}
.sl-level-label {
  font-size: 0.55rem;
  font-weight: var(--weight-bold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wider);
  opacity: 0.7;
}

/* ── Streak ── */
.sl-streak {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: 3px var(--space-2-5);
  border-radius: var(--radius-full);
  background: var(--color-flare-dim);
  border: 1px solid var(--color-flare-border);
  color: var(--color-flare);
}

.sl-streak--active {
  box-shadow: 0 0 10px var(--color-flare-dim);
}

.sl-streak-flame { flex-shrink: 0; }

.sl-streak-count {
  font-family: var(--font-display);
  font-size: var(--text-sm);
  font-weight: var(--weight-extrabold);
}

.sl-streak-label {
  font-size: var(--text-2xs);
  font-weight: var(--weight-medium);
  opacity: 0.7;
}

/* ── Medal ── */
.sl-medal {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full);
}

.sl-medal--1 { background: rgba(255, 215, 0, 0.1); border: 1px solid rgba(255, 215, 0, 0.4); }
.sl-medal--2 { background: rgba(192, 200, 216, 0.1); border: 1px solid rgba(192, 200, 216, 0.3); }
.sl-medal--3 { background: rgba(205, 127, 50, 0.1); border: 1px solid rgba(205, 127, 50, 0.3); }

.sl-medal-emoji { font-size: 1.1rem; }
.sl-medal-pos {
  font-family: var(--font-mono);
  font-size: var(--text-xs);
  font-weight: var(--weight-bold);
  color: var(--color-comet);
}
</style>

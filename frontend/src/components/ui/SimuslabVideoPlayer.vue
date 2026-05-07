<template>
  <div class="sl-vp" :class="{ 'sl-vp--active': isActive, 'sl-vp--no-url': !url }">

    <!-- No video state -->
    <div v-if="!url" class="sl-vp-empty">
      <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <rect x="2" y="3" width="20" height="14" rx="2"/><polyline points="8 21 12 17 16 21"/>
      </svg>
      <p>Vídeo não disponível</p>
    </div>

    <!-- Poster (thumbnail + play) -->
    <div
      v-else-if="!isActive"
      class="sl-vp-poster"
      @click="activate"
      role="button"
      tabindex="0"
      :aria-label="`Assistir aula: ${title}`"
      @keydown.enter.space.prevent="activate"
    >
      <img
        v-if="!thumbFailed && thumbnailSrc"
        :src="thumbnailSrc"
        :alt="title"
        class="sl-vp-thumb"
        @error="onThumbError"
      />
      <div v-else class="sl-vp-thumb-fallback">
        <div class="sl-vp-thumb-gradient" :style="gradientStyle" />
      </div>

      <!-- Overlay -->
      <div class="sl-vp-overlay">
        <button class="sl-vp-play-btn" type="button" :aria-label="`Assistir: ${title}`" tabindex="-1">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
            <path d="M8 5.14v14l11-7-11-7z"/>
          </svg>
        </button>
      </div>

      <!-- Footer meta -->
      <div class="sl-vp-footer">
        <span v-if="watched" class="sl-vp-watched">
          <svg width="11" height="11" viewBox="0 0 12 12" fill="none" aria-hidden="true">
            <path d="M2 6l3 3 5-5" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
          Assistido
        </span>
        <span v-if="duration" class="sl-vp-duration">{{ duration }}min</span>
      </div>
    </div>

    <!-- Active embed -->
    <div v-else class="sl-vp-frame-wrap">
      <iframe
        v-if="embedSrc"
        :src="embedSrc"
        class="sl-vp-frame"
        allowfullscreen
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        :title="title"
      />
      <div v-else class="sl-vp-unsupported">
        <p>Formato de vídeo não suportado para incorporação.</p>
        <a :href="url" target="_blank" rel="noopener noreferrer" class="sl-vp-link">
          Abrir externamente
          <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
        </a>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

const props = defineProps({
  url:      { type: String, default: '' },
  title:    { type: String, default: 'Aula' },
  duration: { type: Number, default: 0 },
  aulaId:   { type: Number, default: null },
  watched:  { type: Boolean, default: false },
  accent:   { type: String, default: '#00E5FF' },
})

const emit = defineEmits(['play'])

const isActive  = ref(false)
const thumbFailed = ref(false)

const youtubeId = computed(() => {
  if (!props.url) return null
  const m = props.url.match(
    /(?:youtu\.be\/|youtube\.com\/(?:watch\?v=|embed\/|v\/|shorts\/))([^&?/\s]{11})/
  )
  return m?.[1] ?? null
})

const thumbnailSrc = computed(() => {
  if (!youtubeId.value) return ''
  return `https://img.youtube.com/vi/${youtubeId.value}/maxresdefault.jpg`
})

const embedSrc = computed(() => {
  if (youtubeId.value) {
    return `https://www.youtube.com/embed/${youtubeId.value}?autoplay=1&rel=0&modestbranding=1&showinfo=0`
  }
  if (props.url?.match(/\.(mp4|webm|ogg)(\?.*)?$/i)) {
    return props.url
  }
  return ''
})

const gradientStyle = computed(() => ({
  background: `linear-gradient(135deg, ${props.accent}22 0%, ${props.accent}44 100%)`,
}))

function onThumbError() {
  if (!thumbFailed.value) {
    const img = new Image()
    img.src = `https://img.youtube.com/vi/${youtubeId.value}/hqdefault.jpg`
    img.onload  = () => { /* hqdefault loads fine, browser will retry */ }
    img.onerror = () => { thumbFailed.value = true }
  }
}

function activate() {
  if (!props.url) return
  isActive.value = true
  emit('play', props.aulaId)
}

watch(() => props.url, () => {
  isActive.value = false
  thumbFailed.value = false
})
</script>

<style scoped>
.sl-vp {
  position: relative;
  width: 100%;
  aspect-ratio: 16 / 9;
  border-radius: var(--radius-xl);
  overflow: hidden;
  background: var(--color-bg-panel);
  border: 1px solid var(--color-border);
}

/* ── Empty ── */
.sl-vp-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  height: 100%;
  color: var(--color-dust);
}
.sl-vp-empty p { font-size: var(--text-sm); margin: 0; }

/* ── Poster ── */
.sl-vp-poster {
  position: relative;
  width: 100%;
  height: 100%;
  cursor: pointer;
  display: block;
}
.sl-vp-poster:focus-visible { outline: none; box-shadow: var(--shadow-focus); }

.sl-vp-thumb {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform var(--duration-normal) var(--ease-out);
}
.sl-vp-poster:hover .sl-vp-thumb { transform: scale(1.03); }

.sl-vp-thumb-fallback {
  width: 100%;
  height: 100%;
}
.sl-vp-thumb-gradient {
  width: 100%;
  height: 100%;
}

/* ── Overlay ── */
.sl-vp-overlay {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.35);
  transition: background-color var(--duration-fast) var(--ease-out);
}
.sl-vp-poster:hover .sl-vp-overlay { background: rgba(0, 0, 0, 0.25); }

.sl-vp-play-btn {
  width: 60px;
  height: 60px;
  border-radius: var(--radius-full);
  background: rgba(255, 255, 255, 0.92);
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #0a0a1a;
  cursor: pointer;
  transition:
    transform var(--duration-fast) var(--ease-spring, cubic-bezier(0.34, 1.56, 0.64, 1)),
    background-color var(--duration-fast) var(--ease-out);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
}
.sl-vp-poster:hover .sl-vp-play-btn {
  transform: scale(1.1);
  background: #fff;
}
.sl-vp-poster:active .sl-vp-play-btn { transform: scale(0.96); }

/* ── Footer ── */
.sl-vp-footer {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: var(--space-3) var(--space-4);
  background: linear-gradient(to top, rgba(0,0,0,0.7) 0%, transparent 100%);
}

.sl-vp-watched {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  color: var(--color-stellar);
  background: rgba(0, 214, 143, 0.15);
  border: 1px solid rgba(0, 214, 143, 0.3);
  border-radius: var(--radius-full);
  padding: 2px var(--space-2);
}

.sl-vp-duration {
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  color: rgba(255, 255, 255, 0.85);
  background: rgba(0, 0, 0, 0.5);
  border-radius: var(--radius-full);
  padding: 2px var(--space-2);
}

/* ── Active frame ── */
.sl-vp-frame-wrap {
  width: 100%;
  height: 100%;
  background: #000;
}
.sl-vp-frame {
  width: 100%;
  height: 100%;
  border: none;
  display: block;
}

/* ── Unsupported ── */
.sl-vp-unsupported {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: var(--space-3);
  height: 100%;
  color: var(--color-comet);
  text-align: center;
  padding: var(--space-6);
}
.sl-vp-unsupported p { font-size: var(--text-sm); margin: 0; }
.sl-vp-link {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1-5);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--color-orbit);
  text-decoration: none;
}
.sl-vp-link:hover { text-decoration: underline; }
</style>

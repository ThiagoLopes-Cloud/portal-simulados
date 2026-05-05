import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUIStore = defineStore('ui', () => {
  const sidebarCollapsed = ref(false)
  const theme = ref('dark')
  const toasts = ref([])

  let toastCounter = 0

  function toggleSidebar() {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }

  function addToast({ message, type = 'info', duration = 4000 }) {
    const id = ++toastCounter
    toasts.value.push({ id, message, type })

    if (toasts.value.length > 4) toasts.value.shift()

    if (duration > 0) {
      setTimeout(() => removeToast(id), duration)
    }
    return id
  }

  function removeToast(id) {
    const idx = toasts.value.findIndex(t => t.id === id)
    if (idx !== -1) toasts.value.splice(idx, 1)
  }

  return { sidebarCollapsed, theme, toasts, toggleSidebar, addToast, removeToast }
})

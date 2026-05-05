import { useUIStore } from '../stores/ui.store.js'

export function useToast() {
  const ui = useUIStore()

  return {
    success: (message, duration) => ui.addToast({ message, type: 'success', duration }),
    error:   (message, duration) => ui.addToast({ message, type: 'error',   duration }),
    warning: (message, duration) => ui.addToast({ message, type: 'warning', duration }),
    info:    (message, duration) => ui.addToast({ message, type: 'info',    duration }),
  }
}

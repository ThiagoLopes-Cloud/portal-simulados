// Orbyn Design System — fundação CSS (ordem importa)
import './assets/styles/tokens.css'
import './assets/styles/base.css'
import './assets/styles/utilities.css'

// Tailwind + SIMUS bridge
import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router/index.js'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')

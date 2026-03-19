// Importa a função createApp do Vue — responsável por criar a aplicação
import { createApp } from 'vue'

// Importa o componente raiz da aplicação
// App.vue é o componente principal que contém todos os outros
import App from './App.vue'

// Importa o router que configuramos
import router from './router/index.js'

// Importa o arquivo de estilos globais
import './style.css'

// Cria a aplicação Vue
// createApp(App) — inicializa o Vue com o componente App como raiz
const app = createApp(App)

// Registra o router na aplicação
// Isso disponibiliza o <router-view> e <router-link> em todos os componentes
app.use(router)

// Monta a aplicação no elemento com id="app" do index.html
// A partir daqui o Vue controla tudo dentro desse elemento
app.mount('#app')
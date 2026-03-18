// Importa o axios — biblioteca para fazer requisições HTTP
import axios from 'axios'

// Cria uma instância do axios com configurações padrão
// baseURL — endereço base da API Django
// Todas as requisições vão usar esse endereço como prefixo
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
})

// Interceptor de requisição — executado antes de cada chamada à API
// Injeta o token JWT automaticamente em todas as requisições
// O aluno não precisa se preocupar com isso — acontece de forma transparente
api.interceptors.request.use((config) => {

  // Busca o token salvo no localStorage do browser
  const token = localStorage.getItem('access_token')

  // Se existir token, adiciona no header Authorization
  // O Django vai ler esse header e identificar o usuário
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

// Interceptor de resposta — executado após cada resposta da API
// Trata erros de autenticação automaticamente
api.interceptors.response.use(
  // Se a resposta for bem sucedida, retorna normalmente
  (response) => response,

  // Se a resposta for um erro, verifica o tipo
  async (error) => {

    // Erro 401 — token expirado ou inválido
    if (error.response?.status === 401) {

      // Remove os tokens inválidos do localStorage
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')

      // Redireciona para a página de login
      window.location.href = '/login'
    }

    return Promise.reject(error)
  }
)

// Exporta a instância do axios configurada
// Todos os outros arquivos vão importar esse 'api' para fazer requisições
export default api
// Importa o axios — biblioteca para fazer requisições HTTP
import axios from 'axios'

// Cria uma instância do axios com configurações padrão
// Em produção usa a URL do Railway, em desenvolvimento usa localhost
const api = axios.create({
  baseURL: 'https://portal-simulados-production.up.railway.app/api',
})

// Interceptor de requisição — executado antes de cada chamada à API
// Injeta o token JWT automaticamente em todas as requisições
api.interceptors.request.use((config) => {

  // Busca o token salvo no localStorage do browser
  const token = localStorage.getItem('access_token')

  // Se existir token, adiciona no header Authorization
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }

  return config
})

// Interceptor de resposta — trata erros de autenticação automaticamente
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

export default api

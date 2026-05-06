import api from './api.js'

export const aulasService = {
  listarTrilhas: () => api.get('/api/aulas/trilhas/'),
  detalharTrilha: (id) => api.get(`/api/aulas/trilhas/${id}/`),
  concluirAula: (id) => api.post(`/api/aulas/aulas/${id}/concluir/`),
  listarMateriais: (params = {}) => api.get('/api/aulas/materiais/', { params }),
}

export const escolasService = {
  listarTurmas: () => api.get('/api/escolas/minhas-turmas/'),
  dashboardTurma: (id) => api.get(`/api/escolas/turmas/${id}/dashboard/`),
}

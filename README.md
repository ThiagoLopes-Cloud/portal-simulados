<div align="center">

# 📝 Portal de Simulados Educacionais

### Projeto Integrador I — Engenharia de Computação
**Universidade Virtual do Estado de São Paulo (UNIVESP) — 4º Semestre**

![Django](https://img.shields.io/badge/Django-6.0-092E20?style=flat&logo=django&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-3.0-4FC08D?style=flat&logo=vue.js&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?style=flat&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-000000?style=flat&logo=jsonwebtokens&logoColor=white)
![CI](https://github.com/ThiagoLopes-Cloud/portal-simulados/actions/workflows/ci.yml/badge.svg)

> Plataforma web educacional desenvolvida para o **Cursinho Preparatório Metamorfose** —
> com foco em simulados do ENEM, correção automática, ranking de alunos e
> potencial de expansão para um mini AVA (Ambiente Virtual de Aprendizagem).

</div>

---

## 🎯 Sobre o Projeto

O **Portal de Simulados** nasceu de uma parceria entre a UNIVESP e o **Cursinho Preparatório Metamorfose**, um curso pré-vestibular que prepara alunos para o ENEM e demais vestibulares.

O objetivo é entregar uma ferramenta gratuita, funcional e escalável que permita aos professores criarem simulados personalizados e aos alunos praticarem com correção automática e acompanhamento de desempenho.

### 🌱 Visão de futuro
Este projeto foi arquitetado para ser escalado futuramente para um **mini AVA completo**, com módulos de aula, materiais de apoio e acompanhamento pedagógico.

---

## ✨ Funcionalidades

- ✅ Cadastro e autenticação de usuários com **JWT**
- ✅ Dois papéis: **Estudante** e **Administrador (Professor)**
- ✅ Criação e gestão de simulados pelo painel admin
- ✅ Questões de múltipla escolha com suporte a **imagens**
- ✅ **Correção automática** com score em percentual
- ✅ **Ranking geral** de alunos por desempenho
- ✅ Interface moderna, limpa e responsiva
- 🔜 Módulos de aula (roadmap futuro)
- 🔜 Upload de materiais de apoio (roadmap futuro)
- 🔜 Relatórios de desempenho por turma (roadmap futuro)

---

## 🏗️ Arquitetura
```
┌─────────────────────┐         ┌──────────────────────┐         ┌─────────────┐
│   Vue.js (SPA)      │  REST   │   Django API          │   ORM   │ PostgreSQL  │
│   porta 5173        │ ──────► │   porta 8000          │ ──────► │             │
│                     │  JSON   │                        │         │             │
└─────────────────────┘         └──────────────────────┘         └─────────────┘
```

**Padrão:** Frontend desacoplado (Vue.js) + Backend API REST (Django)

---

## 🛠️ Tecnologias

| Camada | Tecnologia | Descrição |
|---|---|---|
| Frontend | Vue.js 3 + Vite | SPA reativa e moderna |
| Roteamento | Vue Router 4 | Navegação com guards de autenticação |
| HTTP Client | Axios | Comunicação com a API REST |
| Backend | Django 6 | Framework web Python |
| API REST | Django REST Framework | Serializers, views e autenticação |
| Autenticação | JWT (SimpleJWT) | Tokens de acesso e refresh |
| Banco de dados | PostgreSQL | Banco relacional robusto |
| CI/CD | GitHub Actions | Integração contínua automática |

---

## 📁 Estrutura do projeto
```
portal-simulados/
├── .github/
│   └── workflows/
│       └── ci.yml              # Pipeline de CI automático
├── backend/                    # Django REST API
│   ├── core/                   # Configurações centrais do projeto
│   ├── users/                  # Autenticação e perfis de usuário
│   ├── simulados/              # Criação e listagem de simulados
│   ├── questoes/               # Questões de múltipla escolha
│   ├── respostas/              # Respostas dos estudantes
│   ├── resultados/             # Scores e ranking
│   └── requirements.txt        # Dependências Python
└── frontend/                   # Vue.js SPA
    └── src/
        ├── pages/              # Páginas da aplicação
        │   ├── LoginPage.vue
        │   ├── RegisterPage.vue
        │   ├── DashboardPage.vue
        │   ├── SimuladosPage.vue
        │   ├── ProvaPage.vue
        │   ├── ResultadoPage.vue
        │   └── RankingPage.vue
        ├── router/             # Rotas e navigation guards
        └── services/           # Serviço de API (axios)
```

---

## 🔌 Endpoints da API

| Método | Endpoint | Descrição | Auth |
|---|---|---|---|
| POST | `/api/register/` | Cadastro de novo usuário | ❌ |
| POST | `/api/login/` | Login e geração de token JWT | ❌ |
| GET | `/api/profile/` | Perfil do usuário autenticado | ✅ |
| GET | `/api/simulados/` | Lista simulados disponíveis | ✅ |
| GET | `/api/simulados/{id}/` | Detalhe do simulado com questões | ✅ |
| POST | `/api/responder/` | Envia respostas e calcula score | ✅ |
| GET | `/api/resultados/` | Resultados do aluno autenticado | ✅ |
| GET | `/api/resultados/ranking/` | Ranking geral de alunos | ✅ |

---

## ⚙️ Como rodar localmente

### Pré-requisitos
- Python 3.11+
- Node.js 18+
- PostgreSQL

### 1. Clone o repositório
```bash
git clone https://github.com/ThiagoLopes-Cloud/portal-simulados.git
cd portal-simulados
```

### 2. Configure o Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Crie o arquivo `.env` dentro de `backend/`:
```env
SECRET_KEY=sua-secret-key-aqui
DB_PASSWORD=sua-senha-postgresql
```
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

### 3. Configure o Frontend
```bash
cd frontend
npm install
npm run dev
```

### 4. Acesse o sistema

| Interface | URL |
|---|---|
| Frontend | http://localhost:5173 |
| API Django | http://127.0.0.1:8000 |
| Django Admin | http://127.0.0.1:8000/admin |

---

## 👥 Equipe

Projeto desenvolvido por estudantes do **4º semestre de Engenharia de Computação da UNIVESP**:

| Nome | GitHub |
|---|---|
| Thiago Lopes | [@ThiagoLopes-Cloud](https://github.com/ThiagoLopes-Cloud) |
| 👤 Integrante 2 | — |
| 👤 Integrante 3 | — |
| 👤 Integrante 4 | — |
| 👤 Integrante 5 | — |
| 👤 Integrante 6 | — |
| 👤 Integrante 7 | — |

---

## 🏫 Parceria

<div align="center">

Este projeto foi desenvolvido em parceria com o

### 🦋 Cursinho Preparatório Metamorfose
*Curso pré-vestibular com foco no ENEM*

</div>

---

## 📄 Licença

Projeto acadêmico desenvolvido como **Projeto Integrador I** da UNIVESP.
Desenvolvido com 💜 para democratizar o acesso à educação.
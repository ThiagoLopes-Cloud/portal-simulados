<div align="center">

# 📝 Portal de Simulados Educacionais

### Projeto Integrador I — Engenharia de Computação  
**Universidade Virtual do Estado de São Paulo (UNIVESP) — 4º Semestre**

![Django](https://img.shields.io/badge/Django-6.0-092E20?style=flat&logo=django&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-3.0-4FC08D?style=flat&logo=vue.js&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791?style=flat&logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-000000?style=flat&logo=jsonwebtokens&logoColor=white)
![CI](https://github.com/ThiagoLopes-Cloud/portal-simulados/actions/workflows/ci.yml/badge.svg)

> Plataforma web educacional desenvolvida para o **Cursinho Preparatório Metamorfose**  
> com foco em simulados do ENEM, correção automática, ranking de alunos e  
> potencial de expansão para um mini AVA (Ambiente Virtual de Aprendizagem).

</div>

---

# 📚 Documentação Oficial

## 👨‍🎓 Guia do Usuário

Manual completo da plataforma para estudantes e usuários comuns.

➡️ [Acessar Guia do Usuário](./docs/usuario/README.md)

---

## 👨‍💻 Documentação Técnica

Documentação destinada ao desenvolvimento e manutenção do sistema.

🚧 Em desenvolvimento

---

## 🛠️ Guia Administrativo

Documentação das funcionalidades administrativas da plataforma.

🚧 Em desenvolvimento

---

# 🎯 Sobre o Projeto

O **Portal de Simulados** nasceu de uma parceria entre a UNIVESP e o **Cursinho Preparatório Metamorfose**, um curso pré-vestibular que prepara alunos para o ENEM e demais vestibulares.

O objetivo é entregar uma ferramenta gratuita, funcional e escalável que permita aos professores criarem simulados personalizados e aos alunos praticarem com correção automática e acompanhamento de desempenho.

---

## 🌱 Visão de Futuro

Este projeto foi arquitetado para evoluir futuramente para um **mini AVA completo**, contendo:

- módulos de aula
- trilhas de aprendizagem
- materiais de apoio
- acompanhamento pedagógico
- métricas de desempenho
- relatórios inteligentes

---

# ✨ Funcionalidades

- ✅ Cadastro e autenticação com JWT
- ✅ Dois níveis de acesso: Estudante e Administrador
- ✅ Criação e gerenciamento de simulados
- ✅ Questões com suporte a imagens
- ✅ Correção automática
- ✅ Score percentual
- ✅ Ranking geral de alunos
- ✅ Interface moderna e responsiva
- 🔜 Módulos de aula
- 🔜 Upload de materiais de apoio
- 🔜 Relatórios pedagógicos

---

# 🏗️ Arquitetura

```txt
┌─────────────────────┐         ┌──────────────────────┐         ┌─────────────┐
│   Vue.js (SPA)      │  REST   │   Django API         │   ORM   │ PostgreSQL  │
│   porta 5173        │ ──────► │   porta 8000         │ ──────► │             │
│                     │  JSON   │                      │         │             │
└─────────────────────┘         └──────────────────────┘         └─────────────┘
```

### Padrão Arquitetural

Frontend desacoplado utilizando Vue.js consumindo uma API REST desenvolvida em Django REST Framework.

---

# 🛠️ Tecnologias Utilizadas

| Camada | Tecnologia | Descrição |
|---|---|---|
| Frontend | Vue.js 3 + Vite | SPA moderna e reativa |
| Roteamento | Vue Router 4 | Navegação protegida |
| HTTP Client | Axios | Comunicação com API |
| Backend | Django 6 | Framework web Python |
| API REST | Django REST Framework | Endpoints REST |
| Autenticação | JWT (SimpleJWT) | Controle de sessão |
| Banco de dados | PostgreSQL | Banco relacional |
| CI/CD | GitHub Actions | Integração contínua |

---

# 📁 Estrutura do Projeto

```txt
portal-simulados/
├── .github/
│   └── workflows/
│       └── ci.yml
│
├── docs/
│   ├── usuario/
│   │   └── README.md
│   │
│   └── assets/
│       └── screenshots/
│
├── backend/
│   ├── core/
│   ├── users/
│   ├── simulados/
│   ├── questoes/
│   ├── respostas/
│   ├── resultados/
│   └── requirements.txt
│
├── frontend/
│   └── src/
│       ├── pages/
│       ├── router/
│       └── services/
│
└── README.md
```

---

# 🔌 Endpoints da API

| Método | Endpoint | Descrição | Auth |
|---|---|---|---|
| POST | `/api/register/` | Cadastro de usuário | ❌ |
| POST | `/api/login/` | Login JWT | ❌ |
| GET | `/api/profile/` | Perfil autenticado | ✅ |
| GET | `/api/simulados/` | Lista simulados | ✅ |
| GET | `/api/simulados/{id}/` | Detalhes do simulado | ✅ |
| POST | `/api/responder/` | Envio de respostas | ✅ |
| GET | `/api/resultados/` | Histórico do aluno | ✅ |
| GET | `/api/resultados/ranking/` | Ranking geral | ✅ |

---

# ⚙️ Como Executar Localmente

## Pré-requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL

---

## 1. Clonar o repositório

```bash
git clone https://github.com/ThiagoLopes-Cloud/portal-simulados.git
cd portal-simulados
```

---

## 2. Configurar Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Criar arquivo `.env`

```env
SECRET_KEY=sua-secret-key-aqui
DB_PASSWORD=sua-senha-postgresql
```

### Executar migrations

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

---

## 3. Configurar Frontend

```bash
cd frontend
npm install
npm run dev
```

---

## 4. Acessar Plataforma

| Interface | URL |
|---|---|
| Frontend | http://localhost:5173 |
| API Django | http://127.0.0.1:8000 |
| Django Admin | http://127.0.0.1:8000/admin |

---

# 👥 Equipe

Projeto desenvolvido por estudantes do **4º semestre de Engenharia de Computação da UNIVESP**.

| Integrante | Função |
|---|---|
| Thiago Lopes | integrante do projeto|
| Thaline | Integrante do Projeto |
| Leonardo | Integrante do Projeto |
| Caroline | Integrante do Projeto |
| Eder | Integrante do Projeto |
| Ellen | Integrante do Projeto |

---

# 🏫 Parceria

<div align="center">

Projeto desenvolvido em parceria com o

## 🦋 Cursinho Preparatório Metamorfose

Curso preparatório com foco no ENEM e vestibulares.

</div>

---

# 📄 Licença

Projeto acadêmico desenvolvido como Projeto Integrador I da UNIVESP.

Desenvolvido com 💜 para democratizar o acesso à educação.
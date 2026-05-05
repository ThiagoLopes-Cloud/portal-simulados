# SimusLab — Checklist de Conclusão do Projeto

> Gerado em 2026-05-05. Atualizado conforme implementações avançam.

---

## ✅ Concluído — Sessão Atual (2026-05-05)

- [x] **Bug: login não retorna `role`** — `CustomTokenObtainPairView` retorna `access` + `refresh` + `role` + `username`. LoginPage salva `username` no localStorage.
- [x] **Bug: sem refresh token** — interceptor do axios com fila de requisições, tenta renovar antes de logout. Sessões agora persistem enquanto o refresh for válido.
- [x] **Bug: aluno não vê suas turmas** — `TurmasAlunoOuProfessorView` em `GET /api/escolas/minhas-turmas/` serve admin e aluno corretamente. Rota dedicada `GET /api/escolas/minhas-turmas-aluno/` também adicionada.
- [x] **Segurança: auto-registro como admin** — `RegisterSerializer` removeu `role` dos campos aceitos. `create()` força `role='student'`.
- [x] **RegisterPage** → migrada para `AuthLayout` + `OrbynInput` + `OrbynButton`
- [x] **SimuladosPage** → migrada para `DashboardLayout`, sidebar duplicada removida
- [x] **ProvaPage** → tokens `simus-*` substituídos por CSS vars Orbyn, layout focus mantido
- [x] **ResultadoPage** → migrada para `DashboardLayout` + tema dark completo + `EvolucaoGrafico` integrado
- [x] **RankingPage** → migrada para `DashboardLayout`, sidebar duplicada removida
- [x] **TurmaPortal** → migrada para `DashboardLayout` + modal de criação de turma (admin) + endpoint correto
- [x] **AdminAlunosPage** → migrada para `DashboardLayout`, tema dark completo
- [x] **AdminAlunoDashboardPage** → migrada para `DashboardLayout`, tema dark completo
- [x] **ImportarQuestoesPage** → migrada para `DashboardLayout`, tema dark completo, PROMPT_COMPLETO preservado
- [x] **Página 404** — `NotFoundPage.vue` + rota `/:pathMatch(.*)*` no router
- [x] **Criação de turmas pelo admin** — `POST /api/escolas/turmas/` + modal no TurmaPortal
- [x] **Build de produção** — `npm run build` zero erros, 2.45s ✓

---

## 🟡 Médio — Features incompletas (ainda pendentes)

- [ ] **Simulados por turma** — aba "Missões de Turma" em `SimuladosPage` não busca simulados das turmas do aluno. Falta endpoint no backend `GET /api/simulados/` filtrado por turmas do aluno (campo `exclusivos`).
- [ ] **MaterialEstudo via frontend** — recomendações de estudo só cadastráveis via Django Admin. Falta seção no `ImportarQuestoesPage` ou página dedicada.

---

## 🔵 Segurança

- [ ] **CORS de produção** — `CORS_ALLOW_ALL_ORIGINS = True` está ativo. Após deploy definitivo no Vercel, trocar por `CORS_ALLOWED_ORIGINS` com o domínio exato.

---

## ✅ Concluído — Sessão Anterior (2026-05-05)

- [x] **Orbyn Design System — Fase 2** — tokens.css (60+ vars), base.css (reset + keyframes), utilities.css, Google Fonts (Syne + DM Sans + JetBrains Mono) no index.html
- [x] **Orbyn Design System — Fase 3** — OrbynLogo, OrbynButton (4 variantes + spinner), OrbynInput (v-model + estados), OrbynCard (slots + accent), OrbynBadge (6 variantes + dot), OrbynKPICard (skeleton + direção)
- [x] **Orbyn Design System — Fase 4** — OrbynTopbar (sticky blur + avatar), OrbynSidebar (collapsible + v-show), OrbynModal (Teleport + Esc), OrbynToast (slide-in + empilha 4)
- [x] **Orbyn Design System — Fase 5** — Pinia instalado + ui.store (sidebarCollapsed, toasts, toggleSidebar)
- [x] **Orbyn Design System — Fase 6** — AuthLayout (split panel + starfield), DashboardLayout (Topbar + Sidebar + mobile nav + Toast)
- [x] **LoginPage** — migrada para AuthLayout + OrbynInput + OrbynButton + OrbynLogo
- [x] **DashboardPage** — migrada para DashboardLayout + OrbynKPICard + OrbynCard + saudação dinâmica + data pt-BR
- [x] **useToast composable** — success / error / warning / info
- [x] **Bug: `vertical-align-middle` inválido no RankingPage** — corrigido para CSS inline
- [x] **Build de produção** — `npm run build` zero erros ✓

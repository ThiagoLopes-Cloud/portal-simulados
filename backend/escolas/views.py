# escolas/views.py
from datetime import timedelta

from django.db.models import Avg, Count
from django.utils import timezone
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Turma


class EntrarNaTurmaView(views.APIView):
    """
    POST /api/escolas/entrar/
    { "codigo": "ABC-123" }
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        codigo = request.data.get("codigo", "").strip().upper()

        try:
            turma = Turma.objects.get(codigo_convite=codigo)

            # Verifica se o aluno já está na turma
            if turma.alunos.filter(id=request.user.id).exists():
                return Response(
                    {"error": "Já estás matriculado nesta turma."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            turma.alunos.add(request.user)
            return Response(
                {
                    "message": f"Sucesso! Agora fazes parte da turma: {turma.nome}",
                    "turma": turma.nome,
                },
                status=status.HTTP_200_OK,
            )

        except Turma.DoesNotExist:
            return Response(
                {"error": "Código de convite inválido."},
                status=status.HTTP_404_NOT_FOUND,
            )


class TurmasAlunoView(views.APIView):
    """GET /api/escolas/minhas-turmas-aluno/ — turmas em que o aluno está matriculado."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        turmas = Turma.objects.filter(alunos=request.user).prefetch_related("alunos")
        data = [
            {
                "id": t.id,
                "nome": t.nome,
                "codigo": t.codigo_convite,
                "total_alunos": t.alunos.count(),
            }
            for t in turmas
        ]
        return Response(data)


class TurmasAlunoOuProfessorView(views.APIView):
    """GET /api/escolas/minhas-turmas/ — compatibilidade: admin vê turmas que criou, aluno vê turmas que entrou."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role == "admin":
            turmas = Turma.objects.filter(professor=request.user).prefetch_related("alunos")
        else:
            turmas = Turma.objects.filter(alunos=request.user).prefetch_related("alunos")
        data = [
            {
                "id": t.id,
                "nome": t.nome,
                "codigo": t.codigo_convite,
                "total_alunos": t.alunos.count(),
            }
            for t in turmas
        ]
        return Response(data)


class TurmasAdminCreateView(views.APIView):
    """POST /api/escolas/turmas/ — admin cria uma nova turma."""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "admin":
            return Response({"error": "Acesso restrito."}, status=status.HTTP_403_FORBIDDEN)

        nome = request.data.get("nome", "").strip()
        if not nome:
            return Response({"error": "Nome da turma é obrigatório."}, status=status.HTTP_400_BAD_REQUEST)

        import secrets, string
        codigo = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        turma = Turma.objects.create(nome=nome, professor=request.user, codigo_convite=codigo)
        return Response(
            {"id": turma.id, "nome": turma.nome, "codigo": turma.codigo_convite},
            status=status.HTTP_201_CREATED,
        )


class TurmaDashboardView(views.APIView):
    """GET /api/escolas/turmas/{id}/dashboard/ — dashboard de batalha da turma."""

    permission_classes = [IsAuthenticated]

    def get(self, request, turma_id):
        from resultados.models import Resultado
        from respostas.models import Resposta
        from conteudo.models import Materia

        try:
            turma = Turma.objects.prefetch_related("alunos").get(pk=turma_id)
        except Turma.DoesNotExist:
            return Response({"error": "Turma não encontrada."}, status=404)

        is_admin = request.user.role == "admin"
        is_membro = turma.alunos.filter(id=request.user.id).exists()
        if not is_admin and not is_membro:
            return Response({"error": "Acesso restrito."}, status=403)

        aluno_ids = list(turma.alunos.values_list("id", flat=True))

        # Média de score da turma
        media_score = (
            Resultado.objects.filter(aluno_id__in=aluno_ids)
            .aggregate(media=Avg("score"))["media"]
            or 0
        )

        # Simulados feitos na última semana
        uma_semana_atras = timezone.now() - timedelta(days=7)
        simulados_semana = Resultado.objects.filter(
            aluno_id__in=aluno_ids, realizado_em__gte=uma_semana_atras
        ).count()

        # Total de questões respondidas na semana (para microcopy motivacional)
        questoes_semana = Resposta.objects.filter(
            aluno_id__in=aluno_ids, respondido_em__gte=uma_semana_atras
        ).count()

        # Top 3 alunos por média de score
        top_alunos = list(
            Resultado.objects.filter(aluno_id__in=aluno_ids)
            .values("aluno__id", "aluno__username", "aluno__first_name")
            .annotate(media=Avg("score"), total_simulados=Count("id"))
            .order_by("-media")[:3]
        )

        # Radar: performance por matéria (forças e fraquezas)
        radar_data = []
        for materia in Materia.objects.all():
            respostas = Resposta.objects.filter(
                aluno_id__in=aluno_ids, questao__tema__materia=materia
            )
            total = respostas.count()
            if total > 0:
                corretas = respostas.filter(correta=True).count()
                radar_data.append(
                    {
                        "materia": materia.nome,
                        "percentual": round((corretas / total) * 100, 1),
                    }
                )

        # Barras: produtividade semanal (últimas 7 semanas)
        weekly_data = []
        for i in range(6, -1, -1):
            semana_inicio = timezone.now() - timedelta(weeks=i + 1)
            semana_fim = semana_inicio + timedelta(weeks=1)
            count = Resultado.objects.filter(
                aluno_id__in=aluno_ids,
                realizado_em__gte=semana_inicio,
                realizado_em__lt=semana_fim,
            ).count()
            weekly_data.append(
                {"semana": semana_inicio.strftime("%d/%m"), "simulados": count}
            )

        return Response(
            {
                "turma": {
                    "id": turma.id,
                    "nome": turma.nome,
                    "total_alunos": turma.alunos.count(),
                    "codigo": turma.codigo_convite,
                },
                "media_score": round(float(media_score), 1),
                "simulados_semana": simulados_semana,
                "questoes_semana": questoes_semana,
                "top_alunos": top_alunos,
                "radar_data": radar_data,
                "weekly_data": weekly_data,
            }
        )


class TurmasProfessorView(views.APIView):
    """Retorna as turmas que o professor gerencia com estatísticas básicas."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "admin":
            return Response(
                {"error": "Acesso restrito."}, status=status.HTTP_403_FORBIDDEN
            )

        turmas = Turma.objects.filter(professor=request.user).prefetch_related("alunos")
        data = [
            {
                "id": t.id,
                "nome": t.nome,
                "codigo": t.codigo_convite,
                "total_alunos": t.alunos.count(),
            }
            for t in turmas
        ]

        return Response(data)

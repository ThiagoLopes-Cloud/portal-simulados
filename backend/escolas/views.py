# escolas/views.py
from rest_framework import status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
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

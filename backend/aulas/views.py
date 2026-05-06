from django.utils import timezone
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Aula, Material, ProgressoAluno, Trilha
from .serializers import MaterialSerializer, TrilhaDetalheSerializer, TrilhaListSerializer


class TrilhasListView(views.APIView):
    """GET /api/aulas/trilhas/ — lista todas as trilhas com progresso do aluno."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        trilhas = Trilha.objects.prefetch_related("modulos__aulas").all()
        serializer = TrilhaListSerializer(trilhas, many=True, context={"request": request})
        return Response(serializer.data)


class TrilhaDetalheView(views.APIView):
    """GET /api/aulas/trilhas/{id}/ — detalhe completo da trilha com módulos e aulas."""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            trilha = Trilha.objects.prefetch_related(
                "modulos__aulas__materiais", "modulos__materiais"
            ).get(pk=pk)
        except Trilha.DoesNotExist:
            return Response({"error": "Trilha não encontrada."}, status=404)

        serializer = TrilhaDetalheSerializer(trilha, context={"request": request})
        return Response(serializer.data)


class ConcluirAulaView(views.APIView):
    """POST /api/aulas/aulas/{id}/concluir/ — marca uma aula como concluída."""

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            aula = Aula.objects.get(pk=pk)
        except Aula.DoesNotExist:
            return Response({"error": "Aula não encontrada."}, status=404)

        progresso, created = ProgressoAluno.objects.get_or_create(
            aluno=request.user,
            aula=aula,
            defaults={"is_completed": True, "concluido_em": timezone.now()},
        )

        if not created and not progresso.is_completed:
            progresso.is_completed = True
            progresso.concluido_em = timezone.now()
            progresso.save()

        # Calcula XP ganho (base: 10xp por aula + bônus por sequência)
        xp_ganho = 10
        try:
            perfil = request.user.perfil
            perfil.registrar_atividade(xp_ganho)
        except Exception:
            pass

        # Verifica se o módulo inteiro foi concluído
        modulo = aula.modulo
        total_no_modulo = modulo.aulas.count()
        concluidas_no_modulo = ProgressoAluno.objects.filter(
            aluno=request.user,
            aula__modulo=modulo,
            is_completed=True,
        ).count()
        modulo_completo = total_no_modulo > 0 and concluidas_no_modulo == total_no_modulo

        return Response(
            {
                "success": True,
                "xp_ganho": xp_ganho,
                "modulo_completo": modulo_completo,
                # SUGESTÃO: disparar confete aqui no frontend quando modulo_completo=True
                # SUGESTÃO: exibir animação "+10 XP" flutuante quando xp_ganho > 0
            },
            status=status.HTTP_200_OK,
        )


class MateriaisView(views.APIView):
    """GET /api/aulas/materiais/?modulo={id}&aula={id} — lista materiais de apoio."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = Material.objects.all()
        modulo_id = request.query_params.get("modulo")
        aula_id = request.query_params.get("aula")

        if modulo_id:
            qs = qs.filter(modulo_id=modulo_id)
        if aula_id:
            qs = qs.filter(aula_id=aula_id)

        serializer = MaterialSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)

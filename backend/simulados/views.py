# simulados/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Simulado

# AQUI ESTÁ A CORREÇÃO: Importamos os nomes exatos que estão no seu arquivo
from .serializers import SimuladoListSerializer, SimuladoDetalheSerializer


class SimuladoListView(APIView):
    """Retorna a lista de simulados dividida entre globais e exclusivos da turma."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # 1. Pega os simulados abertos para todos (que não estão em nenhuma turma)
        globais = Simulado.objects.filter(turmas__isnull=True).order_by("-criado_em")

        # 2. Pega os simulados exclusivos (vinculados às turmas que o aluno faz parte)
        exclusivos = (
            Simulado.objects.filter(turmas__alunos=request.user)
            .order_by("-criado_em")
            .distinct()
        )

        # Transforma em JSON usando o serializer correto de Listagem
        serializer_globais = SimuladoListSerializer(globais, many=True)
        serializer_exclusivos = SimuladoListSerializer(exclusivos, many=True)

        # Devolve as duas listas separadas para o Frontend
        return Response(
            {
                "globais": serializer_globais.data,
                "exclusivos": serializer_exclusivos.data,
            },
            status=status.HTTP_200_OK,
        )


class SimuladoDetalheView(APIView):
    """Retorna os detalhes de um simulado específico (tela de prova)."""

    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            # Busca o simulado pelo ID
            simulado = Simulado.objects.get(pk=pk)
            # Usa o serializer de Detalhe para puxar todas as questões junto
            serializer = SimuladoDetalheSerializer(simulado)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Simulado.DoesNotExist:
            return Response(
                {"error": "Simulado não encontrado."}, status=status.HTTP_404_NOT_FOUND
            )

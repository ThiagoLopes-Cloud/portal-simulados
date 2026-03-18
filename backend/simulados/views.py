# Importa o módulo de views do Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Importa a permissão que permite acesso sem autenticação
from rest_framework.permissions import AllowAny

# Importa os serializers de simulado
from .serializers import SimuladoListSerializer, SimuladoDetalheSerializer

# Importa o model Simulado
from .models import Simulado

class SimuladoListView(APIView):
    """
    View de listagem de simulados disponíveis.
    Rota: GET /api/simulados
    Requer autenticação — só alunos logados podem ver os simulados.
    """

    def get(self, request):
        """
        Retorna a lista de todos os simulados ativos.
        Usado na tela de lista de simulados do Vue.js.
        """

        # Busca todos os simulados ativos no banco de dados
        # filter(ativo=True) — retorna apenas os simulados ativos
        simulados = Simulado.objects.filter(ativo=True)

        # Serializa a lista de simulados
        # many=True indica que são múltiplos objetos
        serializer = SimuladoListSerializer(simulados, many=True)

        # Retorna a lista de simulados com status 200 (OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SimuladoDetalheView(APIView):
    """
    View de detalhe de um simulado específico com suas questões.
    Rota: GET /api/simulados/{id}
    Requer autenticação — só alunos logados podem ver o simulado.
    """

    def get(self, request, pk):
        """
        Retorna os dados completos de um simulado com todas as questões.
        O 'pk' é o ID do simulado passado na URL.
        Usado na tela de prova do Vue.js.
        """

        try:
            # Busca o simulado pelo ID — retorna erro se não encontrar
            # pk vem da URL ex: /api/simulados/1
            simulado = Simulado.objects.get(pk=pk, ativo=True)

        except Simulado.DoesNotExist:
            # Retorna erro 404 se o simulado não existir ou não estiver ativo
            return Response(
                {'error': 'Simulado não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serializa o simulado com todas as questões
        serializer = SimuladoDetalheSerializer(simulado)

        # Retorna os dados do simulado com status 200 (OK)
        return Response(serializer.data, status=status.HTTP_200_OK)
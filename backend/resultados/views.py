# Importa o módulo de views do Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Importa os serializers de resultado
from .serializers import ResultadoSerializer, RankingSerializer

# Importa o model Resultado
from .models import Resultado

class ResultadoListView(APIView):
    """
    View para o aluno ver seus próprios resultados.
    Rota: GET /api/resultados
    Requer autenticação — cada aluno vê apenas seus próprios resultados.
    """

    def get(self, request):
        """
        Retorna todos os resultados do aluno autenticado.
        Usado na tela de histórico de resultados do Vue.js.
        """

        # Filtra os resultados apenas do aluno autenticado
        # request.user é preenchido automaticamente pelo JWT
        resultados = Resultado.objects.filter(aluno=request.user)

        # Serializa a lista de resultados
        serializer = ResultadoSerializer(resultados, many=True)

        # Retorna a lista de resultados com status 200 (OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResultadoDetalheView(APIView):
    """
    View para o aluno ver o detalhe de um resultado específico.
    Rota: GET /api/resultados/{id}
    Requer autenticação — o aluno só pode ver seus próprios resultados.
    """

    def get(self, request, pk):
        """
        Retorna o detalhe de um resultado específico do aluno.
        O 'pk' é o ID do resultado passado na URL.
        """

        try:
            # Busca o resultado pelo ID e pelo aluno autenticado
            # Garante que o aluno só acessa seus próprios resultados
            resultado = Resultado.objects.get(pk=pk, aluno=request.user)

        except Resultado.DoesNotExist:
            # Retorna erro 404 se o resultado não existir
            return Response(
                {'error': 'Resultado não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serializa o resultado
        serializer = ResultadoSerializer(resultado)

        # Retorna o resultado com status 200 (OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RankingView(APIView):
    """
    View para exibir o ranking de alunos por score.
    Rota: GET /api/ranking
    Requer autenticação — só alunos logados podem ver o ranking.
    """

    def get(self, request):
        """
        Retorna o ranking de todos os alunos ordenado por score.
        Usado na tela de ranking do Vue.js.
        """

        # Busca todos os resultados ordenados por score decrescente
        # '-score' — o sinal '-' indica ordem decrescente (maior score primeiro)
        resultados = Resultado.objects.all().order_by('-score')

        # Serializa a lista de resultados para o ranking
        serializer = RankingSerializer(resultados, many=True)

        # Retorna o ranking com status 200 (OK)
        return Response(serializer.data, status=status.HTTP_200_OK)
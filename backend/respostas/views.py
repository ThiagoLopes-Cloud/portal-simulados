# Importa o módulo de views do Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Importa os serializers de resposta
from .serializers import ResponderSerializer

# Importa os models necessários
from .models import Resposta
from questoes.models import Questao
from simulados.models import Simulado
from resultados.models import Resultado

class ResponderView(APIView):
    """
    View para o aluno enviar as respostas de um simulado.
    Rota: POST /api/responder
    Requer autenticação — só alunos logados podem responder.

    Fluxo:
    1. Recebe o id do simulado e a lista de respostas
    2. Valida os dados
    3. Salva cada resposta no banco
    4. Calcula o score automaticamente
    5. Salva o resultado
    6. Retorna o resultado para o Vue.js
    """

    def post(self, request):
        """
        Recebe as respostas do aluno e calcula o score automaticamente.
        """

        # Passa os dados recebidos para o serializer validar
        serializer = ResponderSerializer(data=request.data)

        # Verifica se os dados são válidos
        if not serializer.is_valid():
            # Retorna os erros de validação com status 400 (Bad Request)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extrai os dados validados
        simulado_id = serializer.validated_data['simulado_id']
        respostas_data = serializer.validated_data['respostas']

        try:
            # Busca o simulado pelo ID
            simulado = Simulado.objects.get(pk=simulado_id, ativo=True)

        except Simulado.DoesNotExist:
            # Retorna erro 404 se o simulado não existir
            return Response(
                {'error': 'Simulado não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Verifica se o aluno já respondeu esse simulado anteriormente
        if Resultado.objects.filter(aluno=request.user, simulado=simulado).exists():
            return Response(
                {'error': 'Você já respondeu esse simulado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Inicializa o contador de acertos
        acertos = 0

        # Lista para armazenar as respostas salvas
        respostas_salvas = []

        # Percorre cada resposta enviada pelo aluno
        for resposta_item in respostas_data:
            try:
                # Busca a questão pelo ID — verifica se pertence ao simulado
                questao = Questao.objects.get(
                    pk=resposta_item['questao_id'],
                    simulado=simulado
                )

            except Questao.DoesNotExist:
                # Retorna erro se a questão não pertencer ao simulado
                return Response(
                    {'error': f'Questão {resposta_item["questao_id"]} não encontrada.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Verifica se a resposta do aluno está correta
            # Compara a opção escolhida com a resposta correta da questão
            correta = resposta_item['opcao_escolhida'] == questao.resposta_correta

            # Incrementa o contador de acertos se a resposta estiver correta
            if correta:
                acertos += 1

            # Salva a resposta no banco de dados
            resposta = Resposta.objects.create(
                aluno=request.user,       # Usuário autenticado via JWT
                questao=questao,          # Questão respondida
                opcao_escolhida=resposta_item['opcao_escolhida'],  # Opção escolhida
                correta=correta           # True se correta, False se errada
            )

            respostas_salvas.append(resposta)

        # Calcula o total de questões do simulado
        total_questoes = simulado.questoes.count()

        # Calcula o score em percentual
        # ex: 8 acertos em 10 questões = 80.00%
        score = (acertos / total_questoes * 100) if total_questoes > 0 else 0

        # Salva o resultado final no banco de dados
        resultado = Resultado.objects.create(
            aluno=request.user,           # Usuário autenticado
            simulado=simulado,            # Simulado respondido
            acertos=acertos,              # Total de acertos
            total_questoes=total_questoes,# Total de questões
            score=round(score, 2)         # Score arredondado para 2 casas decimais
        )

        # Retorna o resultado para o Vue.js com status 201 (Created)
        return Response({
            'message': 'Simulado respondido com sucesso!',
            'resultado': {
                'simulado': simulado.titulo,
                'acertos': acertos,
                'total_questoes': total_questoes,
                'score': f'{score:.2f}%',
            }
        }, status=status.HTTP_201_CREATED)
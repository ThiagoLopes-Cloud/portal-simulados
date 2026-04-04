# Importa o módulo de views do Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Importa transaction para garantir atomicidade
from django.db import transaction

# Importa os serializers de resposta
from .serializers import ResponderSerializer

# Importa os models necessários
from .models import Resposta
from simulados.models import Simulado, SimuladoQuestao
from resultados.models import Resultado


class ResponderView(APIView):
    """
    POST /api/responder/

    Recebe as respostas do aluno, corrige automaticamente,
    salva as respostas e cria o Resultado.

    Retorna o resultado com resultado_id — necessário para
    o frontend redirecionar para /resultado/{id}/gabarito/
    (Fase 5: gabarito comentado)

    Fluxo:
    1. Valida o JSON recebido
    2. Busca o simulado
    3. Verifica se o aluno já respondeu
    4. Para cada resposta: valida questão via SimuladoQuestao,
       compara com gabarito, acumula acertos
    5. bulk_create das respostas — 1 query para N respostas
    6. Cria o Resultado
    7. Tudo dentro de transaction.atomic() — falha = rollback total
    """

    def post(self, request):

        # Valida o JSON recebido
        serializer = ResponderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        simulado_id    = serializer.validated_data['simulado_id']
        respostas_data = serializer.validated_data['respostas']

        # Busca o simulado
        try:
            simulado = Simulado.objects.get(pk=simulado_id, ativo=True)
        except Simulado.DoesNotExist:
            return Response(
                {'error': 'Simulado não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Verifica se o aluno já respondeu esse simulado
        if Resultado.objects.filter(aluno=request.user, simulado=simulado).exists():
            return Response(
                {'error': 'Você já respondeu esse simulado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Busca todas as questões do simulado via SimuladoQuestao
        # Monta dict {questao_id: Questao} para validação eficiente
        questoes_do_simulado = {
            sq.questao_id: sq.questao
            for sq in SimuladoQuestao.objects.select_related('questao').filter(
                simulado=simulado
            )
        }

        # Valida todas as respostas antes de salvar qualquer coisa
        # Evita salvar respostas parciais se houver questão inválida
        for item in respostas_data:
            if item['questao_id'] not in questoes_do_simulado:
                return Response(
                    {'error': f'Questão {item["questao_id"]} não pertence a este simulado.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # --------------------------------------------------------
        # Processa respostas e cria Resultado dentro de uma transação
        # Se qualquer passo falhar, tudo é revertido (atomicidade)
        # --------------------------------------------------------
        with transaction.atomic():

            acertos = 0
            respostas_para_criar = []

            for item in respostas_data:
                questao = questoes_do_simulado[item['questao_id']]

                # Compara a opção escolhida com a resposta correta
                correta = item['opcao_escolhida'] == questao.resposta_correta

                if correta:
                    acertos += 1

                # Prepara o objeto Resposta para bulk_create
                # simulado incluído — necessário para unique_together [aluno, questao, simulado]
                respostas_para_criar.append(
                    Resposta(
                        aluno=request.user,
                        questao=questao,
                        simulado=simulado,
                        opcao_escolhida=item['opcao_escolhida'],
                        correta=correta,
                    )
                )

            # Salva todas as respostas de uma vez — muito mais eficiente que N inserts
            Resposta.objects.bulk_create(respostas_para_criar)

            # Calcula o total de questões e o score
            total_questoes = len(questoes_do_simulado)
            score = round((acertos / total_questoes * 100), 2) if total_questoes > 0 else 0

            # Cria o Resultado final
            resultado = Resultado.objects.create(
                aluno=request.user,
                simulado=simulado,
                acertos=acertos,
                total_questoes=total_questoes,
                score=score,
            )

        # Retorna com resultado_id para o frontend redirecionar
        # para /resultado/{id} onde buscará o gabarito completo
        return Response({
            'message': 'Simulado respondido com sucesso!',
            'resultado': {
                'resultado_id':   resultado.id,    # ← NOVO: ID do resultado
                'simulado':       simulado.titulo,
                'acertos':        acertos,
                'total_questoes': total_questoes,
                'score':          f'{score:.2f}%',
            }
        }, status=status.HTTP_201_CREATED)
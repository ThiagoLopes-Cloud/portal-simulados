# respostas/views.py
# View de envio de respostas ajustada para o novo relacionamento M2M.
# A validação agora verifica se a questão está vinculada ao simulado
# via tabela intermediária SimuladoQuestao — não mais por ForeignKey direto.

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ResponderSerializer
from .models import Resposta
from questoes.models import Questao
from simulados.models import Simulado, SimuladoQuestao
from resultados.models import Resultado


class ResponderView(APIView):
    """
    View para o aluno enviar todas as respostas de um simulado de uma vez.
    Rota: POST /api/responder/
    
    Fluxo:
    1. Valida payload (simulado_id + lista de respostas)
    2. Verifica se o simulado existe e está ativo
    3. Bloqueia reenvio (aluno já respondeu esse simulado)
    4. Para cada resposta: valida se a questão pertence ao simulado
    5. Salva a resposta e verifica se está correta
    6. Calcula score e salva Resultado
    7. Retorna resultado ao Vue.js
    """

    def post(self, request):
        serializer = ResponderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        simulado_id = serializer.validated_data['simulado_id']
        respostas_data = serializer.validated_data['respostas']

        # Busca o simulado ativo
        try:
            simulado = Simulado.objects.get(pk=simulado_id, ativo=True)
        except Simulado.DoesNotExist:
            return Response(
                {'error': 'Simulado não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Bloqueia reenvio — cada aluno responde cada simulado uma vez
        if Resultado.objects.filter(aluno=request.user, simulado=simulado).exists():
            return Response(
                {'error': 'Você já respondeu esse simulado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Carrega todas as questões do simulado em memória (1 query) —
        # evita N queries dentro do loop de validação.
        # O dict mapeia questao_id → SimuladoQuestao para acesso O(1).
        questoes_do_simulado = {
            sq.questao_id: sq.questao
            for sq in SimuladoQuestao.objects.filter(simulado=simulado)
                                             .select_related('questao')
        }

        acertos = 0
        respostas_para_criar = []   # Acumula para bulk_create no final

        for resposta_item in respostas_data:
            questao_id = resposta_item['questao_id']

            # Valida se a questão pertence a este simulado
            if questao_id not in questoes_do_simulado:
                return Response(
                    {'error': f'Questão {questao_id} não pertence a este simulado.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            questao = questoes_do_simulado[questao_id]
            opcao_escolhida = resposta_item['opcao_escolhida']
            correta = opcao_escolhida == questao.resposta_correta

            if correta:
                acertos += 1

            # Acumula para inserção em lote — muito mais eficiente que
            # criar uma por uma dentro do loop (evita N inserts individuais)
            respostas_para_criar.append(
                Resposta(
                    aluno=request.user,
                    questao=questao,
                    opcao_escolhida=opcao_escolhida,
                    correta=correta,
                )
            )

        # Insere todas as respostas em uma única query SQL — performance crítica
        Resposta.objects.bulk_create(respostas_para_criar)

        # Calcula score
        total_questoes = len(questoes_do_simulado)
        score = round((acertos / total_questoes * 100), 2) if total_questoes > 0 else 0

        # Salva o resultado final
        Resultado.objects.create(
            aluno=request.user,
            simulado=simulado,
            acertos=acertos,
            total_questoes=total_questoes,
            score=score,
        )

        return Response({
            'message': 'Simulado respondido com sucesso!',
            'resultado': {
                'simulado': simulado.titulo,
                'acertos': acertos,
                'total_questoes': total_questoes,
                'score': f'{score:.2f}%',
            }
        }, status=status.HTTP_201_CREATED)
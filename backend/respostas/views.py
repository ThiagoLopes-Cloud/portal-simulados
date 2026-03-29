# respostas/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ResponderSerializer
from .models import Resposta
from simulados.models import Simulado, SimuladoQuestao
from resultados.models import Resultado


class ResponderView(APIView):
    """
    Recebe as respostas do aluno e calcula o score.
    Rota: POST /api/responder/
    """

    def post(self, request):
        serializer = ResponderSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        simulado_id = serializer.validated_data['simulado_id']
        respostas_data = serializer.validated_data['respostas']

        try:
            simulado = Simulado.objects.get(pk=simulado_id, ativo=True)
        except Simulado.DoesNotExist:
            return Response(
                {'error': 'Simulado não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if Resultado.objects.filter(aluno=request.user, simulado=simulado).exists():
            return Response(
                {'error': 'Você já respondeu esse simulado.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Carrega questões do simulado em memória — 1 query com JOIN
        questoes_do_simulado = {
            sq.questao_id: sq.questao
            for sq in SimuladoQuestao.objects
                .filter(simulado=simulado)
                .select_related('questao')
        }

        acertos = 0
        respostas_para_criar = []

        for resposta_item in respostas_data:
            questao_id = resposta_item['questao_id']

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

            respostas_para_criar.append(
                Resposta(
                    aluno=request.user,
                    questao=questao,
                    simulado=simulado,  # ← salva o simulado na resposta
                    opcao_escolhida=opcao_escolhida,
                    correta=correta,
                )
            )

        # 1 query para inserir todas as respostas
        Resposta.objects.bulk_create(respostas_para_criar)

        total_questoes = len(questoes_do_simulado)
        score = round((acertos / total_questoes * 100), 2) if total_questoes > 0 else 0

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
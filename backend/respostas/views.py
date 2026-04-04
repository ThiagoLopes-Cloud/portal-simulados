# respostas/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db import transaction

from .serializers import ResponderSerializer
from .models import Resposta
from simulados.models import Simulado, SimuladoQuestao
from resultados.models import Resultado


class ResponderView(APIView):
    """
    POST /api/responder/

    Recebe as respostas do aluno, corrige automaticamente e cria o Resultado.

    Fase 6 — múltiplas tentativas:
    - Remove o bloqueio de "já respondeu este simulado"
    - Calcula automaticamente o número da tentativa (1ª, 2ª, 3ª vez...)
    - Salva o número da tentativa em Resultado e em cada Resposta
    - O histórico de evolução fica disponível via GET /api/resultados/dashboard/

    Fluxo:
    1. Valida o JSON
    2. Busca o simulado
    3. Calcula qual é a próxima tentativa para este aluno neste simulado
    4. Valida todas as questões antes de salvar qualquer coisa
    5. bulk_create das respostas com o número da tentativa
    6. Cria o Resultado com o número da tentativa
    7. Tudo dentro de transaction.atomic()
    """

    def post(self, request):

        # Valida o JSON recebido
        serializer = ResponderSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        simulado_id    = serializer.validated_data['simulado_id']
        respostas_data = serializer.validated_data['respostas']

        # Busca o simulado ativo
        try:
            simulado = Simulado.objects.get(pk=simulado_id, ativo=True)
        except Simulado.DoesNotExist:
            return Response(
                {'error': 'Simulado não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # ── Calcula o número da próxima tentativa ─────────────────────────
        # Conta quantas tentativas este aluno já fez neste simulado
        # e soma 1 para obter o número da próxima
        # Ex: 0 tentativas anteriores → tentativa 1
        #     1 tentativa anterior    → tentativa 2
        tentativas_anteriores = Resultado.objects.filter(
            aluno=request.user,
            simulado=simulado
        ).count()
        proxima_tentativa = tentativas_anteriores + 1

        # ── Busca questões do simulado via SimuladoQuestao ────────────────
        # dict {questao_id: Questao} para validação e correção eficiente
        questoes_do_simulado = {
            sq.questao_id: sq.questao
            for sq in SimuladoQuestao.objects.select_related('questao').filter(
                simulado=simulado
            )
        }

        # Valida todas as questões antes de salvar qualquer coisa
        # Evita respostas parciais se uma questão for inválida
        for item in respostas_data:
            if item['questao_id'] not in questoes_do_simulado:
                return Response(
                    {'error': f'Questão {item["questao_id"]} não pertence a este simulado.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # ── Processa e salva dentro de uma transação atômica ─────────────
        with transaction.atomic():

            acertos              = 0
            respostas_para_criar = []

            for item in respostas_data:
                questao = questoes_do_simulado[item['questao_id']]
                correta = item['opcao_escolhida'] == questao.resposta_correta

                if correta:
                    acertos += 1

                # Inclui o número da tentativa em cada Resposta
                respostas_para_criar.append(
                    Resposta(
                        aluno=request.user,
                        questao=questao,
                        simulado=simulado,
                        tentativa=proxima_tentativa,   # ← Fase 6
                        opcao_escolhida=item['opcao_escolhida'],
                        correta=correta,
                    )
                )

            # 1 query para salvar todas as respostas
            Resposta.objects.bulk_create(respostas_para_criar)

            # Calcula score
            total_questoes = len(questoes_do_simulado)
            score = round((acertos / total_questoes * 100), 2) if total_questoes > 0 else 0

            # Cria o Resultado com o número da tentativa
            resultado = Resultado.objects.create(
                aluno=request.user,
                simulado=simulado,
                tentativa=proxima_tentativa,           # ← Fase 6
                acertos=acertos,
                total_questoes=total_questoes,
                score=score,
            )

        # Monta mensagem personalizada para tentativas repetidas
        if proxima_tentativa == 1:
            mensagem = 'Simulado respondido com sucesso!'
        else:
            mensagem = f'Tentativa {proxima_tentativa} registrada com sucesso!'

        return Response({
            'message': mensagem,
            'resultado': {
                'resultado_id':   resultado.id,
                'tentativa':      proxima_tentativa,   # ← Fase 6: informa o frontend
                'simulado':       simulado.titulo,
                'acertos':        acertos,
                'total_questoes': total_questoes,
                'score':          f'{score:.2f}%',
            }
        }, status=status.HTTP_201_CREATED)
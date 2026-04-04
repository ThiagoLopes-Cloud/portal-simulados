# resultados/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.db.models import Max

from .serializers import ResultadoSerializer, RankingSerializer, GabaritoSerializer
from .models import Resultado
from respostas.models import Resposta
from simulados.models import SimuladoQuestao
from users.models import User

from collections import defaultdict


def calcular_dashboard(aluno):
    """
    Calcula o dashboard completo de um aluno.
    Reutilizada pelo DashboardView (aluno) e AdminAlunoDashboardView (professor).

    Com múltiplas tentativas (Fase 6):
    - historico lista TODAS as tentativas de todos os simulados
    - score_geral é calculado sobre todas as tentativas
    - por_materia agrega respostas de todas as tentativas
      (reflete o nível atual de conhecimento acumulado)

    Queries: 3 independente do volume de dados.
    """

    # ── Histórico — todas as tentativas, mais recentes primeiro ──────────
    resultados = (
        Resultado.objects
        .filter(aluno=aluno)
        .select_related('simulado')
        .order_by('-realizado_em')
    )

    historico = [
        {
            'resultado_id': r.id,
            'simulado':     r.simulado.titulo,
            'simulado_id':  r.simulado.id,
            'tentativa':    r.tentativa,          # ← Fase 6
            'score':        float(r.score),
            'acertos':      r.acertos,
            'total':        r.total_questoes,
            'data':         r.realizado_em.strftime('%d/%m/%Y'),
        }
        for r in resultados
    ]

    total_simulados = len(historico)

    # Score geral = média de todas as tentativas
    score_geral = (
        round(sum(r['score'] for r in historico) / total_simulados, 1)
        if total_simulados > 0 else 0
    )

    # ── Benchmark da plataforma ───────────────────────────────────────────
    todas_respostas = (
        Resposta.objects
        .filter(questao__tema__isnull=False)
        .select_related('questao__tema__materia')
    )

    benchmark_materia = {}
    benchmark_tema    = {}

    for r in todas_respostas:
        tema = r.questao.tema
        mid  = tema.materia.id
        tid  = tema.id

        if mid not in benchmark_materia:
            benchmark_materia[mid] = {'total': 0, 'acertos': 0}
        benchmark_materia[mid]['total'] += 1
        if r.correta:
            benchmark_materia[mid]['acertos'] += 1

        if tid not in benchmark_tema:
            benchmark_tema[tid] = {'total': 0, 'acertos': 0}
        benchmark_tema[tid]['total'] += 1
        if r.correta:
            benchmark_tema[tid]['acertos'] += 1

    # ── Respostas do aluno — agrega TODAS as tentativas ───────────────────
    # Isso reflete o conhecimento acumulado ao longo do tempo
    respostas_aluno = (
        Resposta.objects
        .filter(aluno=aluno, questao__tema__isnull=False)
        .select_related('questao__tema__materia')
    )

    dados = {}
    for resposta in respostas_aluno:
        tema    = resposta.questao.tema
        materia = tema.materia
        mid     = materia.id
        tid     = tema.id

        if mid not in dados:
            dados[mid] = {
                'nome':   materia.nome,
                'codigo': materia.codigo,
                'temas':  {}
            }

        if tid not in dados[mid]['temas']:
            dados[mid]['temas'][tid] = {
                'nome':    tema.nome,
                'total':   0,
                'acertos': 0,
            }

        dados[mid]['temas'][tid]['total'] += 1
        if resposta.correta:
            dados[mid]['temas'][tid]['acertos'] += 1

    # ── Formata estrutura final ───────────────────────────────────────────
    por_materia = []
    for mid, materia_data in dados.items():
        temas_lista     = []
        total_materia   = 0
        acertos_materia = 0

        for tid, tema_data in materia_data['temas'].items():
            total      = tema_data['total']
            acertos    = tema_data['acertos']
            percentual = round(acertos / total * 100, 1) if total > 0 else 0

            bt = benchmark_tema.get(tid, {'total': 0, 'acertos': 0})
            media_tema = (
                round(bt['acertos'] / bt['total'] * 100, 1)
                if bt['total'] > 0 else 0
            )

            temas_lista.append({
                'tema':             tema_data['nome'],
                'total':            total,
                'acertos':          acertos,
                'percentual':       percentual,
                'media_plataforma': media_tema,
                'diferenca_media':  round(percentual - media_tema, 1),
            })

            total_materia   += total
            acertos_materia += acertos

        temas_lista.sort(key=lambda x: x['percentual'])

        percentual_materia = (
            round(acertos_materia / total_materia * 100, 1)
            if total_materia > 0 else 0
        )

        bm = benchmark_materia.get(mid, {'total': 0, 'acertos': 0})
        media_materia = (
            round(bm['acertos'] / bm['total'] * 100, 1)
            if bm['total'] > 0 else 0
        )

        por_materia.append({
            'materia':          materia_data['nome'],
            'codigo':           materia_data['codigo'],
            'total_questoes':   total_materia,
            'acertos':          acertos_materia,
            'percentual':       percentual_materia,
            'media_plataforma': media_materia,
            'diferenca_media':  round(percentual_materia - media_materia, 1),
            'temas':            temas_lista,
        })

    por_materia.sort(key=lambda x: x['percentual'])

    return {
        'score_geral':     score_geral,
        'total_simulados': total_simulados,
        'por_materia':     por_materia,
        'historico':       historico,
    }


# ============================================================
# Views de resultado e ranking
# ============================================================

class ResultadoListView(APIView):
    """GET /api/resultados/ — todas as tentativas do aluno autenticado."""
    def get(self, request):
        resultados = Resultado.objects.filter(aluno=request.user)
        serializer = ResultadoSerializer(resultados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResultadoDetalheView(APIView):
    """GET /api/resultados/{id}/ — detalhe de um resultado específico."""
    def get(self, request, pk):
        try:
            resultado = Resultado.objects.get(pk=pk, aluno=request.user)
        except Resultado.DoesNotExist:
            return Response(
                {'error': 'Resultado não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = ResultadoSerializer(resultado)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RankingView(APIView):
    """
    GET /api/resultados/ranking/

    Com múltiplas tentativas, o ranking usa o MELHOR score de cada aluno
    por simulado — não faz sentido punir quem tentou mais vezes.

    Estratégia: para cada par (aluno, simulado), pega o Resultado
    com o maior score. Ordena esse conjunto pelo score decrescente.
    """
    def get(self, request):

        # Subconsulta: para cada (aluno, simulado), pega o id do
        # resultado com maior score (melhor tentativa)
        melhores_ids = (
            Resultado.objects
            .values('aluno', 'simulado')
            .annotate(melhor_score=Max('score'), melhor_id=Max('id'))
            .values_list('melhor_id', flat=True)
        )

        # Busca os resultados correspondentes ordenados pelo score
        resultados = (
            Resultado.objects
            .filter(id__in=melhores_ids)
            .select_related('aluno', 'simulado')
            .order_by('-score')
        )

        serializer = RankingSerializer(resultados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ============================================================
# Fase 5: Gabarito comentado
# ============================================================

class GabaritoView(APIView):
    """
    GET /api/resultados/{id}/gabarito/

    Retorna o gabarito completo de uma tentativa específica.
    Busca as respostas filtrando por aluno + simulado + tentativa —
    garante que mostra exatamente as respostas daquela tentativa.
    """

    def get(self, request, pk):

        try:
            resultado = Resultado.objects.select_related(
                'simulado', 'aluno'
            ).get(pk=pk, aluno=request.user)
        except Resultado.DoesNotExist:
            return Response(
                {'error': 'Resultado não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        simulado = resultado.simulado

        # Questões do simulado ordenadas pela tabela intermediária
        simulado_questoes = (
            SimuladoQuestao.objects
            .select_related(
                'questao',
                'questao__tema',
                'questao__tema__materia'
            )
            .filter(simulado=simulado)
            .order_by('ordem')
        )

        # Respostas desta tentativa específica
        # Filtra por tentativa para não misturar respostas de tentativas diferentes
        respostas_dict = {
            r.questao_id: r
            for r in Resposta.objects.filter(
                aluno=request.user,
                simulado=simulado,
                tentativa=resultado.tentativa    # ← filtra pela tentativa correta
            )
        }

        questoes_gabarito = []
        por_materia       = defaultdict(lambda: {'nome': '', 'acertos': 0, 'total': 0})
        temas_erros       = defaultdict(int)

        for sq in simulado_questoes:
            questao = sq.questao

            tema_nome      = questao.tema.nome            if questao.tema                          else None
            materia_codigo = questao.tema.materia.codigo  if questao.tema and questao.tema.materia else None
            materia_nome   = questao.tema.materia.nome    if questao.tema and questao.tema.materia else None

            resposta        = respostas_dict.get(questao.id)
            opcao_escolhida = resposta.opcao_escolhida if resposta else None
            correta         = resposta.correta         if resposta else None

            questoes_gabarito.append({
                'ordem':            sq.ordem,
                'enunciado':        questao.enunciado,
                'imagem_enunciado': questao.imagem_enunciado,
                'opcao_a':          questao.opcao_a,
                'opcao_b':          questao.opcao_b,
                'opcao_c':          questao.opcao_c,
                'opcao_d':          questao.opcao_d,
                'opcao_e':          questao.opcao_e or '',
                'resposta_correta': questao.resposta_correta,
                'explicacao':       questao.explicacao or '',
                'dificuldade':      questao.dificuldade,
                'tema':             tema_nome,
                'materia':          materia_codigo,
                'opcao_escolhida':  opcao_escolhida,
                'correta':          correta,
            })

            if materia_codigo:
                por_materia[materia_codigo]['nome']  = materia_nome or materia_codigo
                por_materia[materia_codigo]['total'] += 1
                if correta:
                    por_materia[materia_codigo]['acertos'] += 1

            if correta is False and tema_nome and materia_codigo:
                temas_erros[(tema_nome, materia_codigo)] += 1

        resumo_por_materia = []
        for codigo, d in por_materia.items():
            total   = d['total']
            acertos = d['acertos']
            perc    = round(acertos / total * 100, 1) if total > 0 else 0
            resumo_por_materia.append({
                'materia':    codigo,
                'nome':       d['nome'],
                'acertos':    acertos,
                'total':      total,
                'percentual': perc,
            })
        resumo_por_materia.sort(key=lambda x: x['percentual'])

        temas_com_erro = [
            {'tema': tema, 'materia': materia, 'erros': erros}
            for (tema, materia), erros in sorted(
                temas_erros.items(), key=lambda x: x[1], reverse=True
            )
        ]

        payload = {
            'simulado_id':        simulado.id,
            'simulado_titulo':    simulado.titulo,
            'acertos':            resultado.acertos,
            'total_questoes':     resultado.total_questoes,
            'score':              resultado.score,
            'realizado_em':       resultado.realizado_em,
            'questoes':           questoes_gabarito,
            'resumo_por_materia': resumo_por_materia,
            'temas_com_erro':     temas_com_erro,
        }

        serializer = GabaritoSerializer(payload)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ============================================================
# Views de dashboard e admin
# ============================================================

class DashboardView(APIView):
    """GET /api/resultados/dashboard/"""
    def get(self, request):
        dados = calcular_dashboard(request.user)
        return Response(dados, status=status.HTTP_200_OK)


class AdminAlunosListView(APIView):
    """GET /api/resultados/admin/alunos/ — apenas admins."""
    def get(self, request):
        if request.user.role != 'admin':
            return Response(
                {'error': 'Acesso restrito a administradores.'},
                status=status.HTTP_403_FORBIDDEN
            )

        alunos = User.objects.filter(role='student').order_by('username')

        lista = []
        for aluno in alunos:
            resultados  = Resultado.objects.filter(aluno=aluno)
            total       = resultados.count()
            score_medio = 0
            if total > 0:
                score_medio = round(
                    sum(float(r.score) for r in resultados) / total, 1
                )
            lista.append({
                'id':              aluno.id,
                'username':        aluno.username,
                'email':           aluno.email,
                'total_simulados': total,
                'score_medio':     score_medio,
            })

        lista.sort(key=lambda x: x['score_medio'])
        return Response(lista, status=status.HTTP_200_OK)


class AdminAlunoDashboardView(APIView):
    """GET /api/resultados/admin/alunos/{id}/ — apenas admins."""
    def get(self, request, pk):
        if request.user.role != 'admin':
            return Response(
                {'error': 'Acesso restrito a administradores.'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            aluno = User.objects.get(pk=pk, role='student')
        except User.DoesNotExist:
            return Response(
                {'error': 'Aluno não encontrado.'},
                status=status.HTTP_404_NOT_FOUND
            )

        dados = calcular_dashboard(aluno)
        dados['aluno'] = {
            'id':       aluno.id,
            'username': aluno.username,
            'email':    aluno.email,
        }

        return Response(dados, status=status.HTTP_200_OK)
# resultados/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import ResultadoSerializer, RankingSerializer
from .models import Resultado
from respostas.models import Resposta
from users.models import User


def calcular_dashboard(aluno):
    """
    Calcula o dashboard completo de um aluno.
    Reutilizada pelo DashboardView (aluno) e AdminAlunoDashboardView (professor).

    Queries realizadas:
    - 1 query para resultados do aluno
    - 1 query para respostas do aluno com JOINs
    - 1 query para todas as respostas da plataforma (benchmark)
    Total: 3 queries independente do volume de dados.
    """

    # ── Histórico ─────────────────────────────────────────────────────────
    resultados = (
        Resultado.objects
        .filter(aluno=aluno)
        .select_related('simulado')
        .order_by('-realizado_em')
    )

    historico = [
        {
            'simulado': r.simulado.titulo,
            'simulado_id': r.simulado.id,
            'score': float(r.score),
            'acertos': r.acertos,
            'total': r.total_questoes,
            'data': r.realizado_em.strftime('%d/%m/%Y'),
        }
        for r in resultados
    ]

    total_simulados = len(historico)
    score_geral = (
        round(sum(r['score'] for r in historico) / total_simulados, 1)
        if total_simulados > 0 else 0
    )

    # ── Benchmark da plataforma — médias por matéria E por tema ──────────
    # 1 query carrega tudo necessário para o benchmark
    todas_respostas = (
        Resposta.objects
        .filter(questao__tema__isnull=False)
        .select_related('questao__tema__materia')
    )

    # Agrupa benchmark em dois níveis: matéria e tema
    # { materia_id: { 'total': int, 'acertos': int } }
    benchmark_materia = {}
    # { tema_id: { 'total': int, 'acertos': int } }
    benchmark_tema = {}

    for r in todas_respostas:
        tema = r.questao.tema
        mid = tema.materia.id
        tid = tema.id

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

    # ── Respostas do aluno agrupadas por matéria e tema ───────────────────
    respostas_aluno = (
        Resposta.objects
        .filter(aluno=aluno, questao__tema__isnull=False)
        .select_related('questao__tema__materia')
    )

    dados = {}
    for resposta in respostas_aluno:
        tema = resposta.questao.tema
        materia = tema.materia
        mid = materia.id
        tid = tema.id

        if mid not in dados:
            dados[mid] = {
                'nome': materia.nome,
                'codigo': materia.codigo,
                'temas': {}
            }

        if tid not in dados[mid]['temas']:
            dados[mid]['temas'][tid] = {
                'nome': tema.nome,
                'total': 0,
                'acertos': 0,
            }

        dados[mid]['temas'][tid]['total'] += 1
        if resposta.correta:
            dados[mid]['temas'][tid]['acertos'] += 1

    # ── Formata estrutura final ───────────────────────────────────────────
    por_materia = []
    for mid, materia_data in dados.items():
        temas_lista = []
        total_materia = 0
        acertos_materia = 0

        for tid, tema_data in materia_data['temas'].items():
            total = tema_data['total']
            acertos = tema_data['acertos']
            percentual = round(acertos / total * 100, 1) if total > 0 else 0

            # Média da plataforma para este tema específico
            bt = benchmark_tema.get(tid, {'total': 0, 'acertos': 0})
            media_tema = (
                round(bt['acertos'] / bt['total'] * 100, 1)
                if bt['total'] > 0 else 0
            )

            temas_lista.append({
                'tema': tema_data['nome'],
                'total': total,
                'acertos': acertos,
                'percentual': percentual,
                'media_plataforma': media_tema,
                'diferenca_media': round(percentual - media_tema, 1),
            })

            total_materia += total
            acertos_materia += acertos

        # Ordena temas do pior para o melhor
        temas_lista.sort(key=lambda x: x['percentual'])

        percentual_materia = (
            round(acertos_materia / total_materia * 100, 1)
            if total_materia > 0 else 0
        )

        # Média da plataforma para esta matéria
        bm = benchmark_materia.get(mid, {'total': 0, 'acertos': 0})
        media_materia = (
            round(bm['acertos'] / bm['total'] * 100, 1)
            if bm['total'] > 0 else 0
        )

        por_materia.append({
            'materia': materia_data['nome'],
            'codigo': materia_data['codigo'],
            'total_questoes': total_materia,
            'acertos': acertos_materia,
            'percentual': percentual_materia,
            'media_plataforma': media_materia,
            'diferenca_media': round(percentual_materia - media_materia, 1),
            'temas': temas_lista,
        })

    por_materia.sort(key=lambda x: x['percentual'])

    return {
        'score_geral': score_geral,
        'total_simulados': total_simulados,
        'por_materia': por_materia,
        'historico': historico,
    }


class ResultadoListView(APIView):
    def get(self, request):
        resultados = Resultado.objects.filter(aluno=request.user)
        serializer = ResultadoSerializer(resultados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResultadoDetalheView(APIView):
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
    def get(self, request):
        resultados = Resultado.objects.all().order_by('-score')
        serializer = RankingSerializer(resultados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DashboardView(APIView):
    """
    Dashboard do próprio aluno autenticado.
    Rota: GET /api/resultados/dashboard/
    """
    def get(self, request):
        dados = calcular_dashboard(request.user)
        return Response(dados, status=status.HTTP_200_OK)


class AdminAlunosListView(APIView):
    """
    Lista todos os alunos com resumo de desempenho.
    Rota: GET /api/resultados/admin/alunos/
    Restrito a role='admin'.
    """
    def get(self, request):
        if request.user.role != 'admin':
            return Response(
                {'error': 'Acesso restrito a administradores.'},
                status=status.HTTP_403_FORBIDDEN
            )

        alunos = User.objects.filter(role='student').order_by('username')

        lista = []
        for aluno in alunos:
            resultados = Resultado.objects.filter(aluno=aluno)
            total = resultados.count()
            score_medio = 0
            if total > 0:
                score_medio = round(
                    sum(float(r.score) for r in resultados) / total, 1
                )

            lista.append({
                'id': aluno.id,
                'username': aluno.username,
                'email': aluno.email,
                'total_simulados': total,
                'score_medio': score_medio,
            })

        # Ordena pelo pior score — professor foca em quem precisa de mais ajuda
        lista.sort(key=lambda x: x['score_medio'])

        return Response(lista, status=status.HTTP_200_OK)


class AdminAlunoDashboardView(APIView):
    """
    Dashboard completo de um aluno específico visto pelo professor.
    Rota: GET /api/resultados/admin/alunos/{id}/
    Restrito a role='admin'.
    """
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
            'id': aluno.id,
            'username': aluno.username,
            'email': aluno.email,
        }

        return Response(dados, status=status.HTTP_200_OK)
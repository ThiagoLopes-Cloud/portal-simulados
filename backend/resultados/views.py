# resultados/views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from django.db.models import Max

from .serializers import ResultadoSerializer, RankingSerializer, GabaritoSerializer
from .models import Resultado
from respostas.models import Resposta
from simulados.models import SimuladoQuestao
from users.models import User

# Import da Fase 7: Precisamos consultar os materiais no GabaritoView
from conteudo.models import MaterialEstudo 

from collections import defaultdict


def calcular_dashboard(aluno):
    """
    Função auxiliar que calcula todo o dashboard de um aluno.
    É reutilizada tanto na view do Aluno quanto na view do Admin (Professor).
    """

    # 1. Busca todo o histórico ordenado da mais recente para a mais antiga
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
            'tentativa':    r.tentativa,          # Fase 6: Exibe a tentativa
            'score':        float(r.score),
            'acertos':      r.acertos,
            'total':        r.total_questoes,
            'data':         r.realizado_em.strftime('%d/%m/%Y'),
        }
        for r in resultados
    ]

    total_simulados = len(historico)
    score_geral = (
        round(sum(r['score'] for r in historico) / total_simulados, 1)
        if total_simulados > 0 else 0
    )

    # 2. Calcula a média geral da plataforma (Benchmark)
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

    # 3. Calcula o conhecimento consolidado do aluno atual
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

    # 4. Formata a estrutura final comparando o aluno com a plataforma
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
# Views de Resultado, Ranking e Dashboard
# ============================================================

class ResultadoListView(APIView):
    """Retorna todas as tentativas do aluno autenticado."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        resultados = Resultado.objects.filter(aluno=request.user)
        serializer = ResultadoSerializer(resultados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResultadoDetalheView(APIView):
    """Retorna dados de uma tentativa específica."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        try:
            resultado = Resultado.objects.get(pk=pk, aluno=request.user)
        except Resultado.DoesNotExist:
            return Response({'error': 'Resultado não encontrado.'}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = ResultadoSerializer(resultado)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RankingView(APIView):
    """
    Retorna o ranking geral baseado no MELHOR score de cada aluno por simulado.
    Evita penalizar alunos que refazem o simulado para estudar.
    """
    def get(self, request):
        # Subconsulta: pega o ID do melhor resultado de cada par (aluno, simulado)
        melhores_ids = (
            Resultado.objects
            .values('aluno', 'simulado')
            .annotate(melhor_score=Max('score'), melhor_id=Max('id'))
            .values_list('melhor_id', flat=True)
        )

        # Busca os objetos completos baseados na subconsulta
        resultados = (
            Resultado.objects
            .filter(id__in=melhores_ids)
            .select_related('aluno', 'simulado')
            .order_by('-score')
        )

        serializer = RankingSerializer(resultados, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ============================================================
# HUB DE REVISÃO: GABARITO & SISTEMA DE RECOMENDAÇÃO (FASES 5 E 7)
# ============================================================

class GabaritoView(APIView):
    """
    GET /api/resultados/{id}/gabarito/
    
    Esta é a view mais importante do pós-prova. Ela consolida:
    1. O gabarito comentado questão a questão.
    2. O diagnóstico de erros por matéria.
    3. Fase 7: A trilha de recomendação de materiais de estudo baseada nos erros.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        # 1. Recupera o resultado específico que o aluno está consultando
        try:
            resultado = Resultado.objects.select_related(
                'simulado', 'aluno'
            ).get(pk=pk, aluno=request.user)
        except Resultado.DoesNotExist:
            return Response({'error': 'Resultado não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        simulado = resultado.simulado

        # 2. Busca todas as questões daquele simulado mantendo a ordem correta
        simulado_questoes = (
            SimuladoQuestao.objects
            .select_related('questao', 'questao__tema', 'questao__tema__materia')
            .filter(simulado=simulado)
            .order_by('ordem')
        )

        # 3. Busca APENAS as respostas desta tentativa específica (Fase 6)
        respostas_dict = {
            r.questao_id: r
            for r in Resposta.objects.filter(
                aluno=request.user,
                simulado=simulado,
                tentativa=resultado.tentativa
            )
        }

        # Variáveis para armazenar o diagnóstico
        questoes_gabarito = []
        por_materia       = defaultdict(lambda: {'nome': '', 'acertos': 0, 'total': 0})
        
        # Fase 7: Dicionário para guardar a instância completa do Tema (nome, id, materia)
        temas_objetos     = {} 
        # Fase 7: Dicionário para contar erros por ID do Tema (Chave=ID_Tema, Valor=Qtd Erros)
        temas_erros       = defaultdict(int)

        # 4. Loop principal: cruza a questão do simulado com a resposta do aluno
        for sq in simulado_questoes:
            questao = sq.questao

            tema_nome      = questao.tema.nome            if questao.tema                          else None
            materia_codigo = questao.tema.materia.codigo  if questao.tema and questao.tema.materia else None
            materia_nome   = questao.tema.materia.nome    if questao.tema and questao.tema.materia else None

            resposta        = respostas_dict.get(questao.id)
            opcao_escolhida = resposta.opcao_escolhida if resposta else None
            correta         = resposta.correta         if resposta else None

            # Constrói o corpo do gabarito para enviar ao frontend
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

            # Alimenta estatísticas por matéria
            if materia_codigo:
                por_materia[materia_codigo]['nome']  = materia_nome or materia_codigo
                por_materia[materia_codigo]['total'] += 1
                if correta:
                    por_materia[materia_codigo]['acertos'] += 1

            # Fase 7: Coleta os temas exatos em que o aluno errou (correta is False, e não None)
            if correta is False and questao.tema:
                temas_erros[questao.tema.id] += 1
                temas_objetos[questao.tema.id] = questao.tema

        # Transforma o dict de matérias em uma lista ordenada
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

        # ============================================================
        # FASE 7: ESTRATÉGIA DE RECOMENDAÇÃO O(1)
        # ============================================================
        
        materiais_db = MaterialEstudo.objects.filter(
            tema_id__in=temas_erros.keys()
        ).order_by('tema_id', 'ordem')

        # Agrupa os materiais encontrados por ID do tema
        materiais_por_tema = defaultdict(list)
        for m in materiais_db:
            materiais_por_tema[m.tema_id].append({
                'titulo': m.titulo,
                'tipo':   m.tipo,
                'url':    m.url,
            })

        # Monta o array final de recomendações para o Frontend
        temas_com_erro = []
        # Percorre os temas errados, ordenando por quem teve mais erros primeiro
        for tema_id, erros in sorted(temas_erros.items(), key=lambda x: x[1], reverse=True):
            tema_obj = temas_objetos[tema_id]
            temas_com_erro.append({
                'tema': tema_obj.nome,
                'materia': tema_obj.materia.codigo if tema_obj.materia else '',
                'erros': erros,
                # Injeta os materiais se existirem, ou lista vazia se não houver material cadastrado
                'materiais_recomendados': materiais_por_tema.get(tema_id, [])
            })

        # Prepara a carga de dados (Payload) final
        payload = {
            'simulado_id':        simulado.id,
            'simulado_titulo':    simulado.titulo,
            'acertos':            resultado.acertos,
            'total_questoes':     resultado.total_questoes,
            'score':              resultado.score,
            'realizado_em':       resultado.realizado_em,
            'questoes':           questoes_gabarito,
            'resumo_por_materia': resumo_por_materia,
            'temas_com_erro':     temas_com_erro, # Agora enriquecido com os materiais (Fase 7)
        }

        serializer = GabaritoSerializer(payload)
        return Response(serializer.data, status=status.HTTP_200_OK)


# ============================================================
# Dashboards e Views de Administração
# ============================================================

class DashboardView(APIView):
    """Painel do Aluno"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        dados = calcular_dashboard(request.user)
        
        # ==========================================
        # FASE 9: ENVIANDO DADOS DE GAMIFICAÇÃO
        # ==========================================
        perfil = getattr(request.user, 'perfil', None)
        dados['gamificacao'] = {
            'xp': perfil.xp if perfil else 0,
            'ofensiva': perfil.ofensiva if perfil else 0,
        }
        
        return Response(dados, status=status.HTTP_200_OK)


class AdminAlunosListView(APIView):
    """Lista todos os alunos para a equipe pedagógica."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        if request.user.role != 'admin':
            return Response({'error': 'Acesso restrito.'}, status=status.HTTP_403_FORBIDDEN)

        alunos = User.objects.filter(role='student').order_by('username')
        lista = []
        for aluno in alunos:
            resultados  = Resultado.objects.filter(aluno=aluno)
            total       = resultados.count()
            score_medio = 0
            if total > 0:
                score_medio = round(sum(float(r.score) for r in resultados) / total, 1)
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
    """Vê o painel de um aluno específico como se fosse ele."""
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        if request.user.role != 'admin':
            return Response({'error': 'Acesso restrito.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            aluno = User.objects.get(pk=pk, role='student')
        except User.DoesNotExist:
            return Response({'error': 'Aluno não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        dados = calcular_dashboard(aluno)
        dados['aluno'] = {
            'id':       aluno.id,
            'username': aluno.username,
            'email':    aluno.email,
        }
        return Response(dados, status=status.HTTP_200_OK)


# ============================================================
# Fase 6: Gráfico de Evolução
# ============================================================

class EvolucaoSimuladoView(APIView):
    """
    Retorna o histórico cronológico de tentativas de um aluno 
    em um simulado específico para popular o gráfico.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, simulado_id):
        resultados = Resultado.objects.filter(
            aluno=request.user,
            simulado_id=simulado_id
        ).order_by('tentativa')

        # Se não fez o simulado ou só fez 1 vez, a API pode retornar array vazio,
        # e o Frontend lida com a lógica de só exibir se length > 1
        if not resultados.exists():
            return Response([])

        data = [
            {
                "resultado_id": r.id,
                "tentativa": r.tentativa,
                "score": float(r.score),
                "acertos": r.acertos,
                "total": r.total_questoes,
                "data": r.realizado_em
            }
            for r in resultados
        ]
        return Response(data)
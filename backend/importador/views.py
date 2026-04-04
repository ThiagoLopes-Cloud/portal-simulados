# Importa os módulos do Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

# Importa transaction para garantir atomicidade — tudo ou nada
from django.db import transaction

# Importa os models necessários para criação dos objetos
from simulados.models import Simulado, SimuladoQuestao
from questoes.models import Questao
from conteudo.models import Materia, Tema


class ImportarQuestoesView(APIView):
    """
    Importa um simulado completo a partir de um JSON gerado por IA.
    Rota: POST /api/importar/
    Requer autenticação com role=admin.

    Fluxo interno:
    1. Verifica se o usuário é admin
    2. Valida a estrutura do JSON (antes de gravar qualquer coisa)
    3. Dentro de transaction.atomic():
       - Cria o Simulado (inativo por padrão)
       - Para cada questão:
         * get_or_create Materia pelo codigo
         * get_or_create Tema pelo nome + materia
         * Cria Questao com revisado=False
         * Vincula via SimuladoQuestao
    4. Retorna relatório detalhado da importação
    """

    # Exige que o usuário esteja autenticado via JWT
    permission_classes = [IsAuthenticated]

    def post(self, request):

        # Verifica se o usuário tem papel de admin
        # Retorna 403 imediatamente se não tiver — não processa nada
        if request.user.role != 'admin':
            return Response(
                {'error': 'Apenas administradores podem importar questões.'},
                status=status.HTTP_403_FORBIDDEN
            )

        # Extrai os dados do corpo da requisição
        dados = request.data

        # Valida presença das duas chaves obrigatórias no JSON raiz
        if 'simulado' not in dados or 'questoes' not in dados:
            return Response(
                {'error': 'JSON inválido. Campos obrigatórios: "simulado" e "questoes".'},
                status=status.HTTP_400_BAD_REQUEST
            )

        dados_simulado = dados['simulado']
        dados_questoes = dados['questoes']

        # Valida que questoes é uma lista com ao menos 1 item
        if not isinstance(dados_questoes, list) or len(dados_questoes) == 0:
            return Response(
                {'error': '"questoes" deve ser uma lista com ao menos 1 item.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Valida campo obrigatório do simulado
        if not dados_simulado.get('titulo'):
            return Response(
                {'error': 'Campo obrigatório ausente: simulado.titulo'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Campos que toda questão precisa ter preenchidos
        campos_obrigatorios = [
            'ordem', 'enunciado',
            'opcao_a', 'opcao_b', 'opcao_c', 'opcao_d',
            'resposta_correta',
        ]

        # Valores válidos para cada campo controlado
        opcoes_validas = {'A', 'B', 'C', 'D', 'E'}
        dificuldades_validas = {'F', 'M', 'D'}

        # Valida TODAS as questões antes de gravar qualquer coisa
        # Se uma questão falhar, o professor recebe o erro antes de
        # qualquer escrita no banco — não cria simulado parcial
        for i, q in enumerate(dados_questoes):

            # Verifica campos obrigatórios — não pode estar ausente ou vazio
            for campo in campos_obrigatorios:
                valor = q.get(campo)
                if valor is None or str(valor).strip() == '':
                    return Response(
                        {'error': f'Questão {i + 1}: campo obrigatório ausente ou vazio: "{campo}"'},
                        status=status.HTTP_400_BAD_REQUEST
                    )

            # Valida que a resposta correta é uma das 5 alternativas válidas
            if q.get('resposta_correta') not in opcoes_validas:
                return Response(
                    {'error': f'Questão {i + 1}: "resposta_correta" deve ser A, B, C, D ou E.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Valida dificuldade apenas se o campo estiver presente
            if q.get('dificuldade') and q['dificuldade'] not in dificuldades_validas:
                return Response(
                    {'error': f'Questão {i + 1}: "dificuldade" deve ser F, M ou D.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # A partir daqui toda a gravação acontece dentro de uma transação
        # Se qualquer operação falhar, o banco volta ao estado anterior
        # Nenhum dado parcial é gravado
        with transaction.atomic():

            # Cria o simulado — SEMPRE inativo na importação
            # Professor precisa ativar manualmente no Admin após revisar
            simulado = Simulado.objects.create(
                titulo=dados_simulado['titulo'],
                descricao=dados_simulado.get('descricao', ''),
                criado_por=request.user,
                ativo=False,
                data_inicio=dados_simulado.get('data_inicio'),
                data_fim=dados_simulado.get('data_fim'),
            )

            # Lista que acumula o relatório de cada questão criada
            relatorio_questoes = []

            for q in dados_questoes:

                # Resolve Materia — cria automaticamente se não existir
                # O codigo é a chave única (ex: MAT, PORT, BIO)
                materia = None
                if q.get('materia'):
                    materia, criou_materia = Materia.objects.get_or_create(
                        # Busca pelo codigo em maiúsculo — padroniza a entrada
                        codigo=q['materia'].upper().strip(),
                        # Se criar novo, usa o codigo como nome temporário
                        # Professor pode editar o nome completo no Admin depois
                        defaults={'nome': q['materia'].upper().strip()}
                    )

                # Resolve Tema — cria automaticamente se não existir
                # A combinação nome + materia é a chave única do tema
                tema = None
                if q.get('tema') and materia:
                    tema, criou_tema = Tema.objects.get_or_create(
                        nome=q['tema'].strip(),
                        materia=materia,
                        defaults={'descricao': ''}
                    )

                # Cria a questão no banco de questões independente
                # revisado=False — toda questão importada entra pendente
                # Só aparece para alunos após o professor aprovar no Admin
                questao = Questao.objects.create(
                    tema=tema,
                    enunciado=q['enunciado'].strip(),
                    imagem_enunciado=q.get('imagem_enunciado') or None,
                    opcao_a=q['opcao_a'].strip(),
                    opcao_b=q['opcao_b'].strip(),
                    opcao_c=q['opcao_c'].strip(),
                    opcao_d=q['opcao_d'].strip(),
                    opcao_e=q.get('opcao_e', '').strip(),
                    imagem_opcao_a=q.get('imagem_opcao_a') or None,
                    imagem_opcao_b=q.get('imagem_opcao_b') or None,
                    imagem_opcao_c=q.get('imagem_opcao_c') or None,
                    imagem_opcao_d=q.get('imagem_opcao_d') or None,
                    imagem_opcao_e=q.get('imagem_opcao_e') or None,
                    resposta_correta=q['resposta_correta'],
                    dificuldade=q.get('dificuldade', 'M'),
                    explicacao=q.get('explicacao', '').strip(),
                    fonte=q.get('fonte', 'Gerado por IA').strip(),
                    ano_origem=q.get('ano_origem') or None,
                    revisado=False,
                )

                # Vincula a questão ao simulado via tabela intermediária
                # ordem vem do JSON — define a sequência na prova
                # peso=1.00 é o padrão — base para TRI futuro
                SimuladoQuestao.objects.create(
                    simulado=simulado,
                    questao=questao,
                    ordem=q['ordem'],
                    peso=1.00,
                )

                # Acumula no relatório para retornar ao frontend
                relatorio_questoes.append({
                    'ordem': q['ordem'],
                    'status': 'criada',
                    'questao_id': questao.id,
                })

        # Retorna relatório completo da importação
        return Response({
            'simulado_id': simulado.id,
            'simulado_titulo': simulado.titulo,
            'total_importadas': len(relatorio_questoes),
            'questoes': relatorio_questoes,
            'avisos': [
                'Simulado criado como inativo — ative no painel Admin após revisar as questões.',
                'Todas as questões estão pendentes de revisão. Acesse /admin para aprovar.',
            ]
        }, status=status.HTTP_201_CREATED)
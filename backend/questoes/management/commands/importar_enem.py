# questoes/management/commands/importar_enem.py
#
# Management command para importar questões do ENEM via API pública.
# Uso: python manage.py importar_enem --ano 2023
#      python manage.py importar_enem --ano 2023 --ano 2022 --ano 2021
#      python manage.py importar_enem --todos
#
# Fonte da API: https://api.enem.dev
# Repositório: https://github.com/yunger7/enem-api

import time
import requests

from django.core.management.base import BaseCommand
from django.db import transaction

from questoes.models import Questao
from conteudo.models import Materia, Tema


# URL base da API pública do ENEM
API_BASE = 'https://api.enem.dev/v1'

# Anos disponíveis na API (conforme documentação do repositório)
ANOS_DISPONIVEIS = [
    2009, 2010, 2011, 2012, 2013, 2014,
    2015, 2016, 2017, 2018, 2019, 2020,
    2021, 2022, 2023
]

# Mapeamento de discipline (API) → nome da Matéria no nosso banco
# Usamos nomes em português para exibição no sistema
MAPA_MATERIAS = {
    'linguagens':        ('Linguagens, Códigos e suas Tecnologias', 'LC'),
    'matematica':        ('Matemática e suas Tecnologias', 'MT'),
    'ciencias-humanas':  ('Ciências Humanas e suas Tecnologias', 'CH'),
    'ciencias-natureza': ('Ciências da Natureza e suas Tecnologias', 'CN'),
    'redacao':           ('Redação', 'RED'),
}


class Command(BaseCommand):
    """
    Importa questões do ENEM para o banco de dados local.
    Idempotente — pode ser rodado múltiplas vezes sem duplicar questões.
    A unicidade é garantida pelo campo fonte (ex: "ENEM 2023 - Questão 1").
    """

    help = 'Importa questões do ENEM via API pública (api.enem.dev)'

    def add_arguments(self, parser):
        """
        Define os argumentos aceitos pelo comando.
        --ano pode ser passado múltiplas vezes: --ano 2023 --ano 2022
        --todos importa todos os anos disponíveis de uma vez
        """
        parser.add_argument(
            '--ano',
            type=int,
            action='append',    # permite múltiplos --ano
            dest='anos',
            help='Ano da prova ENEM (ex: 2023). Pode ser repetido.',
        )
        parser.add_argument(
            '--todos',
            action='store_true',
            help='Importa todos os anos disponíveis na API.',
        )

    def handle(self, *args, **options):
        """
        Ponto de entrada do comando.
        Determina quais anos importar e inicia o processo.
        """
        if options['todos']:
            anos = ANOS_DISPONIVEIS
        elif options['anos']:
            anos = options['anos']
        else:
            self.stderr.write(
                self.style.ERROR(
                    'Informe pelo menos um ano com --ano 2023 ou use --todos'
                )
            )
            return

        self.stdout.write(
            self.style.SUCCESS(f'\n🚀 Iniciando importação para {len(anos)} ano(s): {anos}\n')
        )

        # Totalizadores para o resumo final
        total_importadas = 0
        total_puladas = 0
        total_erros = 0

        for ano in anos:
            importadas, puladas, erros = self.importar_ano(ano)
            total_importadas += importadas
            total_puladas += puladas
            total_erros += erros

        # Resumo final
        self.stdout.write('\n' + '─' * 50)
        self.stdout.write(
            self.style.SUCCESS(
                f'✅ Concluído!\n'
                f'   Importadas: {total_importadas}\n'
                f'   Puladas (já existiam): {total_puladas}\n'
                f'   Erros: {total_erros}'
            )
        )

    def importar_ano(self, ano):
        """
        Importa todas as questões de um ano específico.
        Faz paginação automática até buscar todas as questões.
        Retorna (importadas, puladas, erros).
        """
        self.stdout.write(f'\n📅 Importando ENEM {ano}...')

        importadas = 0
        puladas = 0
        erros = 0
        offset = 0
        limit = 50  # busca 50 questões por vez para não sobrecarregar a API

        while True:
            # Monta a URL com paginação
            url = f'{API_BASE}/exams/{ano}/questions'
            params = {'limit': limit, 'offset': offset}

            try:
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()

            except requests.exceptions.Timeout:
                self.stderr.write(
                    self.style.ERROR(f'  ⚠️  Timeout ao buscar {url} — pulando bloco')
                )
                erros += 1
                break

            except requests.exceptions.HTTPError as e:
                if response.status_code == 404:
                    self.stderr.write(
                        self.style.WARNING(f'  ⚠️  Ano {ano} não encontrado na API')
                    )
                else:
                    self.stderr.write(self.style.ERROR(f'  ❌ Erro HTTP: {e}'))
                    erros += 1
                break

            except Exception as e:
                self.stderr.write(self.style.ERROR(f'  ❌ Erro inesperado: {e}'))
                erros += 1
                break

            questoes = data.get('questions', [])
            metadata = data.get('metadata', {})

            if not questoes:
                break

            # Processa cada questão do bloco
            for questao_data in questoes:
                try:
                    resultado = self.processar_questao(questao_data, ano)
                    if resultado == 'importada':
                        importadas += 1
                    elif resultado == 'pulada':
                        puladas += 1
                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(
                            f'  ❌ Erro ao processar questão {questao_data.get("index")}: {e}'
                        )
                    )
                    erros += 1

            # Log de progresso a cada bloco
            self.stdout.write(
                f'  → {offset + len(questoes)}/{metadata.get("total", "?")} questões processadas'
            )

            # Verifica se há mais páginas
            if not metadata.get('hasMore', False):
                break

            offset += limit

            # Pausa entre requisições para não sobrecarregar a API
            # Comportamento respeitoso com a API pública
            time.sleep(0.5)

        return importadas, puladas, erros

    @transaction.atomic
    def processar_questao(self, data, ano):
        """
        Processa uma questão individual da API e salva no banco.
        Usa transaction.atomic para garantir consistência.
        Retorna 'importada' ou 'pulada'.
        """
        index = data.get('index', 0)
        discipline = data.get('discipline', '')

        # Gera a fonte no formato padronizado
        # Usamos isso como chave de unicidade — evita duplicatas
        fonte = f'ENEM {ano} — Questão {index}'

        # Verifica se a questão já existe no banco
        if Questao.objects.filter(fonte=fonte).exists():
            return 'pulada'

        # Obtém ou cria a Matéria baseado na discipline da API
        materia = self.obter_materia(discipline)

        # Extrai o enunciado — a API usa 'context'
        enunciado = data.get('context', '').strip()
        if not enunciado:
            # Algumas questões de redação não têm context
            enunciado = data.get('title', f'Questão {index} — ENEM {ano}')

        # Extrai a imagem do enunciado — primeiro arquivo da lista
        files = data.get('files', [])
        imagem_enunciado = files[0] if files else None

        # Extrai o gabarito
        resposta_correta = data.get('correctAlternative', 'A').upper()

        # Valida se a resposta correta é uma das opções válidas
        if resposta_correta not in ['A', 'B', 'C', 'D', 'E']:
            resposta_correta = 'A'  # fallback seguro

        # Processa as alternativas
        alternativas = self.processar_alternativas(data.get('alternatives', []))

        # Cria a questão no banco
        Questao.objects.create(
            enunciado=enunciado,
            imagem_enunciado=imagem_enunciado,
            opcao_a=alternativas.get('A', {}).get('texto', ''),
            opcao_b=alternativas.get('B', {}).get('texto', ''),
            opcao_c=alternativas.get('C', {}).get('texto', ''),
            opcao_d=alternativas.get('D', {}).get('texto', ''),
            opcao_e=alternativas.get('E', {}).get('texto', ''),
            imagem_opcao_a=alternativas.get('A', {}).get('imagem'),
            imagem_opcao_b=alternativas.get('B', {}).get('imagem'),
            imagem_opcao_c=alternativas.get('C', {}).get('imagem'),
            imagem_opcao_d=alternativas.get('D', {}).get('imagem'),
            imagem_opcao_e=alternativas.get('E', {}).get('imagem'),
            resposta_correta=resposta_correta,
            dificuldade='M',        # padrão Médio — API não fornece dificuldade
            explicacao='',          # API não fornece explicação
            tema=materia.temas.first() if materia else None,
            ano_origem=ano,
            fonte=fonte,
        )

        return 'importada'

    def processar_alternativas(self, alternatives):
        """
        Transforma a lista de alternativas da API em um dict indexado por letra.
        Retorna: { 'A': { 'texto': '...', 'imagem': '...' }, ... }
        """
        resultado = {}
        for alt in alternatives:
            letra = alt.get('letter', '').upper()
            if letra in ['A', 'B', 'C', 'D', 'E']:
                resultado[letra] = {
                    'texto': alt.get('text', '').strip(),
                    'imagem': alt.get('file'),  # None se não houver imagem
                }
        return resultado

    def obter_materia(self, discipline):
        """
        Obtém ou cria a Matéria correspondente à discipline da API.
        Também cria um Tema genérico se a matéria for nova —
        as questões ficam vinculadas a esse tema padrão até o professor
        classificar manualmente.
        """
        if not discipline or discipline not in MAPA_MATERIAS:
            return None

        nome, codigo = MAPA_MATERIAS[discipline]

        # get_or_create — não duplica se já existir
        materia, criada = Materia.objects.get_or_create(
            codigo=codigo,
            defaults={'nome': nome}
        )

        if criada:
            self.stdout.write(
                self.style.SUCCESS(f'  ✨ Matéria criada: {nome} ({codigo})')
            )
            # Cria um tema genérico para a matéria recém-criada
            # Permite vincular as questões sem deixar tema=NULL
            Tema.objects.get_or_create(
                materia=materia,
                nome=f'Geral — {nome}',
                defaults={'descricao': 'Tema padrão — classifique manualmente'}
            )

        return materia
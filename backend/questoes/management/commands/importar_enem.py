# questoes/management/commands/importar_enem.py
#
# Management command para importar questões do ENEM via API pública.
# Uso: python manage.py importar_enem --ano 2023
#      python manage.py importar_enem --ano 2023 --ano 2022
#      python manage.py importar_enem --todos
#
# Fonte: https://api.enem.dev | https://github.com/yunger7/enem-api

import re
import time
import requests

from django.core.management.base import BaseCommand
from django.db import transaction

from questoes.models import Questao
from conteudo.models import Materia, Tema


API_BASE = 'https://api.enem.dev/v1'

ANOS_DISPONIVEIS = [
    2009, 2010, 2011, 2012, 2013, 2014,
    2015, 2016, 2017, 2018, 2019, 2020,
    2021, 2022, 2023
]

# Mapeamento discipline da API → (nome, código) da nossa Materia
MAPA_MATERIAS = {
    'linguagens':        ('Linguagens, Códigos e suas Tecnologias', 'LC'),
    'matematica':        ('Matemática e suas Tecnologias', 'MT'),
    'ciencias-humanas':  ('Ciências Humanas e suas Tecnologias', 'CH'),
    'ciencias-natureza': ('Ciências da Natureza e suas Tecnologias', 'CN'),
    'redacao':           ('Redação', 'RED'),
}

# URLs de imagens quebradas conhecidas — ignoradas no enunciado
IMAGENS_QUEBRADAS = [
    'broken-image.svg',
    'enem.dev/broken-image',
]


class Command(BaseCommand):
    help = 'Importa questões do ENEM via API pública (api.enem.dev)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--ano',
            type=int,
            action='append',
            dest='anos',
            help='Ano da prova (ex: 2023). Pode repetir: --ano 2023 --ano 2022',
        )
        parser.add_argument(
            '--todos',
            action='store_true',
            help='Importa todos os anos disponíveis.',
        )

    def handle(self, *args, **options):
        if options['todos']:
            anos = ANOS_DISPONIVEIS
        elif options['anos']:
            anos = options['anos']
        else:
            self.stderr.write(self.style.ERROR(
                'Informe --ano 2023 ou use --todos'
            ))
            return

        self.stdout.write(self.style.SUCCESS(
            f'\n🚀 Importando {len(anos)} ano(s): {anos}\n'
        ))

        total_importadas = 0
        total_puladas = 0
        total_erros = 0

        for ano in anos:
            i, p, e = self.importar_ano(ano)
            total_importadas += i
            total_puladas += p
            total_erros += e

        self.stdout.write('\n' + '─' * 50)
        self.stdout.write(self.style.SUCCESS(
            f'✅ Concluído!\n'
            f'   Importadas : {total_importadas}\n'
            f'   Puladas    : {total_puladas}\n'
            f'   Erros      : {total_erros}'
        ))

    def importar_ano(self, ano):
        self.stdout.write(f'\n📅 Importando ENEM {ano}...')

        importadas = puladas = erros = 0
        offset = 0
        limit = 50

        while True:
            try:
                response = requests.get(
                    f'{API_BASE}/exams/{ano}/questions',
                    params={'limit': limit, 'offset': offset},
                    timeout=30
                )
                response.raise_for_status()
                data = response.json()

            except requests.exceptions.Timeout:
                self.stderr.write(self.style.ERROR(
                    f'  ⚠️  Timeout no offset {offset} — abortando ano {ano}'
                ))
                erros += 1
                break

            except requests.exceptions.HTTPError as e:
                if response.status_code == 404:
                    self.stderr.write(self.style.WARNING(
                        f'  ⚠️  Ano {ano} não encontrado na API'
                    ))
                else:
                    self.stderr.write(self.style.ERROR(f'  ❌ HTTP Error: {e}'))
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

            for q in questoes:
                try:
                    resultado = self.processar_questao(q, ano)
                    if resultado == 'importada':
                        importadas += 1
                    else:
                        puladas += 1
                except Exception as e:
                    self.stderr.write(self.style.ERROR(
                        f'  ❌ Erro Q{q.get("index")}: {e}'
                    ))
                    erros += 1

            self.stdout.write(
                f'  → {offset + len(questoes)}/{metadata.get("total", "?")} processadas'
                f' | ✅ {importadas} importadas | ⏭ {puladas} puladas'
            )

            if not metadata.get('hasMore', False):
                break

            offset += limit
            time.sleep(0.5)  # respeita a API pública

        return importadas, puladas, erros

    @transaction.atomic
    def processar_questao(self, data, ano):
        """
        Processa uma questão e salva no banco.

        Estrutura confirmada da API:
        - context: Markdown com texto + imagens embutidas como ![](url)
        - alternativesIntroduction: comando da questão ("Assinale...")
        - alternatives[].text: texto puro das alternativas
        - alternatives[].file: sempre null — imagens só existem no context
        """
        index = data.get('index', 0)
        fonte = f'ENEM {ano} — Questão {index}'

        # Idempotência — pula se já existe
        if Questao.objects.filter(fonte=fonte).exists():
            return 'pulada'

        # ── Monta o enunciado completo ────────────────────────────────────
        context = (data.get('context') or '').strip()
        intro   = (data.get('alternativesIntroduction') or '').strip()

        # Remove imagens quebradas do context antes de salvar
        context = self.remover_imagens_quebradas(context)

        # Enunciado = contexto + comando da questão
        # Separados por linha em branco para o Markdown renderizar corretamente
        if context and intro:
            enunciado = f'{context}\n\n{intro}'
        elif context:
            enunciado = context
        elif intro:
            enunciado = intro
        else:
            # Fallback para questões sem texto (não deveria acontecer)
            enunciado = data.get('title', f'Questão {index} — ENEM {ano}')

        # ── Alternativas ──────────────────────────────────────────────────
        # Confirmado: alternatives[].text é texto puro, file é sempre null
        alternativas = self.processar_alternativas(data.get('alternatives', []))

        # ── Gabarito ──────────────────────────────────────────────────────
        resposta_correta = (data.get('correctAlternative') or 'A').upper()
        if resposta_correta not in ['A', 'B', 'C', 'D', 'E']:
            resposta_correta = 'A'

        # ── Matéria e tema ────────────────────────────────────────────────
        materia = self.obter_materia(data.get('discipline', ''))

        # ── Salva no banco ────────────────────────────────────────────────
        Questao.objects.create(
            enunciado=enunciado,
            imagem_enunciado=None,      # imagens estão embutidas no Markdown
            opcao_a=alternativas.get('A', {}).get('texto', ''),
            opcao_b=alternativas.get('B', {}).get('texto', ''),
            opcao_c=alternativas.get('C', {}).get('texto', ''),
            opcao_d=alternativas.get('D', {}).get('texto', ''),
            opcao_e=alternativas.get('E', {}).get('texto', ''),
            imagem_opcao_a=None,        # confirmado: sempre null na API
            imagem_opcao_b=None,
            imagem_opcao_c=None,
            imagem_opcao_d=None,
            imagem_opcao_e=None,
            resposta_correta=resposta_correta,
            dificuldade='M',            # API não fornece — padrão Médio
            explicacao='',              # API não fornece
            tema=materia.temas.first() if materia else None,
            ano_origem=ano,
            fonte=fonte,
        )

        return 'importada'

    def processar_alternativas(self, alternatives):
        """
        Transforma a lista de alternativas em dict indexado por letra.
        Confirmado na API: text é sempre texto puro, file é sempre null.
        Retorna: { 'A': { 'texto': '...' }, 'B': {...}, ... }
        """
        resultado = {}
        for alt in alternatives:
            letra = (alt.get('letter') or '').upper()
            if letra in ['A', 'B', 'C', 'D', 'E']:
                resultado[letra] = {
                    'texto': (alt.get('text') or '').strip(),
                }
        return resultado

    def remover_imagens_quebradas(self, texto):
        """
        Remove referências a imagens quebradas do Markdown.
        Ex: ![](https://enem.dev/broken-image.svg) → removido
        Mantém todas as outras imagens intactas.
        """
        if not texto:
            return texto

        for padrao in IMAGENS_QUEBRADAS:
            # Remove a tag Markdown completa que contenha o padrão
            texto = re.sub(
                r'!\[([^\]]*)\]\([^)]*' + re.escape(padrao) + r'[^)]*\)',
                '',
                texto
            )

        # Remove linhas em branco extras que possam ter sobrado
        texto = re.sub(r'\n{3,}', '\n\n', texto)
        return texto.strip()

    def obter_materia(self, discipline):
        """
        Obtém ou cria a Matéria e um Tema genérico.
        O Tema genérico permite vincular questões ao diagnóstico
        mesmo antes do professor classificar manualmente.
        """
        if not discipline or discipline not in MAPA_MATERIAS:
            return None

        nome, codigo = MAPA_MATERIAS[discipline]

        materia, criada = Materia.objects.get_or_create(
            codigo=codigo,
            defaults={'nome': nome}
        )

        if criada:
            self.stdout.write(self.style.SUCCESS(
                f'  ✨ Matéria criada: {nome} ({codigo})'
            ))

        # Tema genérico — questões ficam vinculadas até classificação manual
        Tema.objects.get_or_create(
            materia=materia,
            nome=f'Geral — {nome}',
            defaults={'descricao': 'Tema padrão — classifique manualmente pelo Admin'}
        )

        return materia
import time
import requests
from django.core.management.base import BaseCommand
from questoes.models import Questao
from conteudo.models import Materia, Tema


class Command(BaseCommand):
    help = 'Importa questões do ENEM da API yunger7/enem-api de forma gradual e segura'

    def add_arguments(self, parser):
        parser.add_argument('--ano', type=int, required=True, help='Ano da prova. Ex: 2023')
        parser.add_argument('--disciplina', type=str, required=True, help='Ex: matematica, ciencias-natureza, ciencias-humanas, linguagens')
        parser.add_argument('--limite', type=int, default=0, help='Limite de questões a processar. 0 para processar tudo.')
        parser.add_argument('--delay', type=int, default=2, help='Atraso (em segundos) entre as requisições para evitar rate limit da API externa')

    def handle(self, *args, **options):
        ano = options['ano']
        disciplina = options['disciplina']
        limite = options['limite']
        delay = options['delay']

        # 1. Preparação da estrutura de relacionamentos (Tema e Matéria)
        # Associa dinamicamente as disciplinas do ENEM com seu banco
        materia_codigo = disciplina[:10].upper()
        # Garante que a Matéria e o Tema existem, ou os cria genéricos
        materia, _ = Materia.objects.get_or_create(
            codigo=materia_codigo,
            defaults={'nome': f"{disciplina.replace('-', ' ').title()} - teste29/03"}
        )
        tema, _ = Tema.objects.get_or_create(
            materia=materia,
            nome=f'Questões Importadas ENEM ({disciplina}) - teste29/03',
            defaults={'descricao': 'Tema gerado automaticamente pela importação de teste.'}
        )

        self.stdout.write(self.style.NOTICE(f'Iniciando conexão com API enem.dev...'))
        self.stdout.write(self.style.NOTICE(f'Ano: {ano} | Disciplina: {disciplina}'))

        # 2. Conectando com a API
        url_api = f'https://api.enem.dev/v1/exams/{ano}/{disciplina}/questions'
        
        try:
            response = requests.get(url_api, timeout=15)
            response.raise_for_status()
            
            data = response.json()
            
            # Formato paginado ou estático
            questoes_api = data if isinstance(data, list) else data.get('questions', [])
            
            if not questoes_api:
                self.stdout.write(self.style.WARNING('A API não retornou questões. Operação abortada.'))
                return

        except requests.exceptions.RequestException as e:
            self.stdout.write(self.style.ERROR(f'Falha ao conectar com a API do ENEM: {e}'))
            return

        # 3. Processamento das questões (Lote)
        importadas = 0
        ignoradas = 0

        total_questoes = len(questoes_api)
        if limite > 0:
            total_questoes = min(limite, total_questoes)

        self.stdout.write(self.style.SUCCESS(f'{total_questoes} questões identificadas. Processo rodando...'))

        for i, item in enumerate(questoes_api[:total_questoes], start=1):
            
            # Identificador Único
            identificador_api = item.get('id', f'enem-{ano}-{disciplina}-q{i}')
            
            questao_texto = item.get('context', '') + "<br><br>" + item.get('question', '')
            alternativas = item.get('alternatives', [{}, {}, {}, {}, {}])
            
            letras_api = ['A', 'B', 'C', 'D', 'E']
            opcoes_dict = {
                'A': '', 'B': '', 'C': '', 'D': '', 'E': ''
            }
            
            for alt in alternativas:
                letra = alt.get('letter', '').upper()
                texto = alt.get('text', '')
                if letra in opcoes_dict:
                    opcoes_dict[letra] = texto
                    
            resp_corr = str(item.get('correctAlternative', 'A')).upper()

            try:
                # Importação com Idempotência
                obj, created = Questao.objects.get_or_create(
                    id_origem=identificador_api,
                    defaults={
                        'tema': tema,
                        'enunciado': questao_texto,
                        'opcao_a': opcoes_dict['A'],
                        'opcao_b': opcoes_dict['B'],
                        'opcao_c': opcoes_dict['C'],
                        'opcao_d': opcoes_dict['D'],
                        'opcao_e': opcoes_dict['E'] or '',  
                        'resposta_correta': resp_corr,
                        'dificuldade': 'M',
                        'ano_origem': ano,
                        'fonte': f'ENEM {ano} — {disciplina} - teste29/03',
                    }
                )

                if created:
                    importadas += 1
                    self.stdout.write(self.style.SUCCESS(f'[OK] Questão cadastrada — {identificador_api}'))
                else:
                    ignoradas += 1
                    self.stdout.write(self.style.WARNING(f'[EX] Questão já existia — {identificador_api}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Erro ao salvar {identificador_api}: {str(e)}'))

            time.sleep(delay)

        # 4. Finalização
        self.stdout.write(self.style.SUCCESS('\n==================================='))
        self.stdout.write(self.style.SUCCESS('     IMPORTAÇÃO (TESTE) CONCLUÍDA! '))
        self.stdout.write(self.style.SUCCESS(f' {importadas} inseridas | {ignoradas} ignoradas (duplicadas)'))
        self.stdout.write(self.style.SUCCESS('===================================\n'))

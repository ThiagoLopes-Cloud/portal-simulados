# Importa o módulo serializers do Django REST Framework
from rest_framework import serializers

# Importa os models necessários
from .models import Resultado
from respostas.models import Resposta


# ============================================================
# Serializers existentes — não alterados
# ============================================================

class ResultadoSerializer(serializers.ModelSerializer):
    """
    Serializer para exibir o resultado final de um aluno em um simulado.
    Usado em GET /api/resultados/ e GET /api/resultados/{id}/
    """

    aluno_username = serializers.SerializerMethodField()
    simulado_titulo = serializers.SerializerMethodField()

    class Meta:
        model = Resultado
        fields = [
            'id',
            'aluno_username',
            'simulado_titulo',
            'acertos',
            'total_questoes',
            'score',
            'realizado_em',
        ]

    def get_aluno_username(self, obj):
        return obj.aluno.username

    def get_simulado_titulo(self, obj):
        return obj.simulado.titulo


class RankingSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para o ranking de alunos.
    Usado em GET /api/resultados/ranking/
    """

    aluno_username = serializers.SerializerMethodField()
    simulado_titulo = serializers.SerializerMethodField()

    class Meta:
        model = Resultado
        fields = [
            'aluno_username',
            'simulado_titulo',
            'acertos',
            'total_questoes',
            'score',
            'realizado_em',
        ]

    def get_aluno_username(self, obj):
        return obj.aluno.username

    def get_simulado_titulo(self, obj):
        return obj.simulado.titulo


# ============================================================
# NOVO — Fase 5: Gabarito comentado
# ============================================================

class QuestaoGabaritoSerializer(serializers.Serializer):
    """
    Serializer para uma questão dentro do gabarito.
    Combina dados da Questao com a Resposta do aluno.

    Diferente do QuestaoSerializer normal (usado na prova),
    este expõe resposta_correta e explicacao — que são ocultados
    durante a prova por segurança, mas liberados após o envio.

    Também inclui opcao_escolhida e correta da Resposta do aluno,
    permitindo o frontend mostrar o estado de cada questão.

    Já inclui tema e materia — base para Fase 7 (recomendação).
    """

    # Dados da questão
    ordem           = serializers.IntegerField()
    enunciado       = serializers.CharField()
    imagem_enunciado = serializers.URLField(allow_null=True)
    opcao_a         = serializers.CharField()
    opcao_b         = serializers.CharField()
    opcao_c         = serializers.CharField()
    opcao_d         = serializers.CharField()
    opcao_e         = serializers.CharField(allow_blank=True)

    # Gabarito — só exposto APÓS o envio das respostas
    resposta_correta = serializers.CharField()
    explicacao       = serializers.CharField(allow_blank=True)
    dificuldade      = serializers.CharField()

    # Taxonomia — base para recomendação (Fase 7)
    tema    = serializers.SerializerMethodField()
    materia = serializers.SerializerMethodField()

    # Resposta do aluno — null se não respondeu (questão pulada)
    opcao_escolhida = serializers.CharField(allow_null=True)
    correta         = serializers.BooleanField(allow_null=True)

    def get_tema(self, obj):
        """
        Retorna o nome do tema se existir, ou None.
        obj é um dict montado na view — não um model diretamente.
        """
        return obj.get('tema')

    def get_materia(self, obj):
        """
        Retorna o código da matéria se existir, ou None.
        """
        return obj.get('materia')


class GabaritoSerializer(serializers.Serializer):
    """
    Serializer principal do gabarito.
    Usado em GET /api/resultados/{id}/gabarito/

    Retorna o resultado completo com todas as questões,
    as respostas do aluno, o gabarito e as explicações.

    Estrutura pensada para suportar:
    - Fase 5: exibição do gabarito comentado
    - Fase 6: histórico de evolução (score + data já incluídos)
    - Fase 7: recomendação (tema + materia + correta por questão)
    """

    # Dados do resultado
    simulado_id    = serializers.IntegerField()
    simulado_titulo = serializers.CharField()
    acertos        = serializers.IntegerField()
    total_questoes = serializers.IntegerField()
    score          = serializers.DecimalField(max_digits=5, decimal_places=2)
    realizado_em   = serializers.DateTimeField()

    # Lista completa de questões com gabarito e resposta do aluno
    questoes = QuestaoGabaritoSerializer(many=True)

    # Resumo por matéria — base para Fase 7
    # Ex: [{"materia": "MAT", "acertos": 3, "total": 5, "percentual": 60.0}]
    resumo_por_materia = serializers.ListField(
        child=serializers.DictField(),
        default=list
    )

    # Temas com erro — base para recomendação (Fase 7)
    # Ex: [{"tema": "Funções", "materia": "MAT", "erros": 2}]
    temas_com_erro = serializers.ListField(
        child=serializers.DictField(),
        default=list
    )
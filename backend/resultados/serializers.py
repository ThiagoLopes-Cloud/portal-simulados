# Importa o módulo serializers do Django REST Framework
from rest_framework import serializers

# Importa o model Resultado
from .models import Resultado

# Importa o RespostaSerializer para exibir o gabarito junto com o resultado
from respostas.serializers import RespostaSerializer

# Serializer de resultado — usado em GET /api/resultados
class ResultadoSerializer(serializers.ModelSerializer):
    """
    Serializer para exibir o resultado final de um aluno em um simulado.
    Retorna o score, acertos e total de questões.
    Usado na tela de resultado do Vue.js.
    """

    # Campo calculado — retorna o nome do aluno em vez do ID
    aluno_username = serializers.SerializerMethodField()

    # Campo calculado — retorna o título do simulado em vez do ID
    simulado_titulo = serializers.SerializerMethodField()

    class Meta:
        model = Resultado

        # Campos retornados no JSON de resultado
        fields = [
            'id',
            'aluno_username',    # Nome do aluno
            'simulado_titulo',   # Título do simulado
            'acertos',           # Quantidade de acertos
            'total_questoes',    # Total de questões
            'score',             # Percentual de acertos
            'realizado_em',      # Data e hora da realização
        ]

    def get_aluno_username(self, obj):
        """
        Retorna o username do aluno em vez do ID.
        O 'obj' é a instância do Resultado sendo serializado.
        """
        # obj.aluno acessa o objeto User relacionado
        return obj.aluno.username

    def get_simulado_titulo(self, obj):
        """
        Retorna o título do simulado em vez do ID.
        """
        # obj.simulado acessa o objeto Simulado relacionado
        return obj.simulado.titulo

# Serializer de ranking — usado em GET /api/ranking
class RankingSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para exibir o ranking de alunos.
    Retorna apenas os dados necessários para a tabela de ranking.
    """

    # Campo calculado — retorna o nome do aluno
    aluno_username = serializers.SerializerMethodField()

    # Campo calculado — retorna o título do simulado
    simulado_titulo = serializers.SerializerMethodField()

    class Meta:
        model = Resultado

        # Campos retornados no JSON de ranking
        fields = [
            'aluno_username',   # Nome do aluno
            'simulado_titulo',  # Título do simulado
            'acertos',          # Quantidade de acertos
            'total_questoes',   # Total de questões
            'score',            # Percentual de acertos
            'realizado_em',     # Data e hora da realização
        ]

    def get_aluno_username(self, obj):
        """
        Retorna o username do aluno.
        """
        return obj.aluno.username

    def get_simulado_titulo(self, obj):
        """
        Retorna o título do simulado.
        """
        return obj.simulado.titulo
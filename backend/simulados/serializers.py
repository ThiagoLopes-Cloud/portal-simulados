# Importa o módulo serializers do Django REST Framework
from rest_framework import serializers

# Importa os models Simulado e Questao
from .models import Simulado
from questoes.models import Questao


# Serializer de Questao — usado dentro do SimuladoDetalheSerializer
class QuestaoSerializer(serializers.ModelSerializer):
    """
    Serializer para exibir as questões de um simulado.
    Retorna todos os campos necessários para o aluno responder a prova.
    Inclui URLs de imagens do enunciado e das alternativas.
    Atualizado para o formato ENEM com 5 alternativas (A, B, C, D, E).
    """

    class Meta:
        model = Questao

        # Campos retornados no JSON — inclui todas as alternativas e imagens
        # Não inclui 'resposta_correta' para não entregar a resposta ao aluno!
        fields = [
            'id',
            'ordem',
            'enunciado',
            'imagem_enunciado',  # URL da imagem do enunciado
            'opcao_a',
            'opcao_b',
            'opcao_c',
            'opcao_d',
            'opcao_e',           # Nova alternativa E — formato ENEM
            'imagem_opcao_a',    # URL da imagem da alternativa A
            'imagem_opcao_b',    # URL da imagem da alternativa B
            'imagem_opcao_c',    # URL da imagem da alternativa C
            'imagem_opcao_d',    # URL da imagem da alternativa D
            'imagem_opcao_e',    # URL da imagem da alternativa E
        ]


# Serializer de listagem — usado em GET /api/simulados
# Retorna apenas informações básicas do simulado (sem questões)
class SimuladoListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para listar simulados disponíveis.
    Usado na tela de lista de simulados do Vue.js.
    """

    # Campo calculado — conta quantas questões o simulado tem
    total_questoes = serializers.SerializerMethodField()

    class Meta:
        model = Simulado

        # Campos retornados no JSON de listagem
        fields = ['id', 'titulo', 'descricao', 'criado_em', 'total_questoes']

    def get_total_questoes(self, obj):
        """
        Método que calcula o total de questões do simulado.
        O 'obj' é a instância do Simulado sendo serializado.
        """
        return obj.questoes.count()


# Serializer de detalhe — usado em GET /api/simulados/{id}
# Retorna todas as questões do simulado para o aluno responder
class SimuladoDetalheSerializer(serializers.ModelSerializer):
    """
    Serializer completo com todas as questões do simulado.
    Usado na tela de prova do Vue.js.
    """

    # Aninha o QuestaoSerializer — retorna a lista completa de questões
    # many=True indica que são múltiplas questões
    # read_only=True indica que as questões não podem ser editadas por aqui
    questoes = QuestaoSerializer(many=True, read_only=True)

    # Campo calculado — conta quantas questões o simulado tem
    total_questoes = serializers.SerializerMethodField()

    class Meta:
        model = Simulado

        # Campos retornados no JSON de detalhe — inclui a lista de questões
        fields = ['id', 'titulo', 'descricao', 'criado_em', 'total_questoes', 'questoes']

    def get_total_questoes(self, obj):
        """
        Método que calcula o total de questões do simulado.
        """
        return obj.questoes.count()
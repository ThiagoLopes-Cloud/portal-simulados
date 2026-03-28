# simulados/serializers.py
# Serializers atualizados para o novo relacionamento M2M via SimuladoQuestao.
# As questões agora são obtidas ordenadas pelo campo 'ordem' da tabela intermediária.

from rest_framework import serializers
from .models import Simulado, SimuladoQuestao
from questoes.models import Questao


class QuestaoSerializer(serializers.ModelSerializer):
    """
    Serializer para exibir os dados de uma questão ao aluno durante a prova.
    NÃO inclui 'resposta_correta' nem 'explicacao' — entregues só após responder.
    Inclui o campo 'ordem' injetado manualmente via SerializerMethodField.
    """

    # Campo 'ordem' não existe na Questao, mas sim em SimuladoQuestao.
    # Precisamos injetá-lo no contexto para exibir ao aluno.
    # O serializer recebe 'ordem' via source='simulado_questoes' no método do pai.
    ordem = serializers.IntegerField(read_only=True)

    class Meta:
        model = Questao
        fields = [
            'id',
            'ordem',             # Posição da questão neste simulado
            'enunciado',
            'imagem_enunciado',
            'opcao_a',
            'opcao_b',
            'opcao_c',
            'opcao_d',
            'opcao_e',
            'imagem_opcao_a',
            'imagem_opcao_b',
            'imagem_opcao_c',
            'imagem_opcao_d',
            'imagem_opcao_e',
            'dificuldade',       # Exibido ao aluno para contexto (opcional no front)
        ]
        # Segurança: resposta_correta e explicacao nunca saem neste serializer


class SimuladoListSerializer(serializers.ModelSerializer):
    """
    Serializer simplificado para a listagem de simulados disponíveis.
    Retorna apenas dados resumidos — sem a lista de questões.
    Usado em GET /api/simulados/
    """

    # Conta as questões via tabela intermediária
    total_questoes = serializers.SerializerMethodField()

    class Meta:
        model = Simulado
        fields = [
            'id',
            'titulo',
            'descricao',
            'criado_em',
            'data_inicio',
            'data_fim',
            'total_questoes',
        ]

    def get_total_questoes(self, obj):
        # Conta pelos registros da tabela intermediária, não pelo M2M direto.
        # É mais eficiente pois evita JOIN desnecessário com a tabela de questões.
        return obj.simulado_questoes.count()


class SimuladoDetalheSerializer(serializers.ModelSerializer):
    """
    Serializer completo com todas as questões ordenadas.
    Usado em GET /api/simulados/{id}/ — tela de prova do Vue.js.
    
    A ordem das questões é definida pela tabela SimuladoQuestao.
    Usamos SerializerMethodField para injetar o campo 'ordem' em cada questão.
    """

    questoes = serializers.SerializerMethodField()
    total_questoes = serializers.SerializerMethodField()

    class Meta:
        model = Simulado
        fields = [
            'id',
            'titulo',
            'descricao',
            'criado_em',
            'data_inicio',
            'data_fim',
            'total_questoes',
            'questoes',
        ]

    def get_questoes(self, obj):
        """
        Retorna as questões ordenadas pelo campo 'ordem' da tabela intermediária.
        
        Estratégia: percorrer os SimuladoQuestao ordenados e injetar
        o campo 'ordem' em cada objeto Questao antes de serializar.
        Evita N+1 queries com select_related.
        """

        # Busca os vínculos ordenados, com a questão em join — 1 query só
        simulado_questoes = (
            obj.simulado_questoes
            .select_related('questao', 'questao__tema')
            .order_by('ordem')
        )

        questoes_serializadas = []
        for sq in simulado_questoes:
            questao = sq.questao

            # Injeta o campo 'ordem' diretamente no objeto questão.
            # Isso é necessário porque 'ordem' vive na tabela intermediária,
            # não no model Questao — o serializer precisa encontrá-lo.
            questao.ordem = sq.ordem

            serializer = QuestaoSerializer(questao)
            questoes_serializadas.append(serializer.data)

        return questoes_serializadas

    def get_total_questoes(self, obj):
        return obj.simulado_questoes.count()
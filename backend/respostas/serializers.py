# Importa o módulo serializers do Django REST Framework
from rest_framework import serializers

# Importa o model Resposta
from .models import Resposta

# Importa o model Questao para validar se a questão pertence ao simulado
from questoes.models import Questao

# Serializer de uma resposta individual — usado dentro do ResponderSerializer
class RespostaItemSerializer(serializers.Serializer):
    """
    Serializer para uma resposta individual de uma questão.
    Recebe o id da questão e a opção escolhida pelo aluno.
    """

    # ID da questão que o aluno está respondendo
    questao_id = serializers.IntegerField(
        label='ID da Questão'
    )

    # Opção escolhida pelo aluno (A, B, C ou D)
    opcao_escolhida = serializers.ChoiceField(
        choices=['A', 'B', 'C', 'D'],
        label='Opção Escolhida'
    )

# Serializer principal — usado em POST /api/responder
class ResponderSerializer(serializers.Serializer):
    """
    Serializer para receber todas as respostas de um simulado de uma vez.
    O Vue.js envia o id do simulado e a lista de respostas do aluno.

    Exemplo de JSON recebido:
    {
        "simulado_id": 1,
        "respostas": [
            {"questao_id": 1, "opcao_escolhida": "B"},
            {"questao_id": 2, "opcao_escolhida": "A"},
            {"questao_id": 3, "opcao_escolhida": "D"}
        ]
    }
    """

    # ID do simulado que está sendo respondido
    simulado_id = serializers.IntegerField(
        label='ID do Simulado'
    )

    # Lista de respostas — usa o RespostaItemSerializer para validar cada item
    # many=True indica que é uma lista de respostas
    respostas = RespostaItemSerializer(
        many=True,
        label='Respostas'
    )

# Serializer de exibição — usado para retornar o resultado após responder
class RespostaSerializer(serializers.ModelSerializer):
    """
    Serializer para exibir uma resposta salva no banco.
    Usado para mostrar o gabarito após a correção.
    """

    class Meta:
        model = Resposta

        # Campos retornados no JSON de resposta
        fields = ['id', 'questao', 'opcao_escolhida', 'correta', 'respondido_em']

        # Todos os campos são somente leitura
        read_only_fields = ['id', 'questao', 'opcao_escolhida', 'correta', 'respondido_em']
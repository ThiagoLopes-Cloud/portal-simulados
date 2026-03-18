# Importa o módulo serializers do Django REST Framework
from rest_framework import serializers

# Importa o modelo User customizado
from .models import User

# Serializer de registro — usado quando um novo usuário se cadastra
class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer para cadastro de novos usuários.
    Recebe os dados do formulário de registro e cria um novo usuário no banco.
    """

    # Campo de confirmação de senha — apenas para validação, não salva no banco
    password2 = serializers.CharField(
        write_only=True,  # Não aparece na resposta JSON
        label='Confirmar senha'
    )

    class Meta:
        # Define qual model esse serializer representa
        model = User

        # Campos que serão aceitos no JSON de entrada
        fields = ['username', 'email', 'password', 'password2', 'role']

        extra_kwargs = {
            # write_only=True — senha não aparece na resposta JSON por segurança
            'password': {'write_only': True},
        }

    def validate(self, data):
        """
        Validação customizada — verifica se as senhas conferem.
        Chamado automaticamente pelo DRF antes de salvar.
        """
        # Compara password com password2
        if data['password'] != data['password2']:
            raise serializers.ValidationError('As senhas não conferem.')
        return data

    def create(self, validated_data):
        """
        Cria o usuário no banco após a validação.
        Usa create_user para garantir que a senha seja criptografada.
        """
        # Remove o password2 pois não existe no model
        validated_data.pop('password2')

        # create_user criptografa a senha automaticamente — nunca salva em texto puro
        user = User.objects.create_user(**validated_data)
        return user

# Serializer de perfil — usado para exibir dados do usuário logado
class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para exibir os dados do usuário autenticado.
    Usado nas respostas da API após login ou em perfil.
    """

    class Meta:
        model = User

        # Campos que serão retornados no JSON de resposta
        fields = ['id', 'username', 'email', 'role']

        # Todos os campos são somente leitura — não permite edição por aqui
        read_only_fields = ['id', 'username', 'email', 'role']
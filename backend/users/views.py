# Importa o módulo de views do Django REST Framework
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

# Importa a permissão que permite acesso sem autenticação
# Necessário para as rotas de login e registro
from rest_framework.permissions import AllowAny

# Importa os serializers de usuário
from .serializers import RegisterSerializer, UserSerializer

class RegisterView(APIView):
    """
    View de cadastro de novos usuários.
    Rota: POST /api/register
    Não requer autenticação — qualquer pessoa pode se cadastrar.
    """

    # AllowAny — permite acesso sem token JWT
    # Sobrescreve a configuração padrão do settings.py
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Recebe os dados do formulário de registro e cria um novo usuário.
        Retorna os dados do usuário criado ou os erros de validação.
        """

        # Passa os dados recebidos para o serializer validar
        serializer = RegisterSerializer(data=request.data)

        # Verifica se os dados são válidos
        if serializer.is_valid():
            # Salva o usuário no banco de dados
            user = serializer.save()

            # Serializa o usuário criado para retornar no JSON
            user_data = UserSerializer(user).data

            # Retorna os dados do usuário com status 201 (Created)
            return Response({
                'message': 'Usuário criado com sucesso!',
                'user': user_data
            }, status=status.HTTP_201_CREATED)

        # Se os dados forem inválidos, retorna os erros com status 400 (Bad Request)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    """
    View de perfil do usuário autenticado.
    Rota: GET /api/profile
    Requer autenticação — só o próprio usuário pode ver seu perfil.
    """

    def get(self, request):
        """
        Retorna os dados do usuário autenticado.
        O request.user é preenchido automaticamente pelo JWT.
        """

        # Serializa o usuário autenticado
        serializer = UserSerializer(request.user)

        # Retorna os dados do usuário com status 200 (OK)
        return Response(serializer.data, status=status.HTTP_200_OK)
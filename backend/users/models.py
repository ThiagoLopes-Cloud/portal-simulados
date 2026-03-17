from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Model de usuário customizado.
    Extende o User padrão do Django adicionando o campo 'role'.
    Isso permite diferenciar estudantes de administradores/professores.
    """

    # Opções de papel disponíveis no sistema
    STUDENT = 'student'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (STUDENT, 'Estudante'),
        (ADMIN, 'Administrador'),
    ]

    # Campo que define o papel do usuário no sistema
    # Por padrão todo usuário novo é criado como estudante
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=STUDENT,
        verbose_name='Papel'
    )

    def __str__(self):
        return f'{self.username} ({self.get_role_display()})'

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
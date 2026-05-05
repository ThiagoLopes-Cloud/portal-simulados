from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class User(AbstractUser):
    STUDENT = "student"
    ADMIN = "admin"
    ROLE_CHOICES = [(STUDENT, "Estudante"), (ADMIN, "Administrador")]

    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default=STUDENT, verbose_name="Papel"
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"


# --- NOVO MODELO DE GAMIFICAÇÃO ---
class Perfil(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="perfil"
    )
    xp = models.IntegerField(default=0, verbose_name="Pontos de Experiência")
    ofensiva = models.IntegerField(default=0, verbose_name="Dias Seguidos")
    ultima_atividade = models.DateField(null=True, blank=True)

    def registrar_atividade(self, xp_ganho):
        """
        Calcula a lógica de dias consecutivos (Foguinho/Streak).
        """
        hoje = timezone.now().date()
        self.xp += xp_ganho

        if self.ultima_atividade == hoje:
            # Já estudou hoje, não mexe na ofensiva
            pass
        elif self.ultima_atividade == hoje - timedelta(days=1):
            # Estudou ontem e hoje: +1 dia de ofensiva! 🔥
            self.ofensiva += 1
        else:
            # Quebrou a sequência ou é a primeira vez: reseta para 1
            self.ofensiva = 1

        self.ultima_atividade = hoje
        self.save()

    class Meta:
        verbose_name = "Perfil Gamificado"
        verbose_name_plural = "Perfis Gamificados"

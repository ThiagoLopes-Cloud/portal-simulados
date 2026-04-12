# escolas/models.py
from django.db import models
from django.conf import settings
import uuid

class Turma(models.Model):
    nome = models.CharField(max_length=100)
    codigo_convite = models.CharField(max_length=12, unique=True, blank=True)
    
    professor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        related_name='turmas_gerenciadas'
    )
    
    alunos = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='minhas_turmas',
        blank=True
    )

    # AQUI ESTÁ A MÁGICA: Ligando a Turma aos Simulados!
    simulados = models.ManyToManyField(
        'simulados.Simulado', 
        blank=True, 
        related_name='turmas'
    )

    criado_em = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.codigo_convite:
            self.codigo_convite = str(uuid.uuid4()).split('-')[0].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome} ({self.codigo_convite})"
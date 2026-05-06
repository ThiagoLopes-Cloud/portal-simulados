from django.db import models
from django.conf import settings
from django.utils import timezone


class Trilha(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    icone = models.CharField(max_length=10, default="📚")
    cor = models.CharField(max_length=20, default="#4F46E5")
    ordem = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["ordem", "nome"]

    def __str__(self):
        return self.nome


class Modulo(models.Model):
    trilha = models.ForeignKey(Trilha, on_delete=models.CASCADE, related_name="modulos")
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True)
    ordem = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["ordem"]

    def __str__(self):
        return f"{self.trilha.nome} › {self.nome}"


class Aula(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name="aulas")
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    video_url = models.URLField(blank=True)
    duracao_minutos = models.PositiveIntegerField(default=0)
    ordem = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["ordem"]

    def __str__(self):
        return f"{self.modulo.nome} › {self.titulo}"


class ProgressoAluno(models.Model):
    aluno = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="progressos_aulas",
    )
    aula = models.ForeignKey(Aula, on_delete=models.CASCADE, related_name="progressos")
    is_completed = models.BooleanField(default=False)
    concluido_em = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ["aluno", "aula"]

    def __str__(self):
        status = "✓" if self.is_completed else "○"
        return f"{self.aluno.username} {status} {self.aula.titulo}"


class Material(models.Model):
    TIPO_CHOICES = [
        ("PDF", "PDF"),
        ("VIDEO", "Vídeo"),
        ("LINK", "Link Externo"),
        ("EXERCICIO", "Lista de Exercícios"),
    ]

    modulo = models.ForeignKey(
        Modulo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="materiais",
    )
    aula = models.ForeignKey(
        Aula,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="materiais",
    )
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default="PDF")
    arquivo = models.FileField(upload_to="materiais/", blank=True, null=True)
    url_externa = models.URLField(blank=True)
    tamanho_kb = models.PositiveIntegerField(default=0)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"[{self.tipo}] {self.titulo}"

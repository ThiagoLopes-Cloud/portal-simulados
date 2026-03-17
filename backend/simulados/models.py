# Importa o módulo models do Django — contém todos os tipos de campos do banco
from django.db import models

# Importa nosso User customizado para criar o relacionamento
from users.models import User

# Define a classe Simulado que representa uma tabela no banco de dados
# Toda classe que herda de models.Model vira uma tabela no PostgreSQL
class Simulado(models.Model):
    """
    Representa uma prova/simulado no sistema.
    Criado pelo admin/professor e disponível para os estudantes responderem.
    """

    # Campo de texto curto — armazena o título do simulado
    # max_length=200 define o limite máximo de caracteres
    titulo = models.CharField(
        max_length=200,
        verbose_name='Título'  # Nome exibido no Django Admin
    )

    # Campo de texto longo — armazena a descrição do simulado
    # blank=True significa que o campo não é obrigatório
    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição'
    )

    # ForeignKey cria um relacionamento "muitos para um"
    # Muitos simulados podem pertencer a um único professor
    # on_delete=SET_NULL — se o professor for deletado, o simulado permanece
    # null=True — permite que o campo fique vazio no banco
    # related_name — permite acessar os simulados de um user com user.simulados_criados.all()
    criado_por = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='simulados_criados',
        verbose_name='Criado por'
    )

    # Campo de data e hora — preenchido automaticamente quando o simulado é criado
    # auto_now_add=True significa que o Django preenche sozinho na criação
    criado_em = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )

    # Campo booleano (True/False) — permite ocultar simulados sem deletar do banco
    # default=True significa que todo simulado novo começa como ativo
    ativo = models.BooleanField(
        default=True,
        verbose_name='Ativo'
    )

    # Método __str__ define como o objeto aparece como texto
    # Ex: no Django Admin vai mostrar o título em vez de "Simulado object (1)"
    def __str__(self):
        return self.titulo

    # Classe Meta define configurações extras do model
    class Meta:
        verbose_name = 'Simulado'           # Nome singular no Admin
        verbose_name_plural = 'Simulados'   # Nome plural no Admin
        ordering = ['-criado_em']           # Ordena pelos mais recentes primeiro
                                            # O sinal '-' significa ordem decrescente
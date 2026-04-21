from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conteudo', '0002_alter_materia_options_alter_tema_options_and_more'),
        ('importador', '0006_questaoimportada_tema_dificuldade'),
    ]

    operations = [
        migrations.AddField(
            model_name='questaoimportada',
            name='imagem_enunciado_arquivo',
            field=models.FileField(
                blank=True,
                null=True,
                upload_to='importacoes/imagens/enunciados/',
                verbose_name='Imagem extraida do enunciado',
            ),
        ),
        migrations.AddField(
            model_name='questaoimportada',
            name='pagina_inicial',
            field=models.PositiveIntegerField(
                blank=True,
                null=True,
                verbose_name='Pagina inicial',
            ),
        ),
        migrations.AlterField(
            model_name='questaoimportada',
            name='dificuldade',
            field=models.CharField(
                choices=[('F', 'Facil'), ('M', 'Medio'), ('D', 'Dificil')],
                default='M',
                max_length=1,
                verbose_name='Dificuldade',
            ),
        ),
        migrations.AlterField(
            model_name='questaoimportada',
            name='idioma',
            field=models.CharField(
                blank=True,
                choices=[('ingles', 'Ingles'), ('espanhol', 'Espanhol')],
                max_length=20,
                null=True,
                verbose_name='Idioma',
            ),
        ),
        migrations.AlterField(
            model_name='questaoimportada',
            name='prova_original',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='questoes_importadas',
                to='importador.provaoriginal',
                verbose_name='Prova original',
            ),
        ),
        migrations.AlterField(
            model_name='questaoimportada',
            name='questao_oficial',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='importacoes_publicadas',
                to='questoes.questao',
                verbose_name='Questao oficial publicada',
            ),
        ),
        migrations.AlterField(
            model_name='questaoimportada',
            name='status',
            field=models.CharField(
                choices=[
                    ('pendente_aprovacao', 'Pendente de aprovacao'),
                    ('correcao_necessaria', 'Correcao necessaria'),
                    ('rejeitada', 'Rejeitada'),
                    ('publicada', 'Publicada'),
                ],
                default='pendente_aprovacao',
                max_length=30,
                verbose_name='Status',
            ),
        ),
        migrations.AlterField(
            model_name='questaoimportada',
            name='tema',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='questoes_importadas',
                to='conteudo.tema',
                verbose_name='Tema',
            ),
        ),
    ]

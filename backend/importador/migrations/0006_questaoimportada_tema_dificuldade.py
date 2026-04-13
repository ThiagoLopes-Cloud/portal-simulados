from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conteudo', '0001_initial'),
        ('importador', '0005_idioma_campos'),
    ]

    operations = [
        migrations.AddField(
            model_name='questaoimportada',
            name='dificuldade',
            field=models.CharField(
                choices=[('F', 'Facil'), ('M', 'Medio'), ('D', 'Dificil')],
                default='M',
                max_length=1,
                verbose_name='Dificuldade',
            ),
        ),
        migrations.AddField(
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

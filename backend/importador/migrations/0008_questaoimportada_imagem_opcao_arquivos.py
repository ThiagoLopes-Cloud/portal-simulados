from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("importador", "0007_questaoimportada_imagem_enunciado_arquivo_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="questaoimportada",
            name="imagem_opcao_a_arquivo",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="importacoes/imagens/opcoes/",
                verbose_name="Imagem extraida da alternativa A",
            ),
        ),
        migrations.AddField(
            model_name="questaoimportada",
            name="imagem_opcao_b_arquivo",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="importacoes/imagens/opcoes/",
                verbose_name="Imagem extraida da alternativa B",
            ),
        ),
        migrations.AddField(
            model_name="questaoimportada",
            name="imagem_opcao_c_arquivo",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="importacoes/imagens/opcoes/",
                verbose_name="Imagem extraida da alternativa C",
            ),
        ),
        migrations.AddField(
            model_name="questaoimportada",
            name="imagem_opcao_d_arquivo",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="importacoes/imagens/opcoes/",
                verbose_name="Imagem extraida da alternativa D",
            ),
        ),
        migrations.AddField(
            model_name="questaoimportada",
            name="imagem_opcao_e_arquivo",
            field=models.FileField(
                blank=True,
                null=True,
                upload_to="importacoes/imagens/opcoes/",
                verbose_name="Imagem extraida da alternativa E",
            ),
        ),
    ]

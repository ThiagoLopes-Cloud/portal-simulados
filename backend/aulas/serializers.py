from rest_framework import serializers
from .models import Trilha, Modulo, Aula, ProgressoAluno, Material


class MaterialSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Material
        fields = ["id", "titulo", "descricao", "tipo", "url", "tamanho_kb"]

    def get_url(self, obj):
        if obj.url_externa:
            return obj.url_externa
        if obj.arquivo:
            request = self.context.get("request")
            return request.build_absolute_uri(obj.arquivo.url) if request else obj.arquivo.url
        return None


class AulaSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    materiais = MaterialSerializer(many=True, read_only=True)

    class Meta:
        model = Aula
        fields = [
            "id", "titulo", "descricao", "video_url",
            "duracao_minutos", "ordem", "is_completed", "materiais",
        ]

    def get_is_completed(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return ProgressoAluno.objects.filter(
            aluno=request.user, aula=obj, is_completed=True
        ).exists()


class ModuloSerializer(serializers.ModelSerializer):
    aulas = AulaSerializer(many=True, read_only=True)
    total_aulas = serializers.SerializerMethodField()
    aulas_concluidas = serializers.SerializerMethodField()

    class Meta:
        model = Modulo
        fields = ["id", "nome", "descricao", "ordem", "total_aulas", "aulas_concluidas", "aulas"]

    def get_total_aulas(self, obj):
        return obj.aulas.count()

    def get_aulas_concluidas(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return 0
        return ProgressoAluno.objects.filter(
            aluno=request.user, aula__modulo=obj, is_completed=True
        ).count()


class TrilhaListSerializer(serializers.ModelSerializer):
    total_aulas = serializers.SerializerMethodField()
    aulas_concluidas = serializers.SerializerMethodField()
    total_modulos = serializers.SerializerMethodField()
    percentual_progresso = serializers.SerializerMethodField()

    class Meta:
        model = Trilha
        fields = [
            "id", "nome", "descricao", "icone", "cor",
            "total_modulos", "total_aulas", "aulas_concluidas", "percentual_progresso",
        ]

    def get_total_modulos(self, obj):
        return obj.modulos.count()

    def get_total_aulas(self, obj):
        from django.db.models import Count
        return Aula.objects.filter(modulo__trilha=obj).count()

    def get_aulas_concluidas(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return 0
        return ProgressoAluno.objects.filter(
            aluno=request.user,
            aula__modulo__trilha=obj,
            is_completed=True,
        ).count()

    def get_percentual_progresso(self, obj):
        total = self.get_total_aulas(obj)
        if total == 0:
            return 0
        concluidas = self.get_aulas_concluidas(obj)
        return round((concluidas / total) * 100)


class TrilhaDetalheSerializer(TrilhaListSerializer):
    modulos = serializers.SerializerMethodField()

    class Meta(TrilhaListSerializer.Meta):
        fields = TrilhaListSerializer.Meta.fields + ["modulos"]

    def get_modulos(self, obj):
        return ModuloSerializer(
            obj.modulos.all(), many=True, context=self.context
        ).data

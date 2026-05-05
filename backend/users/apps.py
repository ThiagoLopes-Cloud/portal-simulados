from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"

    def ready(self):
        # Esta linha importa os sinais quando o app é iniciado,
        # ativando a criação automática do Perfil Gamificado.
        import users.signals
